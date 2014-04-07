from django.conf.urls import patterns, url

from groups import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^create/$', views.create, name='create'),
	url(r'^delete/(?P<groupid>\d+)$', views.delete, name='delete'),
	url(r'^edit/(?P<groupid>\d+)/$', views.edit, name='edit'),
	url(r'^edit/(?P<groupid>\d+)/remove/(?P<userid>\d+)/$', views.remove_user, name='remove_user'),
)
