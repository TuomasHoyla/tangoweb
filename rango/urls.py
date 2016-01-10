from django.conf.urls import patterns, url
#from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from rango import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    url(r'^about', views.about, name='about'),
    url(r'^add_category/$', views.add_category, name='add_category'), # NEW MAPPING!
    url(r'^categories', views.categories, name='categories'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
    url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page, name='add_page'), 
    #vähän eri tavalla taalla tehty http://www.tangowithdjango.com/book17/chapters/login.html
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^restricted/', views.restricted, name='restricted'),
    url(r'^logout/$', views.user_logout, name='logout')
                      )  # New!
 #   url(r'^time/$', views.current_datetime),
#    url(r'^time/plus/(\d{1,2})/$', views.hours_ahead),
#    url(r'^time/plus/(\d{1,2})/(\d{1,2})/$', views.min_ahead))

urlpatterns += staticfiles_urlpatterns()