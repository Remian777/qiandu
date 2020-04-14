from rest_framework.filters import BaseFilterBackend

class LimitFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        limit = request.query_params.get('limit')
        try:
            return queryset[:int(limit)]
        except:
            return queryset



from django_filters.rest_framework.filterset import FilterSet
from django_filters import filters
from . import models
class NovelFilterSet(FilterSet):
    max_works = filters.NumberFilter(field_name='total_words',lookup_expr='lte')
    min_works = filters.NumberFilter(field_name='total_words',lookup_expr='gte')
    class Meta:
        model = models.Novel
        fields = ['category','novel_status','max_works','min_works','is_vip']