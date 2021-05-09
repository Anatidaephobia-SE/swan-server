"""swan URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
import team.urls as team_urls
import post.urls as post_urls
import filestorage.urls as filestorage_urls
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/socialmedia/', include(('socialmedia.urls', "socialmedia"), namespace="socialmedia-urls")),
    path("", include("django_prometheus.urls"), name="django-prometheus"),
    path('api/v1/users/', include(("users.urls", "users"), namespace="users-urls")),
    path('api/v1/post/', include(("post.urls", "post"), namespace="post-urls")),
    path('api/v1/team/', include(("team.urls", "team"), namespace="team-urls")),
    path('api/v1/filestorage/', include(("filestorage.urls", "filestorage"), namespace="filestorage-urls")),
]

if(settings.DEBUG):
    urlpatterns +=  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
