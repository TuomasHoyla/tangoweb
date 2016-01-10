"""tango_with_django_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
#from rango import views

from django.conf import settings

from tastypie.api import Api
#Muista laittaa tähän resurssit APILLE
from rango.api.resources import PageResource, CategoryResource

#Tee api
v1_api = Api(api_name='v1')
#rekisteröi ressut
v1_api.register(PageResource())
v1_api.register(CategoryResource())

urlpatterns = [
    
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('rango.urls')),
    url(r'^rango/', include('rango.urls')), # ADD THIS NEW TUPLE!
    url(r'^api/', include(v1_api.urls)),
    url(r'^api/doc/',
        include('tastypie_swagger.urls', namespace='myapi_tastypie_swagger'),
        kwargs={
          "tastypie_api_module":"rango.category.my_api",
          "namespace":"myapi_tastypie_swagger",
          "version": "0.1"}),
    
#    url(r'^docs/', include('rest_framework_swagger.urls')),
 #   url(r'api/doc/', include('tastypie_swagger.urls', namespace='tastypie_swagger')),

    
]

#if settings.DEBUG:
#    # static files (images, css, javascript, etc.)
#    urlpatterns += patterns('',
#        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
#        'document_root': settings.MEDIA_ROOT}))