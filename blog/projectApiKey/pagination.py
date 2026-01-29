from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination, CursorPagination

class BlogPagination(PageNumberPagination):
    page_size = 2
    page_query_param ="page_size"
    page_size_query_param = "size"
    max_page_size = 5
    last_page_strings = ("end",)

class AuthorPagination(PageNumberPagination):
    page_size = 2
    page_query_param = "page"
    page_size_query_param = "size"    
    max_page_size = 3 
    last_page_strings = ("end",)
    
class BlogOffsetPagination(PageNumberPagination):
    default_limit = 4
    limit_query_param = "limit"
    offset_query_param = "offset"
    max_limit = 5

class BlogCursorPagination(CursorPagination):
    page_size = 3
    cursor_query_param = 'cursor'
    ordering ="-title"