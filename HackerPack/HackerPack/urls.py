from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.contrib import admin



urlpatterns = [
	url(r'', include('src.urls', namespace='src')),

	# Required for all-auth
	url(r'^accounts/', include('allauth.urls')),

	url(r'^admin/', admin.site.urls),

	url(r'^notifications/', include('notify.urls', 'notifications')),
]

if settings.DEBUG:
	urlpatterns += static(
		settings.MEDIA_URL,
		document_root=settings.MEDIA_ROOT
	)

	urlpatterns += static(
		settings.STATIC_URL,
		document_root=settings.STATIC_ROOT
	)