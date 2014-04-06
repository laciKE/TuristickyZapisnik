from django.conf.urls import patterns, url

from groups import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	#url(r'^edit/(?P<groupid>\d+)/$', views.edit, name='edit'),
	url(r'^create/$', views.create, name='create'),
	url(r'^delete/(?P<groupid>\d+)$', views.delete, name='delete'),
)
