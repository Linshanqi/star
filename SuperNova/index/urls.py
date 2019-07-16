from django.conf.urls import url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from .views import *

urlpatterns = [
    url(r'^upload/',upload_image,name='upload'),
    url(r'^show', show_image,name='sh'),
    url(r'^dete1/',dete1,name='det'),
    url(r'^result',result,name='res'),
    url(r'^index',index_views,name='index'),
    url(r'^contact',contact_views,name='contact'),
    url(r'^about',about_views,name='about'),
    url(r'^project',project_views,name='project'),
    url(r'^single',single_views,name='single'),
]
