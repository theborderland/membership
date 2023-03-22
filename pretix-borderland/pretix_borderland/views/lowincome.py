import os

from django.views.generic import CreateView
from django.contrib.messages.views import SuccessMessageMixin

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
        form.instance.event = self.request.event
        form.instance.email = self.request.request.POST["email"]
        form.instance.dob = self.request.request.POST["dob"]

        ret = super().form_valid(form)
        return ret


