from django.conf.urls import include,url
from . import views

urlpatterns = [
    url(r'^dashboard/$',views.dashboard, name='delivery-boy-dashboard'),
    url(r'^accept-task/(?P<id>\d+)/$', views.acceptTask, name='accept-task'),
    url(r'^decline-task/(?P<id>\d+)/$', views.declineTask, name='decline-task'),
    url(r'^completed-task/(?P<id>\d+)/$', views.completedTask, name='completed-task'),

]