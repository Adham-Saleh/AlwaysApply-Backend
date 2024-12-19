from django.urls import path
from .views import RegisterView, LoginView, UserView, LogoutView, userList
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('userList/<int:pk>/', userList.as_view({'get': 'retrieve', 'put':'put'})),
    path('logout', LogoutView.as_view()),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
