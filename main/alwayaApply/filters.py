import django_filters
from .models import Job,Application

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='istartswith', label='Job Title')
    level = django_filters.CharFilter(lookup_expr='exact', label='Job Level')
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Price Less Than')
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='Price Greater Than')

    class Meta:
        model = Job
        fields = ['title', 'level', 'price_lt', 'price_gt']

class ApplicationFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(choices=[('pending', 'PENDING'), ('accepted', 'ACCEPTED'), ('rejected', 'REJECTED')])
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    min_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='gte')
    max_duration = django_filters.NumberFilter(field_name='duration', lookup_expr='lte')
    created_after = django_filters.DateTimeFilter(field_name='createdAt', lookup_expr='gte')
    created_before = django_filters.DateTimeFilter(field_name='createdAt', lookup_expr='lte')

    class Meta:
        model = Application
        fields = ['status', 'min_price', 'max_price', 'min_duration', 'max_duration', 'created_after', 'created_before']