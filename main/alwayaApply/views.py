from django.shortcuts import render
from rest_framework.response import Response
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer 
from rest_framework import viewsets
from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from users.models import User


# Create your views here.

class jobView(viewsets.ViewSet):
    
    queryset = Job.objects.all()
    
    def list(self, request):
        serializedData = JobSerializer(self.queryset, many=True)
        return Response(serializedData.data)
    
    def create(self, request):
        serializedData = JobSerializer(data=request.data)
        if serializedData.is_valid():
            serializedData.save()
            return Response(serializedData.data,  status=status.HTTP_201_CREATED)
        return Response(serializedData.errors,  status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = JobSerializer(job, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def destroy(self,request,pk):
        try:
            job = Job.objects.get(id=pk).delete()
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message":"success"})
    

    def retrieve(self,request,pk):
        try:
            job = Job.objects.get(id=pk)
            serializedData = JobSerializer(job)
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializedData.data)
    

class ApplicationView(viewsets.ViewSet):
    
    def list(self, request, pk=None):
        queryset = None
        try:
            user = User.objects.get(id=pk) 
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.role == 'freelancer':  
            queryset = Application.objects.filter(freelancer_id=pk)
        else: 
            queryset = Application.objects.filter(company_id=pk)
        
        serializedData = ApplicationSerializer(queryset, many=True)
        return Response(serializedData.data)
    
    def create(self, request):
        serializedData = ApplicationSerializer(data=request.data)
        if serializedData.is_valid():
            print('is Valid --->>')
            serializedData.save()
            return Response(serializedData.data,  status=status.HTTP_201_CREATED)
        return Response(serializedData.errors,  status=status.HTTP_400_BAD_REQUEST)


