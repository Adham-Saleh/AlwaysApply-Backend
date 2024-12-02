from rest_framework import serializers
from .models import Application,Job,Freelancer,Employer,Offer


class EmployerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Employer
        fields='__all__'

class JobSerializer(serializers.ModelSerializer):
    employer=EmployerSerializer()
    class Meta:
        model=Job
        fields='__all__'

class FreelancerSerializer(serializers.ModelSerializer):
    class Meta:
        model=Freelancer
        fields='__all__'

class ApplicationSerializer(serializers.ModelSerializer):
    job = JobSerializer()  # Serialize the related job
    freelancer = FreelancerSerializer()  # Serialize the related freelancer

    class Meta:
        model = Application
        fields = '__all__'


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model=Offer
        fields='__all__'