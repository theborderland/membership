import re

from django.db import transaction, IntegrityError
from django.views.generic import CreateView, TemplateView, View, UpdateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from django import forms

from rest_framework import status, viewsets
from rest_framework.response import Response

from datetime import datetime

from pretix.presale.views.order import OrderDetailMixin
from pretix.base.forms.widgets import DatePickerWidget
from pretix.base.models.event import Event
from pretix.helpers.http import get_client_ip

from .models import LotteryEntry, RefundRequest
from .serializers import LotteryEntrySerializer, RefundRequestSerializer
from .tasks import send_mail


# Lottery


class RegisterForm(forms.ModelForm):
    dob = forms.DateField(
        required=True,
        label='Date of Birth',
        widget=DatePickerWidget(),
    )
    dob_again = forms.DateField(
        required=True,
        label='Date of Birth again',
        widget=DatePickerWidget(),
    )
    email = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label="E-mail address")
    email_again = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label="E-mail address again")
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label="Legal First Name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label="Legal Last Name")

    class Meta:
        model = LotteryEntry
        fields = [ "email", "email_again", "first_name", "last_name", "dob" ]

class Register(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/register.html"
    form_class = RegisterForm
    success_url = '..'
    success_message = "%(first_name)s, you've registered! Good luck!"

    # TODO move to config
    email_subject = "Lottery Receipt 🔥"
    email_message = """Yay, you did it! You’ve successfully registered for the Grand Membership Lottery of the Borderland 2022! Now it’s time to kick back and give yourself time for some dreaming!

If you’re super eager and can’t wait, here’s some things you can do to get ready:

  * Dream your dreams! Anything (ish) is possible at the Borderland, you just gotta dream it (and then potentially realize it)! Think about what cool shennanigans you want to cook up this year!

  * Want to get into the thick of it? Check out what [responsibilities and lead roles that still has to be filled](https://coda.io/d/Realities-2022_dFvRNS5423Z/Responsibilities_sulZB#_luxNx) up for the event to actually happen and run smooothly! 

  * Involve yourself! If you’re ready to dive head first into some live action plotting, you should check out the [Borderland Discord](https://discord.gg/9bvgcSW2Ej) server! There’s so many cool things happening there, and anyone can help out. This is also a great place to ask questions! 

  * Read last year's Survival Guide! The Survival Guide contains EVERYTHING (ish) that you need to survive the Borderland! It hasn’t been updated to the 2022 edition yet though, but there’s a bunch of vital information in the old one that is still relevant! [https://talk.theborderland.se/survival](https://talk.theborderland.se/survival/) 

  * Join the Facebook group! So, Facebook isn’t always the best communication channel, as it tend to become a bit messy. But it’s still a great way to connect with people, and there’s a lot of future friends just waiting for you in there!

  * Create or join a camp! Camps are great to augment your Borderland experience! If you haven’t found one yet (or if you have and you’re looking for members), there’s a Facebook group for camp matchmaking. [Check it out](https://www.facebook.com/groups/2080911315480407)!  

Let’s keep our fingers crossed for a lucky strike at the Lottery, and see you soon! <3

Bleeps and bloops,

The Borderland Computer 👯🏽‍♂️🤖👨‍❤️‍💋‍👨
    """ # TODO

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        # TODO move to config
        ctx.update({ "open": datetime.now() >= datetime(2022, 4, 25, 0, 0) })
        return ctx


    def form_valid(self, form):
        if form.instance.dob.strftime("%Y-%m-%d") != self.request.POST.get("dob_again", "") or form.instance.dob.year > 2008:
            messages.add_message(self.request, messages.ERROR, "Check your date of birth!")
            return render(self.request,template_name=self.template_name,context=self.get_context_data())
        if form.instance.email != self.request.POST.get("email_again", ""):
            messages.add_message(self.request, messages.ERROR, "Check your email address!")
            return render(self.request,template_name=self.template_name,context=self.get_context_data())
        form.instance.event = self.request.event
        form.instance.browser = self.request.META.get('HTTP_USER_AGENT', "")
        form.instance.ip = get_client_ip(self.request)
        form.instance.cookie = self.request.COOKIES.get("pretix_csrftoken")
        try:
            with transaction.atomic():
                ret = super().form_valid(form)
        except IntegrityError:
            messages.add_message(self.request, messages.ERROR,
                                 "This email address is already registered!")
            return render(self.request,template_name=self.template_name,context=self.get_context_data())
        send_mail(event_id=self.request.event.id,
                    to = [ self.request.POST["email"] ],
                    subject = self.email_subject,
                    body = self.email_message % self.request.POST.dict())
        return ret


# SMEP

class RefundRequestView(SuccessMessageMixin, OrderDetailMixin, UpdateView):
    template_name = "pretix_borderland/refund_request.html"
    model = RefundRequest
    fields = []

    def get_success_url(self):
        return self.get_order_url()

    def get_error_url(self):
        return self.get_order_url()

    def get_success_message(self, value):
        return 'Refund request sent.'

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(order=self.order)
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['order'] = self.order
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        if self.order.status != "p":
            raise forms.ValidationError("Can only cancel paid orders!")
        form.instance.status = "p"
        self.order.log_action('pretix.plugins.borderland.refund.request', data=form)
        ret = super().form_valid(form)
        return ret



class TransferRequestView(RefundRequestView):
    template_name = "pretix_borderland/transfer_request.html"
    fields = ["target", "user_comment"]

    def get_success_message(self, value):
        return 'Transfer request sent!'


class TransferRequestCancel(SuccessMessageMixin, OrderDetailMixin, View):
    def post(self, request, *args, **kwargs):
        req, created = RefundRequest.objects.get_or_create(order=self.order)
        if req.status == 'p':
            req.status = 'c'
            req.save()
            self.order.log_action('pretix.plugins.borderland.refund.cancel', data=form)
            messages.add_message(request, messages.SUCCESS, "Transfer request cancelled!")
        return redirect(self.get_order_url())

# API viewsets TODO move

class RegisterAPIViewSet(viewsets.ModelViewSet):
    permission = 'can_view_orders'
    serializer_class = LotteryEntrySerializer

    def get_queryset(self):
        event = re.findall(r"events/([^.]*)/registration", self.request.path)
        if not event:
            return Response({'error': 'invalid request, event not found'}, status=401)

        events = Event.objects.filter(slug=event[0])
        if not events:
            return Response({'error': 'event not found'}, status=404)

        return LotteryEntry.objects.filter(event_id=events[0].id).order_by('id')

    def update(self, request, pk=None):
        self.event.log_action('pretix.plugins.borderland.registration.api_update', data=request.data, auth=request.auth)
        return super.update(self, request, *args, **kwargs)

class EmailViewSet(viewsets.GenericViewSet):
    permission = 'can_view_orders'

    def create(self, request, organizer, event):
        self.request.event.log_action('pretix.plugins.borderland.email.send', data=request.data, auth=request.auth)
        d = request.data
        m = send_mail(event_id=self.request.event.id,
                    to=d['to'],
                    body=d['body'],
                    subject=d['subject']
        )
        return Response({"result": "ok i guess"})

class TransferAPIViewSet(viewsets.ModelViewSet):
    queryset = RefundRequest.objects.all().order_by('id')
    permission = 'can_view_orders'
    serializer_class = RefundRequestSerializer

    def update(self, request, *args, **kwargs):
        self.event.log_action('pretix.plugins.borderland.refund.api_update', data=request.data, auth=request.auth)
        return super.update(self, request, *args, **kwargs)
