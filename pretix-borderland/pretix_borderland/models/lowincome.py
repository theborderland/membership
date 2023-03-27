from pretix.base.models import LoggedModel
from enum import Enum
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class YesNo(Enum):
    No = 1
    Yes = 2


class YesNoDontKnowPreferNotToSay(Enum):
    DontKnow = 1
    No = 2
    Yes = 3
    PreferNotToSay = 4


class LowIncomeEntry(LoggedModel):
    event = models.ForeignKey('pretixbase.Event', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="E-mail address")
    country = models.CharField(max_length=100, verbose_name="Country", default="Borderland")
    has_income = models.IntegerField(choices=[(tag.value, tag.name) for tag in YesNo], default=YesNo.No.value)
    income = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Income", default=0.0)
    last_year_income = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Income last year", default=0.0)
    has_assets = models.IntegerField(choices=[(tag.value, tag.name) for tag in YesNoDontKnowPreferNotToSay], default=YesNoDontKnowPreferNotToSay.DontKnow.value)
    assets = models.DecimalField(max_digits=20, decimal_places=2, verbose_name="Assets", default=0.0)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "email"], name="unique_event_email_combination"),
        ]



@receiver(pre_save, sender=LowIncomeEntry)
def pre_save(sender, instance, **kwargs):
    instance.email = instance.email.lower()
