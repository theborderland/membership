
from django.db import transaction, IntegrityError
from django.views.generic import CreateView, TemplateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render

from rest_framework import status, viewsets
from rest_framework.response import Response

from .models import LotteryForm
from .serializers import LotteryFormSerializer

# TODO
# deal with deadlines
# nice form
# tracking info
# send email confirmation

class RegisterForm(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/register.html"
    model = LotteryForm
    fields = [ "email", "first_name", "last_name", "dob" ]
    success_url = '..'
    success_message = "%(first_name)s %(last_name)s successfully registered with address %(email)s! Good luck!"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        return ctx

    def post(self, request, *args, **kwargs): # Is this the way to do it?
        try:
            return super().post(request, *args, **kwargs)
        except IntegrityError:
            messages.add_message(request, messages.ERROR, "This email address or name and date-of-birth combination is already registered!")
            return render(request,template_name=self.template_name,context=self.get_context_data())


    @transaction.atomic
    def form_valid(self, form):
        form.instance.event = self.request.event
        # todo store tracking info
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
