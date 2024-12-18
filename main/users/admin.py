from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'name', 'email', 'role', 'rating', 'is_staff', 'is_active')
    
    # Fields to use in the detail/edit form
    fieldsets = (
        (None, {'fields': ('name', 'email', 'password', 'rating', 'role', 'image')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'groups', 'user_permissions')}),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2', 'role', 'rating', 'image'),
        }),
    )
    
    # Fields for filtering in the admin list view
    search_fields = ('email', 'name')
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions')

# Register the custom user model
admin.site.register(User, UserAdmin)
