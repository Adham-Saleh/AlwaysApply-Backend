from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView, ListAPIView
from django.shortcuts import get_object_or_404
from .models import Employer, Job, Freelancer, Application, Offer
from .serializers import (
    EmployerSerializer,
    JobSerializer,
    FreelancerSerializer,
    ApplicationSerializer,
    OfferSerializer
)

# Employer Views
class EmployerListCreateAPIView(ListAPIView, CreateAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

class EmployerDetailAPIView(RetrieveAPIView):
    queryset = Employer.objects.all()
    serializer_class = EmployerSerializer

class PostOfferAPIView(APIView):
    def post(self, request, employer_id):
        employer = get_object_or_404(Employer, id=employer_id)
        title = request.data.get('title')
        description = request.data.get('description')
        budget = request.data.get('budget')

        if not title or not description or not budget:
            return Response({"error": "All fields are required."}, status=status.HTTP_400_BAD_REQUEST)

        job = employer.post_offer(title, description, budget)
        serializer = JobSerializer(job)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

# Job Views
class JobListAPIView(ListAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

class JobDetailAPIView(RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = JobSerializer

# Freelancer Views
class FreelancerListCreateAPIView(ListAPIView, CreateAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer

class FreelancerDetailAPIView(RetrieveAPIView):
    queryset = Freelancer.objects.all()
    serializer_class = FreelancerSerializer

class ApplyForJobAPIView(APIView):
    def post(self, request, freelancer_id, job_id):
        freelancer = get_object_or_404(Freelancer, id=freelancer_id)
        job = get_object_or_404(Job, id=job_id)
        cover_letter = request.data.get('cover_letter')

        try:
            application = freelancer.apply_for_job(job, cover_letter)
            serializer = ApplicationSerializer(application)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Application Views
class ApplicationListAPIView(ListAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class ApplicationDetailAPIView(RetrieveAPIView):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer

class AcceptApplicationAPIView(APIView):
    def post(self, request, application_id, employer_id):
        employer = Employer.objects.get(id=employer_id)
        application = Application.objects.get(id=application_id)
        try:
            employer.accept_freelancer(application)
            return Response({"message": "Application accepted."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class RejectApplicationAPIView(APIView):
    def post(self, request, application_id, employer_id):
        employer = get_object_or_404(Employer, id=employer_id)
        application = get_object_or_404(Application, id=application_id)
        reason = request.data.get('reason')

        if not reason:
            return Response({"error": "Rejection reason is required."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            employer.reject_freelancer(application, reason)
            return Response({"message": "Application rejected."}, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# Offer Views
class OfferListAPIView(ListAPIView):
    queryset = Offer.objects.all()
    serializer_class = OfferSerializer

class MarkOfferCompletedAPIView(APIView):
    def post(self, request, offer_id):
        offer = get_object_or_404(Offer, id=offer_id)
        offer.mark_completed()
        return Response({"message": "Offer marked as completed."}, status=status.HTTP_200_OK)
