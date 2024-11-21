from django.db import models

# Create your models here.
class Job(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(max_length=1000)
    requierments = models.TextField(max_length=500)
    # category = foreign key with the roles
    budget = models.TextField(max_length=1000)
    # postedBy = foreign key with user posted the job
    status = models.TextField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
