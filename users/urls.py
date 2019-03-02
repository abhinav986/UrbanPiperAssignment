from django.contrib import admin
from django.urls import path
from django.conf.urls import include,url
from . import views

urlpatterns = [
    url(r'^$', views.homePage, name="homepage"),
    url(r'^login/$', views.custom_login, name="users-login"),
    url(r'^custom_logout/$', views.custom_logout, name="users-logout"),
    url(r'^createUser/$', views.createUser, name="create-user"),
    url(r'^api/$', views.api, name="create-api"),

]