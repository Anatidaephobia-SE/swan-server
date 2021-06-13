from django.urls import path
from . import views

urlpatterns = [
    path('create_template/',views.CreateTemplatetView.as_view(), name="createTemplate"),
    path('update_template/<int:pk>/',views.UpdateTemplateView.as_view(), name="updateTemplate"),
    ]