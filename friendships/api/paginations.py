from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class FriendshipPagination(PageNumberPagination):
    # default page size, before we set in url
    page_size = 20
    # default page_size_query_param is None, 
    # meaning do not allow client side to define size of each page
    # if adding this func, means client side can use size = 10 to define a certain size
    # e.g. mobile and web access needs different size
    
    page_size_query_param = 'size'
    # maximum page_size allowed
    max_page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'total_results': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'page_number': self.page.number,
            'has_next_page': self.page.has_next(),
            'results': data,
        })
