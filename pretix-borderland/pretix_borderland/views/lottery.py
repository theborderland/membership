import os

from django.db import transaction, IntegrityError
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, redirect
from pretix.helpers.http import get_client_ip

from ..tasks import send_mail
from ..forms import RegisterForm
from .lowincome import LowIncome


class Register(SuccessMessageMixin, CreateView):
    template_name = "pretix_borderland/register.html"
    low_income_template_name = "pretix_borderland/register_low_income.html"
    form_class = RegisterForm
    success_url = '..'
    success_message = "%(first_name)s, you've registered! Good luck!"

    # TODO move to config
    email_subject = "Lottery Receipt 🔥"
    email_message = """
Congratulations! 🥳


You did it! ... You’ve successfully registered for the Membership Lottery of the Borderland 2024! 

There is still some time until the raffle, and yet more time to the Borderland. No worries if you don't win the raffle, there will be plenty of opportunities to get a membership, so relax and start getting in the mood in this cold February. 

In the meantime, here’s some things you can do to pre-prep the prep-prep-prep:

 * Dream big! The Borderland is a haven all creative and non-creative endeavors, so don't hold up and start making sketches of what you'd like to create/co-create.

 * Want to get some action? ... Check out the [responsibilities and Lead roles that still need sorting](https://coda.io/d/Realities-2023_dFvRNS5423Z/Responsibilities_sulZB#_luxNx) to make the event run as smoothly as possible! Get involved! ❤️  

 * Get Social! Join the [Borderland Discord](https://discord.gg/9bvgcSW2Ej) server and/or [Facebook](https://www.facebook.com/groups/2080911315480407) to connect with other borderlings in this quest.

 * Read the survival guide! It may not be updated to the 2024 edition yet, but there's a ton of helpful info to get clued up on! [Survival](https://coda.io/d/Survival-Guide_ddTvwEwgvJw/The-Borderland-2022-Survival-Guide_su5XR?fbclid=IwAR2f50DTyQbEZnqsTZZGk4bv0pMZfEdjN7jBZIdnaruZOcKoy7CQycr6IEg#_lucB5)


Bleeps and bloops,


The Membership team ❤️❤️❤️
"""

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        # TODO move to config
        ctx.update(
            {"registration_opened": bool(os.getenv("ENABLE_LOTTERY_REGISTRATION")),
             "low_income_enabled": bool(os.getenv("ENABLE_LOTTERY_LOW_INCOME"))})
        return ctx

    def form_valid(self, form):
        if form.instance.dob.strftime("%Y-%m-%d") != self.request.POST.get("dob_again",
                                                                           "") or form.instance.dob.year > 2009:
            messages.add_message(self.request, messages.ERROR, "Check your date of birth!")
            return render(self.request, template_name=self.template_name, context=self.get_context_data())

        if form.instance.email != self.request.POST.get("email_again", ""):
            messages.add_message(self.request, messages.ERROR, "Check your email address!")
            return render(self.request, template_name=self.template_name, context=self.get_context_data())

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
            return render(self.request, template_name=self.template_name, context=self.get_context_data())

        # If the information provided in the registration form is valid, we email the user confirming
        # their registration. If the user has applied for a low income ticket, we render after sending the email a
        # new form, so they can fill in information to be eligible for a low income membership
        send_mail(event_id=self.request.event.id,
                  to=[self.request.POST["email"]],
                  subject=self.email_subject,
                  body=self.email_message % self.request.POST.dict())

        if form.instance.applied_low_income:
            return redirect(f"./lowincome/{self.request.POST['email']}")

        return ret
