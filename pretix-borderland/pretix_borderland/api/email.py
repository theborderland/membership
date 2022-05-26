from rest_framework import viewsets
from rest_framework.response import Response

from ..tasks import send_mail


class EmailViewSet(viewsets.GenericViewSet):
    permission = 'can_view_orders'

    def create(self, request, organizer, event):
        self.request.event.log_action('pretix.plugins.borderland.email.send', data=request.data, auth=request.auth)
        d = request.data
        send_mail(event_id=self.request.event.id,
                  to=d['to'],
                  body=d['body'],
                  subject=d['subject']
                  )
        return Response({"result": "ok i guess"})
