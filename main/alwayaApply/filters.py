import django_filters
from .models import Job

class JobFilter(django_filters.FilterSet):
    title = django_filters.CharFilter(lookup_expr='istartswith', label='Job Title')
    level = django_filters.CharFilter(lookup_expr='exact', label='Job Level')
    price_lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt', label='Price Less Than')
    price_gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt', label='Price Greater Than')

    class Meta:
        model = Job
        fields = ['title', 'level', 'price_lt', 'price_gt']
