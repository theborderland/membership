from django.db import transaction
from django.views.generic import View, UpdateView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.shortcuts import redirect
from django import forms
from pretix.presale.views.order import OrderDetailMixin

from ..models import RefundRequest


class RefundRequestView(SuccessMessageMixin, OrderDetailMixin, UpdateView):
    template_name = "pretix_borderland/refund_request.html"
    model = RefundRequest
    fields = []

    def get_success_url(self):
        return self.get_order_url()

    def get_error_url(self):
        return self.get_order_url()

    def get_success_message(self, value):
        return 'Refund request sent.'

    def get_object(self, queryset=None):
        obj, created = self.model.objects.get_or_create(order=self.order)
        return obj

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['order'] = self.order
        return ctx

    @transaction.atomic
    def form_valid(self, form):
        if self.order.status != "p":
            raise forms.ValidationError("Can only cancel paid orders!")
        form.instance.status = "p"
        self.order.log_action('pretix.plugins.borderland.refund.request', data=form)
        ret = super().form_valid(form)
        return ret


class TransferRequestView(RefundRequestView):
    template_name = "pretix_borderland/transfer_request.html"
    fields = ["target", "user_comment"]

    def get_success_message(self, value):
        return 'Transfer request sent!'


class TransferRequestCancel(SuccessMessageMixin, OrderDetailMixin, View):
    def post(self, request, *args, **kwargs):
        req, created = RefundRequest.objects.get_or_create(order=self.order)
        if req.status == 'p':
            req.status = 'c'
            req.save()
            self.order.log_action('pretix.plugins.borderland.refund.cancel', data=form)
            messages.add_message(request, messages.SUCCESS, "Transfer request cancelled!")
        return redirect(self.get_order_url())
