from django.conf import settings
from django.conf.urls import handler404, handler500
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

handler404 = 'apps.recipes.views.page_not_found'  # noqa
handler500 = 'apps.recipes.views.server_error' # noqa


urlpatterns = [
    path('auth/', include('apps.users.urls'),),
    path('auth/', include('django.contrib.auth.urls')),
    path('about/', include('apps.about.urls')),
    path('admin/', admin.site.urls),
    path('', include('apps.recipes.urls')),
]


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)

    urlpatterns += (path('__debug__/', include(debug_toolbar.urls)),)
