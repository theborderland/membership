import os

from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect

from pretix.base.models import Event
from ..forms import LowIncomeForm
from ..models import LotteryEntry, LowIncomeEntry


class LowIncome(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/register_low_income.html"
    form_class = LowIncomeForm
    success_url = 'plugins:pretix_borderland:register'
    success_message = "Success!, your application has been sent."
    organizer = None
    event = None
    email = None


    def get(self, request, *args, **kwargs):
        self.organizer = kwargs.get("organizer")
        self.event = kwargs.get("event")
        self.email = kwargs.get("email")
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()

        event = Event.objects.filter(slug=self.event).first()
        is_registered = LotteryEntry.objects.filter(event=event, email=self.email).exists()
        has_applied_already = LowIncomeEntry.objects.filter(event=event, email=self.email).exists()

        # TODO move to config
        ctx.update(
            {
                "open": bool(os.getenv("ENABLE_LOTTERY_REGISTRATION")),
                "low_income_enabled": bool(os.getenv("ENABLE_LOTTERY_LOW_INCOME")),
                "registered": is_registered,
                "has_applied": has_applied_already,
            })
        return ctx

    def form_valid(self, form):
        form.instance.event = self.request.event

        try:
            super().form_valid(form)
        except Exception as e:
            messages.add_message(self.request, messages.ERROR,
                                 "You have already applied for a low income membership. Should you want to change your application, please contact the membership team directly on Discord.")
            return redirect("../../..")
