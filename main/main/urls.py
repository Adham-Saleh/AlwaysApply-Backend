from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('employer.urls')),
    path('api/', include('users.urls')),
    path('', include('alwayaApply.urls'))
]

# Swgger
from rest_framework import permissions
from rest_framework.routers import DefaultRouter
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Schema view configuration
schema_view = get_schema_view(
    openapi.Info(
        title="Job Portal API",
        default_version='v1',
        description="""
        **Team Members**  
        - **Adham Saleh**: Frontend Developer  
        - **Ahmed Elhadidy**: Backend Developer  
        - **Mohammed Abedy**: Backend Developer  
        - **Mahmoud Walid**: Backend Developer  
        """,
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

# Router setup
router = DefaultRouter()
# Add your API viewsets here, e.g.:
# router.register(r'jobs', JobViewSet, basename='job')

# URL patterns
urlpatterns += [
    # Add the documentation path explicitly
    path('documentation/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
] + router.urls
