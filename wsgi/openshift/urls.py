from django.conf.urls import patterns, include, url
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
	url(r'^$', 'views.home', name='index'),
	url(r'^home/$', 'views.home', name='home'),
	url(r'^users/', include('users.urls', namespace='users')),
	url(r'^groups/', include('groups.urls', namespace='groups')),
	url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
	#urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT, show_indexes=True)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT, show_indexes=True)
