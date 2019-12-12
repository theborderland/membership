from pretix.base.models import LoggedModel
from i18nfield.fields import I18nCharField, I18nTextField
from django.db import models
#from django_scopes import ScopedManager

class LotteryEntry(LoggedModel):
    event = models.ForeignKey('pretixbase.Event', on_delete=models.CASCADE)
    email = models.EmailField(verbose_name="E-mail")
    first_name = models.CharField(max_length=200,verbose_name="Real First Name")
    last_name = models.CharField(max_length=200,verbose_name="Real Last Name")
    dob = models.DateField(verbose_name="Date of Birth")
    timestamp = models.DateTimeField(auto_now_add=True)
    vouchers = models.ManyToManyField('pretixbase.Voucher')
    ip = models.CharField(max_length=200, blank=True)
    cookie = models.CharField(max_length=200, blank=True)
    browser = models.CharField(max_length=200, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["event", "email"], name="register_email_once"),
            models.UniqueConstraint(fields=["event", "first_name", "last_name", "dob"],
                                    name="register_person_once")
        ]



class RefundRequest(LoggedModel):
    order = models.ForeignKey('pretixbase.Order', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('p', 'Pending'),
                                                      ('c', 'Cancelled'),
                                                      ('d', 'Done'),
                                                      ('i', 'In Progress'),
                                                      ('r', 'Rejected')])
    vouchers = models.ManyToManyField('pretixbase.Voucher')
    # for directed transfers
    target = models.EmailField(verbose_name="Target E-mail", blank=True)
    user_comment = models.TextField(blank=True)
    authorized = models.BooleanField(null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order"],
                                    condition=models.Q(status='p'),
                                    name="only_one_pending")
        ]


