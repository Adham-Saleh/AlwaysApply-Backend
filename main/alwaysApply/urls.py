from django.contrib import admin
from django.urls import path

from . import views

urlpatterns = [
    path('test', views.job.as_view(), name="job-list"),
]