from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from . import views

event_patterns = [
    url(r'^register/$', views.RegisterForm.as_view(), name="register"),
    url(r'^order/(?P<order>[^/]+)/(?P<secret>[A-Za-z0-9]+)/refund/$',
        views.RefundRequestView.as_view()),
    url(r'^order/(?P<order>[^/]+)/(?P<secret>[A-Za-z0-9]+)/transfer/$',
        views.TransferRequestView.as_view()),
    url(r'^order/(?P<order>[^/]+)/(?P<secret>[A-Za-z0-9]+)/transfer/cancel$',
        views.TransferRequestCancel.as_view(),
        name="transfer.cancel")
]



apirouter = routers.DefaultRouter()
apirouter.register(r'registration', views.RegisterAPIViewSet)
apirouter.register(r'refund', views.TransferAPIViewSet)
apirouter.register(r'email', views.EmailViewSet, basename="Email")

urlpatterns = [
    url(r'^api/v1/organizers/(?P<organizer>[^/]+)/events/(?P<event>[^/]+)/', include(apirouter.urls))
]

