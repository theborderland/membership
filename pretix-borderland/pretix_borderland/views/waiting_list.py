import os
from datetime import date
from django.db import transaction, IntegrityError
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from pretix.helpers.http import get_client_ip

from ..tasks import send_mail
from ..forms import JoinWaitingList


class WaitingList(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/waiting_list.html"
    form_class = JoinWaitingList

    success_url = '..'
    success_message = "%(first_name)s, you're registered in the membership transfers waiting list! Good luck!"

    # TODO move to config
    email_subject = "You just joined the waiting list ..."
    email_message = """Beep!

You are now signed in the membership transfer waiting list. 

We'll get in touch with you as soon as there is a membership available! 

Good Luck 🍀!

The Borderland Computer ‍🤖❤️‍💋‍
    """  # TODO

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        # TODO move to config
        ctx.update({"waiting_lists_enabled": bool(os.getenv("ENABLE_TRANSFER_WAITINGLIST_REGISTRATION"))})
        return ctx

    def form_valid(self, form):
        today = date.today()
        dob = date(form.instance.dob.year, form.instance.dob.month, form.instance.dob.day)
        age_years = int((today - dob).days / 365.25)

        if age_years < 18:
            messages.add_message(self.request, messages.ERROR, "You must be at least a legal adult to register")
            return render(self.request, template_name=self.template_name, context=self.get_context_data())

        form.instance.event = self.request.event
        try:
            with transaction.atomic():
                ret = super().form_valid(form)
        except IntegrityError:
            messages.add_message(self.request, messages.ERROR,
                                 "This email address is already registered to the Waiting List!")
            return render(self.request, template_name=self.template_name, context=self.get_context_data())

        send_mail(event_id=self.request.event.id,
                  to=[self.request.POST["email"]],
                  subject=self.email_subject,
                  body=self.email_message % self.request.POST.dict())
        return ret
