from django.conf.urls import patterns, url

from trips import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^create/$', views.create, name='create'),
	url(r'^view/(?P<tripid>\d+)$', views.view, name='view'),
	url(r'^delete/(?P<tripid>\d+)$', views.delete, name='delete'),
	url(r'^edit/(?P<tripid>\d+)/$', views.edit, name='edit'),
)
