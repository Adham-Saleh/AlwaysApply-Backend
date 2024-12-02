from django.db import models
from django.utils import timezone

class Employer(models.Model):
    PLANS_CHOICES=[
        ('standard','standard'),
        ('premium','premium'),
    ]

    
    name=models.CharField(max_length=250)
    location=models.CharField(max_length=255)
    verified=models.BooleanField(default=False)
    certification=models.DateField(null=True,blank=True)
    plans=models.CharField(max_length=25,default='standard',choices=PLANS_CHOICES)
    rates=models.DecimalField(max_digits=5,decimal_places=2,default=5.00)
    connects=models.IntegerField(default=0)
    rating=models.FloatField(default=0.0)

    def post_offer(self,title,description,budget):
        job=job.objects.create(
            employer=self,
            title=title,
            description=description,
            budget=budget
        )
        return job

    def accept_freelancer(self,application):
        if application.job.employer!=self:
            raise ValueError('You are not allowed to accept this application')
        application.accept()
        return application
    
    def reject_freelancer(self,application,reason):
        if application.job.employer!=self:
            raise ValueError('You are not allowed to reject this application')
        application.reject(reason)
        return application
    
    def renew_job(self,job):
        if job.employer!=self:
            raise ValueError('You are not allowed to renew this application')
        job.renew()
        return job

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if self.rating==5.0 and self.jobs.count()>100:
            self.verified=True
        super().save(*args,**kwargs)
    

class Job(models.Model):
    employer=models.ForeignKey(Employer,on_delete=models.CASCADE,related_name='jobs')
    title=models.CharField(max_length=250)
    description=models.TextField()
    budget=models.FloatField()
    created_at=models.DateTimeField(auto_now_add=True)
    renewed_at=models.DateTimeField(null=True,blank=True)
    isActive=models.BooleanField(default=True)
    connects_required = models.IntegerField(default=10)

    def renew(self):
        self.renewed_at=timezone.now()
        self.save()
    
    def __str__(self):
        return self.title
    

class Freelancer(models.Model):
    
    name=models.CharField(max_length=250)
    connects=models.IntegerField(default=10)
    rating=models.FloatField(default=0.0)

    def apply_for_job(self,job,cover_letter):
        if self.connects<job.connects_required:
            raise ValueError("Not enough connects to apply for this job.")
        applications=Application.objects.create(
            job=job,
            cover_letter=cover_letter,
            freelancer=self,
            connects=job.connects_required
        )
        self.connects-=job.connects_required
        self.save()
        return applications

    def __str__(self):
        return self.name

from django.db import models

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    freelancer = models.ForeignKey(Freelancer, on_delete=models.CASCADE, related_name='applications')
    isAccepted = models.BooleanField(default=False)
    isPending = models.BooleanField(default=True)
    connects = models.IntegerField()
    cover_letter = models.TextField(null=True, blank=True)
    rejection_reason = models.TextField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.connects:
            self.connects = self.job.connects_required
        super().save(*args, **kwargs)
        print(args,kwargs)

    def accept(self):
        self.isAccepted=True
        self.isPending=False
        self.save()
    
    def reject(self,reason):
        self.isAccepted=False
        self.isPending=False
        self.rejection_reason=reason
        self.save()

    def __str__(self):
        return f"Application {self.id} for {self.job.title} by {self.freelancer.name}"
    
class Offer(models.Model):
    
    job=models.ForeignKey(Job,on_delete=models.CASCADE,related_name='offer')
    isDone=models.BooleanField(default=False)

    def mark_completed(self):
        self.isDone=True
        self.save()

    def __str__(self):
        return f"Offer for {self.job.title} is ({'Done' if self.isDone else 'Pending'})"
    
