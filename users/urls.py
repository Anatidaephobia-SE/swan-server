from django.urls import path
from .views import (signup_view, login_view, update_profile, get_profile)

urlpatterns = [
    path('signup/', signup_view, name="signup"),
    path('login/', login_view, name="login"),
    path('profile/update/', update_profile, name="updateProfile"),
    path('profile/<user_email>/', get_profile, name="getProfileByEmail"),
    path('profile/', get_profile, name = "getProfile"),
]
