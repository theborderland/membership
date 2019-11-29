
from django.db import transaction, IntegrityError
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.response import Response

from datetime import datetime

from .models import LotteryForm
from .serializers import LotteryFormSerializer
from .tasks import send_mail

class RegisterForm(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/register.html"
    model = LotteryForm
    fields = [ "email", "first_name", "last_name", "dob" ]
    success_url = '..'
    success_message = "%(first_name)s, you've registered! Good luck!"

    success_email = """
For reference, this is the information you provided:

    - First Name: %(first_name)s
    - Last Name: %(last_name)s
    - Date of Birth: %(dob)s
    """ # TODO

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        # TODO move to config
        ctx.update({ "open": datetime.now() < datetime(2020, 1, 30) })
        return ctx


    def post(self, request, *args, **kwargs): # Is this the way to do it?
        try:
            sup = super().post(request, *args, **kwargs)
            send_mail(event_id=self.request.event.id,
                      to = [ request.POST["email"] ],
                      subject = "Borderland Lottery Receipt", # TODO
                      body = self.success_email % request.POST.dict())
            return sup
        except IntegrityError:
            messages.add_message(request, messages.ERROR,
                                 "This email address or name and date-of-birth combination is already registered!")
            return render(request,template_name=self.template_name,context=self.get_context_data())


    @transaction.atomic
    def form_valid(self, form):
        form.instance.event = self.request.event
        form.instance.browser = self.request.META.get('HTTP_USER_AGENT', "")
        form.instance.ip = self.request.META.get('REMOTE_ADDR', "")
        # TODO cookie
        # emit log message
        ret = super().form_valid(form)
        return ret


class RegisterAPIViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = LotteryForm.objects.all()
    permission = 'can_view_orders'
    serializer_class = LotteryFormSerializer

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx['event'] = self.request.event
        return ctx


class EmailViewSet(viewsets.GenericViewSet):
    permission = 'can_view_orders'

    def create(self, request, organizer, event):
        d = request.data
        m = send_mail(event_id=self.request.event.id,
                    to=d['to'],
                    body=d['body'],
                    subject=d['subject']
        )
        return Response({"result": "ok i guess"})
