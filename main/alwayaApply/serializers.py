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

    freelancer_details = serializers.SerializerMethodField()
    company_details = serializers.SerializerMethodField()
    job_details = serializers.SerializerMethodField()

    class Meta:
        model = Application
        fields = ['id', 'job','job_details', 'freelancer', 'freelancer_details', 'company', 'company_details', 'proposal', 'price', 'status', 'duration', 'createdAt','due_to']
    
    def get_freelancer_details(self, obj):
        freelancer = obj.freelancer
        return {
            "id": freelancer.id,
            "name": freelancer.name,
            "email": freelancer.email,
            "role": freelancer.role,
            "rating":freelancer.rating
        }
    
    def get_company_details(self, obj):
        company = obj.company
        return {
            "id": company.id,
            "name": company.name,
            "email": company.email,
            "role": company.role
        }
    def get_job_details(self, obj):
        job = obj.job
        return {
            "id": job.id,
            "title": job.title,
            "description": job.description,
            "level": job.level,
            "workingMode":job.workingMode,
            "price":job.price,
            "isActive":job.isActive,
            "createdAt":job.createdAt,
            "location":job.location
        }
    
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
            status=validated_data.get('status', 'pending'),
            due_to=validated_data.get('due_to')
        )
        return application


class DashboardSerializer(serializers.ModelSerializer):
    job = JobSerializer(read_only=True)
    freelancer_name = serializers.CharField(source="freelancer.name", read_only=True)

    class Meta:
        model = Application
        fields = ['id', 'job', 'freelancer_name', 'proposal', 'price', 'status', 'duration', 'createdAt']

