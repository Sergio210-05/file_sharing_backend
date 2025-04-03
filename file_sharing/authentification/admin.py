from django.contrib import admin

from authentification.models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'full_name', 'password', 'email',
                    'folder_path', 'is_staff', 'is_superuser', ]
    list_filter = ['is_staff',  'is_superuser', ]


# admin.site.register(User, UserAdmin)
