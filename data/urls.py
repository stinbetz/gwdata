from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^chooselist/$', views.chooselist, name='chooselist'),
    url(r'^loaddata/$', views.generatelist, name='load'),
]
