from rest_framework import pagination

class NewsCommentPagination(pagination.PageNumberPagination):
    page_size = 4
    page_size_query_param = 'page_size'
    new_page_size = 100