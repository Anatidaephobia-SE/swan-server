from django.urls import path
from . import views

urlpatterns = [
    path('create_template/',views.CreateTemplatetView.as_view(), name="createTemplate")
    ]