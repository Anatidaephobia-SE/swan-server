from django.urls import path
from . import views

urlpatterns = [
    path('upload/',views.UploadFileView.as_view(), name="upload"),
    path('single_file/',views.SingleFileView.as_view(), name="single_file"),
    path('all_media/',views.AllMediaView.as_view(),name="all_media"),
    path('delete_media/',views.DeleteMediaView.as_view(),name="Delete_media"),
]

