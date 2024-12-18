from django.db import models
# from django.contrib.auth.models import User
from users.models import User
# from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Job(models.Model):
    
    levelsEnum = [('ENTRY', 'ENTRY'), ('INTERMEDIATE', 'INTERMEDIATE'), ('ADVANCED', 'ADVANCED')]
    workModeEnum = [('FULL TIME', 'FULL TIME'), ('PART TIME', 'PART TIME')]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=200, choices=levelsEnum, default='ENTRY')
    workingMode = models.CharField(max_length=200, choices=workModeEnum, default='PART TIME')
    isActive = models.BooleanField()
    # requirements = ArrayField(models.CharField(max_length=200),blank=True,default=list)
    createdAt = models.DateTimeField(auto_now_add=True)
    price=models.FloatField(default=2000.0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'company'})
    location = models.CharField(max_length=200, default='Egypt')
    
    def __str__(self):
        return self.title

class Application(models.Model):
    
    statusEnum = [('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('rejected', 'REJECTED')]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'freelancer'}, related_name='applications_as_freelancer')

    company = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'company'}, default=1, related_name='applications_as_company')
    proposal = models.TextField()
    price = models.IntegerField()
    status = models.CharField(max_length=200, choices=statusEnum, default='pending')
    duration = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)
    due_to = models.DateField(default="18-12-2024")

    def __str__(self):
        return self.proposal

