from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.views.decorators.cache import cache_control
from django.contrib.staticfiles.views import serve


from . import views as homepage_views
from entries import urls as entries_urls
from gitload import urls as gitload_urls

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', homepage_views.LandingView.as_view(), name='landing'),
    path('entries/', include(entries_urls)),
    path('gitload/', include(gitload_urls)),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += static(
        settings.STATIC_URL,
        view=cache_control(max_age=settings.CACHE_CONTROL_MAX_AGE)(serve),
        document_root=settings.STATIC_ROOT
    )
