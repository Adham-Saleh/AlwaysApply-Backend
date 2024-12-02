from django.urls import path
from .views import (
    EmployerListCreateAPIView,
    EmployerDetailAPIView,
    PostOfferAPIView,
    JobListAPIView,
    JobDetailAPIView,
    FreelancerListCreateAPIView,
    FreelancerDetailAPIView,
    ApplyForJobAPIView,
    ApplicationListAPIView,
    ApplicationDetailAPIView,
    AcceptApplicationAPIView,
    RejectApplicationAPIView,
    OfferListAPIView,
    MarkOfferCompletedAPIView,
)

urlpatterns = [
    # Employer endpoints
    path('employers/', EmployerListCreateAPIView.as_view(), name='employer-list-create'),
    path('employers/<int:pk>/', EmployerDetailAPIView.as_view(), name='employer-detail'),
    path('employers/<int:employer_id>/post-offer/', PostOfferAPIView.as_view(), name='post-offer'),

    # Job endpoints
    path('jobs/', JobListAPIView.as_view(), name='job-list'),
    path('jobs/<int:pk>/', JobDetailAPIView.as_view(), name='job-detail'),

    # Freelancer endpoints
    path('freelancers/', FreelancerListCreateAPIView.as_view(), name='freelancer-list-create'),
    path('freelancers/<int:pk>/', FreelancerDetailAPIView.as_view(), name='freelancer-detail'),
    path('freelancers/<int:freelancer_id>/apply/<int:job_id>/', ApplyForJobAPIView.as_view(), name='apply-for-job'),

    # Application endpoints
    path('applications/', ApplicationListAPIView.as_view(), name='application-list'),
    path('applications/<int:pk>/', ApplicationDetailAPIView.as_view(), name='application-detail'),
    path('applications/<int:application_id>/accept/<int:employer_id>/', AcceptApplicationAPIView.as_view(), name='accept-application'),
    path('applications/<int:application_id>/reject/<int:employer_id>/', RejectApplicationAPIView.as_view(), name='reject-application'),

    # Offer endpoints
    path('offers/', OfferListAPIView.as_view(), name='offer-list'),
    path('offers/<int:offer_id>/mark-completed/', MarkOfferCompletedAPIView.as_view(), name='mark-offer-completed'),
]
