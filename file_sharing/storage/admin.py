from django.contrib import admin

from storage.models import File


@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ['id', 'original_title', 'storage_title', 'size',
                    'upload_date', 'last_download', 'owner',
                    'link', ]
    list_filter = ['owner', ]
