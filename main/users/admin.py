from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # Define the fields to be displayed in the admin panel
    model = User
    list_display = ('id', 'name', 'email', 'role', 'image')  # Customize fields displayed in list view
    list_filter = ('role',)  # Filter by role (company or freelancer)
    search_fields = ('email', 'name')  # Allow search by email or name
    ordering = ('email',)  # Order by email in the admin panel

    # Define which fields should be shown in the detail view
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'role', 'image')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Important Dates', {'fields': ('last_login',)}),
    )
    # Define the fields that should be in the admin form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'name', 'role', 'image'),
        }),
    )
    # Override form to save password correctly (this is already handled by the serializer in your case)
    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.set_password(obj.password)  # Ensure password is hashed on creation
        super().save_model(request, obj, form, change)

# Register the custom User model with the admin
admin.site.register(User, CustomUserAdmin)
