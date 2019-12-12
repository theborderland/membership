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

    class Meta:
        model = LotteryEntry
        fields = [ "email", "first_name", "last_name", "dob" ]

class Register(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/register.html"
    form_class = RegisterForm
    success_url = '..'
    success_message = "%(first_name)s, you've registered! Good luck!"

    # TODO move to config
    email_subject = "Receipt"
    email_message = """
For reference, this is the information you provided:

  * First Name: %(first_name)s
  * Last Name: %(last_name)s
  * Date of Birth: %(dob)s
    """ # TODO

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        # TODO move to config
        ctx.update({ "open": datetime.now() < datetime(2020, 2, 1, 4, 0) })
        return ctx


    def post(self, request, *args, **kwargs):
        try:
            sup = super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                 "This email address or name and date-of-birth combination is already registered!")
            return render(request,template_name=self.template_name,context=self.get_context_data())
        send_mail(event_id=self.request.event.id,
                    to = [ request.POST["email"] ],
                    subject = self.email_subject,
                    body = self.email_message % request.POST.dict())
        return sup

    @transaction.atomic
    def form_valid(self, form):
        form.instance.event = self.request.event
        form.instance.browser = self.request.META.get('HTTP_USER_AGENT', "")
        form.instance.ip = self.request.META.get('REMOTE_ADDR', "")
        # TODO cookie
        # emit log message
        ret = super().form_valid(form)
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
    queryset = LotteryEntry.objects.all().order_by('id')
    permission = 'can_view_orders'
    serializer_class = LotteryEntrySerializer

    def update(self, request, *args, **kwargs):
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
