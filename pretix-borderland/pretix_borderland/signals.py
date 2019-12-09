# Register your receivers here

from pretix.presale.signals import order_info
# front_page_top
from django.dispatch import receiver
# register_global_settings


@receiver(order_info)
def orderbleh(sender, order=None, **kwargs):
    #template = get_template('pretix_pages/control_head.html')
    # template.render
    # if order.status = 'p'
    # have warning about transferability
    return "Request refund (SMEP) --- Transfer ticket  "

