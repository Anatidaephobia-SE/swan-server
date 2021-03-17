from django.conf.urls import url
from .views import signup_view

urlpatterns = [
    url(r'^signup', signup_view),
]