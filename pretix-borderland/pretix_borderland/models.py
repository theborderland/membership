from pretix.base.models import LoggedModel
from i18nfield.fields import I18nCharField, I18nTextField
from django.db import models

class LotteryForm(LoggedModel):
    event = models.ForeignKey('pretixbase.Event', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="E-mail")
    first_name = models.CharField(max_length=200,verbose_name="Legal First Name")
    last_name = models.CharField(max_length=200,verbose_name="Legal Last Name")
    dob = models.DateField(verbose_name="Date of Birth")
    timestamp = models.DateTimeField(auto_now_add=True)
    voucher = models.PositiveIntegerField(blank=True,null=True)
    ip = models.CharField(max_length=200, blank=True)
    cookie = models.CharField(max_length=200, blank=True)
    browser = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "email"], name="register_email_once"),
            models.UniqueConstraint(fields=["event", "first_name", "last_name", "dob"],
                                    name="register_person_once")
        ]

