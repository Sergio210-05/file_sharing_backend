"""
URL configuration for file_sharing project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings as st
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('core.urls')),
    path('admin/', admin.site.urls),
    path('api/', include('storage.urls')),
    path('api/accounts/', include('django.contrib.auth.urls')),
    path('api/', include('authentification.urls')),
    path('api/', include('download.urls')),
]

if st.DEBUG:
    urlpatterns += static(st.STATIC_URL, document_root=st.STATIC_ROOT)
    urlpatterns += static(st.MEDIA_URL, document_root=st.MEDIA_ROOT)
