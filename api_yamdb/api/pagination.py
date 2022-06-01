from rest_framework.pagination import PageNumberPagination


class ObjectsPagination(PageNumberPagination):
    page_size = 20
