from django.urls import path
from .views import (signup_view, login_view, update_profile, get_profile)

urlpatterns = [
    path('signup/', signup_view),
    path('login/', login_view),
    path('profile/update/', update_profile),
    path('profile/<user_email>/', get_profile),
    path('profile/', get_profile),
]
