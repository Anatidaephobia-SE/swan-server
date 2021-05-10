from django.urls import path
from . import views

urlpatterns = [
    path('create_post/',views.CreatePostView.as_view(), name="createPost"),
    path('update_post/<int:pk>/',views.UpdatePostView.as_view(), name="updatePost"),
    path('single_post/<int:pk>/',views.SinglePostView.as_view(), name="singlePost"),
    path('all_post/<int:pk>/',views.AllPostView.as_view(), name="allPost"),
    path('create_comment/<int:pk>/',views.CreateCommentView.as_view(), name="createComment"),
    path('all_comment/<int:pk>/',views.AllCommentsView.as_view(), name="allComment"),
    path('delete_comment/<int:pk>/',views.DeleteCommentView.as_view(), name="deleteComment"),
]