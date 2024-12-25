from rest_framework.pagination import PageNumberPagination


class MenuItemPagination(PageNumberPagination):
    page_size = 3
    max_page_size = 4
    