from django.urls import include, path

from . import views


urlpatterns = [
    path('', views.home , name='index'),
    path('home/', views.home , name='home-page'),
    path('about/', views.about , name='about-page'),
]
