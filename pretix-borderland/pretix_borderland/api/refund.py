from rest_framework import viewsets

from ..models import RefundRequest
from ..serializers import RefundRequest, RefundRequestSerializer
from . import ResultsSetPagination


class RefundRequestAPIViewSet(viewsets.ModelViewSet):
    queryset = RefundRequest.objects.all().order_by('id')
    permission = 'can_view_orders'
    serializer_class = RefundRequestSerializer
    pagination_class = ResultsSetPagination

    def update(self, request, *args, **kwargs):
        self.event.log_action('pretix.plugins.borderland.refund.api_update', data=request.data, auth=request.auth)
        return super.update(self, request, *args, **kwargs)

class TransferAPIViewSet(viewsets.ModelViewSet):
    queryset = RefundRequest.objects.all().order_by('id')
    permission = 'can_view_orders'
    serializer_class = RefundRequestSerializer
    pagination_class = ResultsSetPagination

    def update(self, request, *args, **kwargs):
        self.event.log_action('pretix.plugins.borderland.refund.api_update', data=request.data, auth=request.auth)
        return super.update(self, request, *args, **kwargs)