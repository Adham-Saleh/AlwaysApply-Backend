from rest_framework import serializers
from .models import Job, Application
from users.models import User

class JobSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = ['id', 'user', 'user_details', 'title', 'description', 'level', 'workingMode', 'isActive', 'createdAt', 'price', 'location']
        read_only_fields = ['user_details']

    def get_user_details(self, obj):
        user = obj.user
        return {
            "id":user.id,
            "name": user.name,
            "email": user.email,
            "role": user.role
        }



class ApplicationSerializer(serializers.ModelSerializer):
    job = serializers.PrimaryKeyRelatedField(queryset=Job.objects.all())
    freelancer = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='freelancer'))
    company = serializers.PrimaryKeyRelatedField(queryset=User.objects.filter(role='company'))

    class Meta:
        model = Application
        fields = '__all__'
    
    def create(self, validated_data):
        job = validated_data.get('job')
        freelancer = validated_data.get('freelancer')
        company = validated_data.get('company', None)

        if not company:
            company = job.user

        application = Application.objects.create(
            job=job,
            freelancer=freelancer,
            company=company,
            proposal=validated_data.get('proposal'),
            price=validated_data.get('price'),
            duration=validated_data.get('duration'),
            status=validated_data.get('status', 'pending')
        )
        return application

    
from rest_framework import serializers
from .models import Application
from users.serializers import UserSerializer

class DashboardSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)  # Include full job details
    freelancer_name = serializers.CharField(source="freelancer.name", read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'freelancer_name', 'proposal', 'price', 'status', 'duration', 'createdAt']

