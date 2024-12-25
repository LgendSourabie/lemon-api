
from django_filters.rest_framework import filters
from django_filters import FilterSet
from lemon_menuitems.models import MenuItem


class MenuItemFilter(FilterSet):

    max_price = filters.NumberFilter(field_name='price', lookup_expr='lte')
    category = filters.CharFilter(field_name='category__title', lookup_expr='exact')
    featured = filters.BooleanFilter(field_name='featured', lookup_expr='exact')

    class Meta:
        model = MenuItem
        fields = ["max_price","category","featured"]