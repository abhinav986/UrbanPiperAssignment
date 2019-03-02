from django.conf.urls import include,url
from . import views

urlpatterns = [
    url(r'^dashboard/$',views.dashboard, name='manager-dashboard'),
    url(r'^create-task/$',views.createTask, name='create-task'),
    url(r'^cancel-task/(?P<id>\d+)/$',views.cancelTask, name='cancel-task'),

]