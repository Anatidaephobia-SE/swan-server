from django.conf.urls import url
from .views import signup_view, login_view, update_profile

urlpatterns = [
    url(r'^signup', signup_view),
    url(r'^login', login_view),
    url(r'^profile', update_profile),
]