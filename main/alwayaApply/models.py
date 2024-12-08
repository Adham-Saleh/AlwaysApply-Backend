from django.db import models
# from django.contrib.auth.models import User
from users.models import User
# from django.contrib.postgres.fields import ArrayField

# Create your models here.

class Job(models.Model):
    
    levelsEnum = [('entry', 'ENTRY'), ('intermediate', 'INTERMEDIATE'), ('advanced', 'ADVANCED')]
    workModeEnum = [('full', 'FULL TIME'), ('part', 'PART TIME')]
    
    title = models.CharField(max_length=200)
    description = models.TextField()
    level = models.CharField(max_length=200, choices=levelsEnum, default='entry')
    workingMode = models.CharField(max_length=200, choices=workModeEnum, default='part')
    isActive = models.BooleanField()
    # requirements = ArrayField(models.CharField(max_length=200),blank=True,default=list)
    createdAt = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'company'})
    
    def __str__(self):
        return self.title

class Application(models.Model):
    
    statusEnum = [('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('rejected', 'REJECTED')]

    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    freelancer = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'freelancer'}, related_name='applications_as_freelancer')
    
    # Company field, referencing users with the 'company' role
    company = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': 'company'}, default=1, related_name='applications_as_company')
    proposal = models.TextField()
    price = models.IntegerField()
    status = models.CharField(max_length=200, choices=statusEnum, default='pending')
    duration = models.IntegerField()
    createdAt = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.proposal

