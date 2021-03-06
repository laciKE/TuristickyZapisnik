from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

# include urls patterns and paths from individual apps
urlpatterns = patterns('',
	url(r'^$', 'views.home', name='home'),
	url(r'^dashboard/$', 'views.dashboard', name='dashboard'),
	url(r'^users/', include('users.urls', namespace='users')),
	url(r'^groups/', include('groups.urls', namespace='groups')),
	url(r'^trips/', include('trips.urls', namespace='trips')),
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
