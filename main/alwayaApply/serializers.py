from rest_framework import serializers
from .models import Job, Application
from users.models import User
from users.serializers import UserSerializer

class JobSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    class Meta: 
        model = Job
        fields = '__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer() 
    freelancer = UserSerializer()
    company = UserSerializer()
    class Meta:
        model = Application
        fields = '__all__'