"""adsv1 URL Configuration

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
from os import name
from django.urls.conf import include
import adsv2.views as views
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('oauth/', include('social_django.urls', namespace='social')),

    path('', views.PicListView.as_view(), name='ads_all'),
    path('ad/<int:pk>/', views.AdDetailView.as_view(), name='ad_detail'),
    path('ad/<int:pk>/update', views.AdUpdateView.as_view(), name='ad_edit'),
    path('ad/<int:pk>/delete/', views.AdDeleteView.as_view(), name='ad_delete'),
    path('ad/pic/<int:pk>/', views.stream_file, name='ad_pic'),
    path('ad/create/', views.PicCreateView.as_view(), name='ad_create'),
    path('ad/<int:pk>/comment', views.CommentCreateView.as_view(), name='comment_create'),
    path('comment/<int:pk>/delete', views.CommentDeleteView.as_view(), name='comment_delete'),
    path('ad/<int:pk>/favorite', views.AddFavouriteView.as_view(), name='ad_fav'),
    path('ad/<int:pk>/unfavorite', views.DeleteFavouriteView.as_view(), name='ad_unfav'),
]
