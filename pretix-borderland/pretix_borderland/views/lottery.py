import os

from django.db import transaction, IntegrityError
from django.views.generic import CreateView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render
from pretix.helpers.http import get_client_ip

from ..tasks import send_mail
from ..forms import RegisterForm


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
    """  # TODO

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data()
        # TODO move to config
        ctx.update({"open": bool(os.getenv("ENABLE_LOTTERY_REGISTRATION"))})
        return ctx

    def form_valid(self, form):
        if form.instance.dob.strftime("%Y-%m-%d") != self.request.POST.get("dob_again",
                                                                           "") or form.instance.dob.year > 2008:
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
        send_mail(event_id=self.request.event.id,
                  to=[self.request.POST["email"]],
                  subject=self.email_subject,
                  body=self.email_message % self.request.POST.dict())
        return ret
