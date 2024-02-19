import os

from pretix.presale.signals import front_page_top
from pretix.base.signals import register_html_mail_renderers
from django.dispatch import receiver
from django.template.loader import get_template
from django.db.models.signals import post_save

from .models import LowIncomeEntry
from .controller import is_eligible_for_low_income

@receiver(register_html_mail_renderers, dispatch_uid="renderer_borderland_classic")
def register_mail_renderer_classic(sender, **kwargs):
    from .templates.email import BorderlandMailRendererClassic
    return BorderlandMailRendererClassic

@receiver(register_html_mail_renderers, dispatch_uid="renderer_borderland_2024")
def register_mail_renderer_2024(sender, **kwargs):
    from .templates.email import BorderlandMailRenderer2024
    return BorderlandMailRenderer2024


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
    if kwargs['created'] and is_eligible_for_low_income(kwargs['instance']):
        # open model and mark as eligible
        entry = LowIncomeEntry.objects.filter(event=kwargs['instance'].event, email=kwargs['instance'].email)
        entry.low_income = True


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
