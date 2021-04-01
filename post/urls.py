from django.urls import path
from . import views

urlpatterns = [
    path('create_post',views.CreatePostView.as_view()),
    path('update_post/<int:pk>/',views.UpdatePostView.as_view()),
]