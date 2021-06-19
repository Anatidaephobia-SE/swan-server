from django.urls import path
from . import views

urlpatterns = [
    path('create_template/',views.CreateTemplatetView.as_view(), name="createTemplate"),
    path('update_template/<int:pk>/',views.UpdateTemplateView.as_view(), name="updateTemplate"),
    path('single_template/<int:pk>/',views.SingleTemplateView.as_view(), name="singleTemplate"),
    path('all_template/<int:pk>/',views.AllTemplateView.as_view(), name="allTemplate"),
    ]