from pretix.base.models import LoggedModel
from i18nfield.fields import I18nCharField, I18nTextField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
#from django_scopes import ScopedManager



class LotteryEntry(LoggedModel):
    event = models.ForeignKey('pretixbase.Event', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="E-mail address")
    first_name = models.CharField(max_length=200,verbose_name="Legal First Name")
    last_name = models.CharField(max_length=200,verbose_name="Legal Last Name")
    dob = models.DateField(verbose_name="Date of Birth")
    timestamp = models.DateTimeField(auto_now_add=True)
    vouchers = models.ManyToManyField('pretixbase.Voucher')
    ip = models.CharField(max_length=200, blank=True)
    cookie = models.CharField(max_length=2048, blank=True)
    browser = models.CharField(max_length=2048, blank=True)
    applied_low_income = models.BooleanField(default=False, verbose_name="Applied to a low income membership")
    low_income = models.BooleanField(default=False, verbose_name="Apply for low income membership")

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "email"], name="register_email_once"),
#            models.UniqueConstraint(fields=["event", "first_name", "last_name", "dob"],
#                                    name="register_person_once")
        ]

@receiver(pre_save, sender=LotteryEntry)
def pre_save(sender, instance, **kwargs):
    instance.email = instance.email.lower()