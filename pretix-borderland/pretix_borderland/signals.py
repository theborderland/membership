from pretix.presale.signals import order_info, front_page_top
# register_global_settings
from django.dispatch import receiver
from django.template.loader import get_template
from datetime import datetime

@receiver(front_page_top)
def lottery_registration(sender, **kwargs):
    """"""
    template = get_template('pretix_borderland/registration_button.html')
    ctx = { "open": datetime.now() < datetime(2020, 2, 1, 4, 0), # TODO
            "event": sender,
            "organizer": sender.organizer }
    return template.render(ctx)


@receiver(order_info)
def order_transfer_request(sender, order=None, **kwargs):
    """ Transfer request """
    # Just skipping the UI part is fine for disabling transfers, if a user were
    # to find the URL and submit a request nothing would happen as the actual
    # background jobs don't run

    # if order.status = 'p'
    # have warning about transferability
    # return "Request refund (SMEP) --- Transfer ticket  "

