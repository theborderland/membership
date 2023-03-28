from pretix.base.services.tasks import ProfiledEventTask
from pretix.base.services.mail import SendMailException, mail_send, mail
from pretix.celery_app import app

from email.utils import formataddr
from .controller import is_eligible_for_low_income
from .models import LowIncomeEntry, LotteryEntry

def send_mail(*args, **kwargs):
    send_mail_.apply_async(args=args, kwargs=kwargs)

@app.task(base=ProfiledEventTask)
def send_mail_(to, subject, body, event_id=None,event=None):
    # TODO defaults if event == None
    renderer = event.get_html_mail_renderer()
    sender_mail = event.settings.get('mail_from')
    sender_name = event.settings.mail_from_name or str(event.name)
    sender = formataddr((sender_name, sender_mail))
    signature = ""
    renderer = event.get_html_mail_renderer()
    body_html = renderer.render(body, signature, subject, order=None, position=None)
    mail_send(to=to,
              subject=subject,
              body=body,
              html=body_html,
              sender=sender)

@app.task(base=ProfiledEventTask)
def update_low_income_status(organizer, event, force=False):
    """ Check if the low income application is valid and if eligible for a low income. This task may come in handy
    when we change the algorithm to gauge eligibility. """
    for entry in LowIncomeEntry.objects.filter(event__organizer=organizer, event__slug=event):
        if force:
            lottery_entry = LotteryEntry.objects.filter(event=entry.event, email=entry.email).first()
            lottery_entry.low_income = is_eligible_for_low_income(entry)
        else:
            if is_eligible_for_low_income(entry):
                lottery_entry = LotteryEntry.objects.filter(event=entry.event, email=entry.email).first()
                lottery_entry.low_income = True
