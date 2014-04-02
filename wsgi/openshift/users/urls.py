from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
	url(r'^$', views.index, name='index'),
	url(r'^profile/(?P<username>\w+)/$', views.profile, name='profile'),
	url(r'^registration/$', views.registration, name='registration'),
	url(r'^login/$', views.user_login, name='login'),
	url(r'^logout/$', views.user_logout, name='logout'),
)
