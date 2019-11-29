from pretix.base.services.tasks import ProfiledEventTask
from pretix.base.services.mail import SendMailException, mail_send, mail
from pretix.celery_app import app
from email.utils import formataddr

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
