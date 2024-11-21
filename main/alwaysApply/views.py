from django.shortcuts import render
from.models import Job
from .serializers import JobSerializer
from rest_framework import generics, status
from rest_framework.response import Response
# Create your views here.

class job(generics.ListCreateAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer
