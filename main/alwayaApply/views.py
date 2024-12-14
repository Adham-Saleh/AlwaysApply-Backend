from django.shortcuts import render
from rest_framework.response import Response
from .models import Job, Application
from .serializers import JobSerializer, ApplicationSerializer 
from rest_framework import viewsets
from rest_framework import status
from users.models import User
from rest_framework.pagination import PageNumberPagination
from .filters import JobFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from .serializers import DashboardSerializer
from rest_framework.decorators import api_view



class JobPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'size'
    max_page_size = 100


class jobView(viewsets.ViewSet):
    queryset = Job.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def list(self, request):
        queryset = self.queryset
        filter_backend = DjangoFilterBackend()
        queryset = filter_backend.filter_queryset(request, queryset, self)
        paginator = JobPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serializedData = JobSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializedData.data)



    @api_view(['GET'])
    def jobs_by_company(request, company_id):
        jobs = Job.objects.filter(user_id=company_id)
        serialized_jobs = JobSerializer(jobs, many=True)
        
        return Response(serialized_jobs.data, status=status.HTTP_200_OK)
    
    @api_view(['GET'])
    def job_titles(request):
        job_titles = Job.objects.values_list('title', flat=True)
        job_titles_list = set(job_titles)
        
        return Response({"job_titles": job_titles_list}, status=status.HTTP_200_OK)

    def create(self, request):
        user_id = request.data.get('user')
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_400_BAD_REQUEST)
        request.data['user'] = user.id

        serializedData = JobSerializer(data=request.data)
        if serializedData.is_valid():
            serializedData.save()
            return Response(serializedData.data, status=status.HTTP_201_CREATED)
        return Response(serializedData.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def destroy(self, request, pk):
        try:
            job = Job.objects.get(id=pk)
            job.delete()
        except Job.DoesNotExist:
            return Response({"error": "Job not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "success"})

    def retrieve(self, request, pk):
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
        # elif user.role == 'company':
        #     queryset = Application.objects.filter(company_id=pk)
        
        serializedData = ApplicationSerializer(queryset, many=True)
        return Response(serializedData.data)
    
    def create(self, request):
        serializedData = ApplicationSerializer(data=request.data)
        if serializedData.is_valid():
            print('is Valid --->>')
            serializedData.save()
            return Response(serializedData.data,  status=status.HTTP_201_CREATED)
        return Response(serializedData.errors,  status=status.HTTP_400_BAD_REQUEST)




class ApplicationPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'size'
    max_page_size = 100


class ApplicationDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        # Filter applications based on user role
        if user.role == 'freelancer':
            applications = Application.objects.filter(freelancer=user)
        elif user.role == 'company':
            applications = Application.objects.filter(company=user)
        else:
            return Response({"error": "User role is not valid for dashboard access."}, 
                            status=status.HTTP_403_FORBIDDEN)

        # Apply pagination
        paginator = ApplicationPagination()
        paginated_queryset = paginator.paginate_queryset(applications, request)
        
        # Use a dedicated serializer
        serializer = DashboardSerializer(paginated_queryset, many=True)

        # Return paginated response
        return paginator.get_paginated_response(serializer.data)
