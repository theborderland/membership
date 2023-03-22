from pretix.base.models import LoggedModel
from enum import Enum
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver


class INCOME_CHOICES(Enum):
    NoIncome = 1
    LessThanTenKSEK = 2
    LessThanThirtyKSEK = 3
    LessThanFiftyKSEK = 4
    MoreThanFiftyKSEK = 5
    PreferNotToAnswer = 6

class YES_NO_PREFER_NOT_TO_SAY(Enum):
    Yes = 1
    No = 2
    DontKnow = 3
    PreferNotToSay = 4

class LowIncomeEntry(LoggedModel):
    event = models.ForeignKey('pretixbase.Event', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="E-mail address")
    dob = models.DateField(verbose_name="Date of Birth")
    personal_income = models.IntegerField(choices=[(tag.value, tag.name) for tag in INCOME_CHOICES])
    household_income = models.IntegerField(choices=[(tag.value, tag.name) for tag in INCOME_CHOICES])
    income_source = models.IntegerField(choices=[(tag.value, tag.name) for tag in YES_NO_PREFER_NOT_TO_SAY])
    social_security = models.IntegerField(choices=[(tag.value, tag.name) for tag in YES_NO_PREFER_NOT_TO_SAY])
    timestamp = models.DateTimeField(auto_now_add=True)


@receiver(pre_save, sender=LowIncomeEntry)
def pre_save(sender, instance, **kwargs):
    instance.email = instance.email.lower()