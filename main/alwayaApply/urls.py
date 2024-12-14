from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'jobs', views.jobView, basename='jobs')
router.register(r'apply', views.ApplicationView, basename='apply')
urlpatterns = [
    path('apply/<int:pk>/', views.ApplicationView.as_view({'get': 'list'}), name='apply-detail'),
    path('jobs/company/<int:company_id>/', views.jobView.jobs_by_company, name='jobs-by-company'),
    path('dashboard/', views.ApplicationDashboard.as_view(), name='application-dashboard'),
    path('jobs/titles/', views.jobView.job_titles, name='job-titles'),
    
] + router.urls



# from django.urls import path, include
# from rest_framework.routers import DefaultRouter
# from . import views

# router = DefaultRouter()
# router.register(r'jobs', views.jobView, basename='jobs')
# router.register(r'apply', views.ApplicationView, basename='apply')

# urlpatterns = [
#     path('', include(router.urls)),
# ]
