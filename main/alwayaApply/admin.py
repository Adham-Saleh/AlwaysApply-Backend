from django.contrib import admin
from .models import Job,Application
# Register your models here.

admin.site.register(Job)
class ApplicationAdmin(admin.ModelAdmin):
    # Fields to display in the admin list view
    list_display = ('id', 'job', 'freelancer', 'company', 'price', 'status', 'duration', 'due_to', 'createdAt')
    
    # Fields to filter in the admin interface
    list_filter = ('status', 'createdAt', 'due_to')
    
    # Fields to search for in the admin interface
    search_fields = ('proposal', 'freelancer__name', 'company__name', 'job__title')
    
    # Fields to include in the detail/edit view
    fieldsets = (
        (None, {
            'fields': ('job', 'freelancer', 'company', 'proposal', 'price', 'status', 'duration', 'due_to')
        }),
    )

admin.site.register(Application, ApplicationAdmin)
