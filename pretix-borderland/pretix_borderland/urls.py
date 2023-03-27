from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from . import api, views

#handler404 = 'pretix.base.views.errors.page_not_found'

event_patterns = [
    url(r'^register/$', views.Register.as_view(), name="register"),
    url(r'^register/lowincome/(?P<email>[^/]+)/$', views.LowIncome.as_view(), name="LowIncome"),
    url(r'^order/(?P<order>[^/]+)/(?P<secret>[A-Za-z0-9]+)/refund/$',
        views.RefundRequestView.as_view()),
    url(r'^order/(?P<order>[^/]+)/(?P<secret>[A-Za-z0-9]+)/transfer/$',
        views.TransferRequestView.as_view()),
    url(r'^order/(?P<order>[^/]+)/(?P<secret>[A-Za-z0-9]+)/transfer/cancel$',
        views.TransferRequestCancel.as_view(),
        name="transfer.cancel")
]



apirouter = routers.DefaultRouter()
apirouter.register(r'registration', api.RegisterAPIViewSet, basename="RegisterAPI")
apirouter.register(r'refund', api.TransferAPIViewSet)
apirouter.register(r'email', api.EmailViewSet, basename="Email")

urlpatterns = [
    url(r'^api/v1/organizers/(?P<organizer>[^/]+)/events/(?P<event>[^/]+)/', include(apirouter.urls))
]

