from django.conf.urls import patterns, url

from trips import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^public/$', views.public, name='public'),
	url(r'^create/$', views.create, name='create'),
	url(r'^view/(?P<tripid>\d+)$', views.view, name='view'),
	url(r'^delete/(?P<tripid>\d+)$', views.delete, name='delete'),
	url(r'^edit/(?P<tripid>\d+)/$', views.edit, name='edit'),
	url(r'^share/(?P<tripid>\d+)/$', views.share, name='share'),
	url(r'^share/(?P<tripid>\d+)/remove/(?P<userid>\d+)/$', views.remove_user, name='remove_user'),
	url(r'^share/(?P<tripid>\d+)/add/(?P<userid>\d+)/$', views.add_user, name='add_user'),	
	url(r'^share/(?P<tripid>\d+)/removegroup/(?P<groupid>\d+)/$', views.remove_group, name='remove_group'),
	url(r'^share/(?P<tripid>\d+)/addgroup/(?P<groupid>\d+)/$', views.add_group, name='add_group'),	
)
