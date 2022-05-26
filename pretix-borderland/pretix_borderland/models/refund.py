from pretix.base.models import LoggedModel
from i18nfield.fields import I18nCharField, I18nTextField
from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver
#from django_scopes import ScopedManager



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

