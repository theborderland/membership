from pretix.presale.signals import order_info, front_page_top
from pretix.base.signals import register_html_mail_renderers
# register_global_settings
from django.dispatch import receiver
from django.template.loader import get_template
from datetime import datetime


@receiver(register_html_mail_renderers, dispatch_uid="renderer_borderland")
def register_mail_renderers(sender, **kwargs):
    from .email import BorderlandMailRenderer
    return BorderlandMailRenderer


@receiver(front_page_top)
def lottery_registration(sender, **kwargs):
    """"""
    template = get_template('pretix_borderland/registration_button.html')
    ctx = { "open": datetime.now() < datetime(2020, 1, 29, 18, 0), # TODO
            "event": sender,
            "organizer": sender.organizer }
    return template.render(ctx)


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

