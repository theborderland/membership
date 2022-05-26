from rest_framework.pagination import PageNumberPagination

class ResultsSetPagination(PageNumberPagination):
    page_size = 500
    page_size_query_param = 'page_size'
    max_page_size = 4000

from .email import EmailViewSet
from .lottery import RegisterAPIViewSet
from .refund import RefundRequestAPIViewSet, TransferAPIViewSet