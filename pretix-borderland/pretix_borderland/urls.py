from django.conf.urls import url
from django.urls import include, path
from rest_framework import routers

from . import views

event_patterns = [
    url(r'^register/$', views.RegisterForm.as_view()),
]

apirouter = routers.DefaultRouter()
apirouter.register(r'registration', views.RegisterAPIViewSet)

urlpatterns = [
    url(r'^api/v1/(?P<organizer>[^/]+)/events/(?P<event>[^/]+)/', include(apirouter.urls))
]

