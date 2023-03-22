import os

from pretix.presale.signals import front_page_top
from pretix.base.signals import register_html_mail_renderers
from django.dispatch import receiver
from django.template.loader import get_template
from django.db.models.signals import post_save

from models import LowIncomeEntry
from controller import IsEligibleForLowIncome

@receiver(register_html_mail_renderers, dispatch_uid="renderer_borderland")
def register_mail_renderers(sender, **kwargs):
    from .templates.email import BorderlandMailRenderer
    return BorderlandMailRenderer


@receiver(front_page_top)
def lottery_registration(sender, **kwargs):
    """"""
    template = get_template('pretix_borderland/registration_button.html')
    ctx = { "open": bool(os.getenv("ENABLE_LOTTERY_REGISTRATION")),
            "low_income_enabled": bool(os.getenv("ENABLE_LOTTERY_LOW_INCOME")),
            "event": sender,
            "organizer": sender.organizer }
    return template.render(ctx)

@receiver(post_save, sender=LowIncomeEntry, dispatch_uid='low_income_application')
def low_income_application(sender, **kwargs):
    # check if the application is valid and if eligible for a low income
    if kwargs['created'] and IsEligibleForLowIncome(kwargs['instance']):
        # open model and mark as eligible
        entry = LowIncomeEntry.object.filter(email=kwargs['instance'].email, event=kwargs['instance'].event)
        entry.low_income = True
        entry.save()


#@receiver(order_info)
#def order_transfer_request(sender, order=None, **kwargs):
    """ Transfer request """
    # Just skipping the UI part is fine for disabling transfers, if a user were
    # to find the URL and submit a request nothing would happen as the actual
    # background jobs don't run

 #   if order.status == 'p':
 #       template = get_template('pretix_borderland/order_info.html')
 #       return template.render()
    # have warning about transferability
0
