# gas_utility/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('customer_portal/', include('customer_portal.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
