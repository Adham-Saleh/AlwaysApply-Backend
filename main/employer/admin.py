from django.contrib import admin
from .models import Employer, Job, Freelancer, Application, Offer

admin.site.register(Employer)
admin.site.register(Job)
admin.site.register(Freelancer)
admin.site.register(Application)
admin.site.register(Offer)