import re

from rest_framework import viewsets
from rest_framework.response import Response
from pretix.base.models.orders import Order
from pretix.base.models.event import Event

from ..serializers import LotteryEntry, LotteryEntrySerializer
from . import ResultsSetPagination


class RegisterAPIViewSet(viewsets.ModelViewSet):
    permission = 'can_view_orders'
    serializer_class = LotteryEntrySerializer
    pagination_class = ResultsSetPagination

    def get_queryset(self):
        event = re.findall(r"events/([^.]*)/registration", self.request.path)
        if not event:
            return Response({'error': 'invalid request, event not found'}, status=401)

        events = Event.objects.filter(slug=event[0])
        if not events:
            return Response({'error': 'event not found'}, status=404)
        event = events[0]

        registered_users = LotteryEntry.objects.filter(event_id=event).order_by('id')
        if "without-membership" in self.request.query_params:
            registered_users_without_membership = []
            for reg_user in registered_users:
                orders = Order.objects.filter(email=reg_user.email, event=event)
                if not orders:
                    registered_users_without_membership.append(reg_user)
            return registered_users_without_membership
        return registered_users

    # TODO: fix update (was broken since the start)
    def update(self, request, pk=None):
        self.event.log_action('pretix.plugins.borderland.registration.api_update', data=request.data, auth=request.auth)
        return super.update(self, request, *args, **kwargs)