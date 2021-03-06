from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext as _
from .models import User


class UserAdmin(BaseUserAdmin):
    ordering = ['id']
    list_display = ('email', 'name', 'is_active')
    fieldsets = (
        (_('User data'), {'fields': ('email', 'password')}),
        (_('Personal info'), {'fields': ('name',)}),
        (
            _('Permissions'), {
                'fields': ('is_active', 'is_staff', 'is_superuser')}
        ),
        (_('Important dates'), {'fields': ('last_login',)}),
    )
    search_fields = ('email', 'name')

    add_fieldsets = (
        (_('Basic user info'), {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2')
        }),
    )


admin.site.register(User, UserAdmin)
