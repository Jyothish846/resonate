"""
URL configuration for resonate project.
...
"""
from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect,render
from django.conf import settings
from django.conf.urls.static import static


def landing_view(request):
    if request.user.is_authenticated:
        return redirect("accounts:profile")
    return render(request, "landing.html")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.urls")),
    path("", landing_view, name="landing"),
]

# In a production environment (DEBUG=False), Django's built-in static handler 
# and media handler is disabled. WhiteNoise handles STATIC. 
# It's generally NOT RECOMMENDED to handle MEDIA files this way in production,
# but if you must, this line is only used for local development (which is correct).
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # The line below is a good fallback for static files in development
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns
    urlpatterns += staticfiles_urlpatterns()