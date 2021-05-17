from django.urls import path
from . import views

urlpatterns = [
    path('create_card/',views.CreateCardView.as_view(), name="createCard"),
    path('all_card/<int:pk>/',views.AllCardstView.as_view(), name="allCard"),
    path('Delete_Card/<int:pk>/',views.DeleteCardView.as_view(), name="DeleteCard"),
    path('Move_Card/<int:pk>/',views.MoveCardView.as_view(), name="MoveCard"),
]