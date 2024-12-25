from rest_framework.pagination import PageNumberPagination


class OrderPagination(PageNumberPagination):
    page_size = 4
    max_page_size = 6
    