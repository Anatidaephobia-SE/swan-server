from django.urls import path
from . import views

urlpatterns = [
    path('create_card/',views.CreateCardView.as_view(), name="createCard"),
    path('all_card/',views.AllCardstView.as_view(), name="allCard"),
]