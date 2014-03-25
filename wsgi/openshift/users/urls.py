from django.conf.urls import patterns, url

from users import views

urlpatterns = patterns('',
	url(r'^registration/$', views.registration, name='registration'),
)
