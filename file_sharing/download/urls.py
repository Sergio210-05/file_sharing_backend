from django.urls import path

from . import views


urlpatterns = [
    path('download/<str:storage_title>', views.file_download, name='api-download'),
]
