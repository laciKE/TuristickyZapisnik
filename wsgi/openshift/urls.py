from django.conf.urls import patterns, include, url
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'views.home', name='home'),
	url(r'^users/', include('users.urls', namespace='users')),
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT, 'show_indexes':True}),
	)

	urlpatterns += patterns('',
		(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes':True}),
	)
