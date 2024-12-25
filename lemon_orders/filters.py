
from django_filters.rest_framework import filters
from django_filters import FilterSet
from lemon_orders.models import Order


class OrderFilter(FilterSet):

    user = filters.NumberFilter(field_name='user', lookup_expr='exact')
    delivery_crew = filters.NumberFilter(field_name='delivery_crew', lookup_expr='exact')
    date = filters.DateFilter(field_name='date', lookup_expr='exact')
    status = filters.BooleanFilter(field_name='status', lookup_expr='exact')

    class Meta:
        model = Order
        fields = ["user","delivery_crew","date","status"]