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
from django.views.decorators.csrf import csrf_exempt
from .filters import ApplicationFilter

@csrf_exempt
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
        return paginator.get_paginated_response({'jobs': serializedData.data, 'totalCount': queryset.count()})
    
    

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

# views.py


class ApplicationPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'size'
    max_page_size = 100

class ApplicationView(viewsets.ViewSet):
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ApplicationFilter

    
    def list(self, request, pk=None):
        try:
            user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

        if user.role == 'freelancer':  
            queryset = Application.objects.filter(freelancer_id=pk)
        elif user.role == 'company':
            queryset = Application.objects.filter(company_id=pk)
        else:
            return Response({"error": "Invalid user role"}, status=400)
        
        filter_backend = DjangoFilterBackend()
        queryset = filter_backend.filter_queryset(self.request, queryset, self)

        paginator = ApplicationPagination()
        paginated_queryset = paginator.paginate_queryset(queryset, request)
        serialized_data = ApplicationSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serialized_data.data)


    def create(self, request):
        serialized_data = ApplicationSerializer(data=request.data)
        if serialized_data.is_valid():
            serialized_data.save()
            return Response(serialized_data.data, status=status.HTTP_201_CREATED)
        return Response(serialized_data.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def update(self, request, pk):
        try:
            application = Application.objects.get(id=pk)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = ApplicationSerializer(application, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def retrieve(self, request, pk=None):
        try:
            application = Application.objects.get(id=pk)
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=404)

        serialized_data = ApplicationSerializer(application)
        return Response(serialized_data.data)
    
    def destroy(self, request, pk):
        try:
            application = Application.objects.get(id=pk)
            application.delete()
        except Application.DoesNotExist:
            return Response({"error": "Application not found"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"message": "success"})



class JobsByCompanyView(APIView):
    queryset = Job.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = JobFilter

    def get(self, request, company_id):
        try:
            company = User.objects.get(id=company_id, role='company')
            queryset = Job.objects.filter(user=company)

            filter_backend = DjangoFilterBackend()
            queryset = filter_backend.filter_queryset(request, queryset, self)

            paginator = JobPagination()
            paginated_queryset = paginator.paginate_queryset(queryset, request)

            serialized_jobs = JobSerializer(paginated_queryset, many=True)

            return paginator.get_paginated_response({
                'jobs': serialized_jobs.data,
                'totalCount': queryset.count()
            })

        except User.DoesNotExist:
            return Response({"error": "Company not found."}, status=status.HTTP_404_NOT_FOUND)

class ApplicationDashboard(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        if user.role == 'freelancer':
            applications = Application.objects.filter(freelancer=user)

        elif user.role == 'company':
            applications = Application.objects.filter(company=user)

        else:
            return Response({"error": "User role is not valid for dashboard access."}, 
                            status=status.HTTP_403_FORBIDDEN)
        
        paginator = ApplicationPagination()
        paginated_queryset = paginator.paginate_queryset(applications, request)

        serializer = DashboardSerializer(paginated_queryset, many=True)
        return paginator.get_paginated_response(serializer.data)
