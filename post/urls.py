from django.urls import path
from . import views

urlpatterns = [
    path('create_post',views.CreatePostView.as_view()),
    path('update_post/<int:pk>/',views.UpdatePostView.as_view()),
    path('single_post/<int:pk>/',views.SinglePostView.as_view()),
    path('all_post/',views.AllPostView.as_view()),
    path('create_comment/<int:pk>/',views.CreateCommentView.as_view()),
    path('all_comment/<int:pk>/',views.AllCommentsView.as_view()),
    path('delete_comment/<int:pk>/',views.DeleteCommentView.as_view()),
]