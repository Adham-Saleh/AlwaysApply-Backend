from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views


router = DefaultRouter()
router.register(r'jobs', views.jobView, basename='jobs')
router.register(r'apply', views.ApplicationView, basename='apply')
router.register(r'appllication', views.ApplicationView, basename='application')
urlpatterns = [
    path('apply/<int:pk>/', views.ApplicationView.as_view({'get': 'list'}), name='apply-detail'),
    path('application/<int:pk>/', views.ApplicationView.as_view({'get': 'retrieve'}), name='application-detail'),
    path('dashboard/', views.ApplicationDashboard.as_view(), name='application-dashboard'),
    path('jobs/titles/', views.jobView.job_titles, name='job-titles'),
    path('companies/<int:company_id>/jobs/', views.JobsByCompanyView.as_view(), name='jobs-by-company'),
    
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
