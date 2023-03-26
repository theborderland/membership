import os

from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import render, redirect

from ..forms import LowIncomeForm


class LowIncome(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/register_low_income.html"
    form_class = LowIncomeForm
    success_url = '..'
    success_message = "%(first_name)s, you've registered! Good luck!" # FIXME!!!!

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        # TODO move to config
        ctx.update(
            {"open": bool(os.getenv("ENABLE_LOTTERY_REGISTRATION")),
             "low_income_enabled": bool(os.getenv("ENABLE_LOTTERY_LOW_INCOME"))})
        return ctx

    def form_valid(self, form):
        if form.instance.email != self.request.POST.get("email_again", ""):
            messages.add_message(self.request, messages.ERROR, "Check your email address!")
            return render(self.request, template_name=self.template_name, context=self.get_context_data())

        form.instance.event = self.request.event
        form.instance.email = self.request.request.POST["email"]
        form.instance.dob = self.request.request.POST["dob"]

        ret = super().form_valid(form)
        return ret


