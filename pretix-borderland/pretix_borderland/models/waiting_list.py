from pretix.base.models import LoggedModel
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class WaitingList(LoggedModel):
    event = models.ForeignKey('pretixbase.Event', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="E-mail address")
    first_name = models.CharField(max_length=200, verbose_name="Legal First Name")
    last_name = models.CharField(max_length=200, verbose_name="Legal Last Name")
    dob = models.DateField(verbose_name="Date of Birth")
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "email"], name="register_email_once"),
        ]


@receiver(pre_save, sender=WaitingList)
def pre_save(sender, instance, **kwargs):
    instance.email = instance.email.lower()
