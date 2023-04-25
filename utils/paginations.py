from dateutil import parser
from django.conf import settings
from rest_framework.pagination import BasePagination
from rest_framework.response import Response

class EndlessPagination(BasePagination):
    page_size = 20 # if not settings.TESTING else 10

    def __str__(self):
        super(EndlessPagination, self).__init__()
        self.has_next_page = False
    
    def to_html(self):
        pass

    def paginate_ordered_list(self, reverse_ordered_list, request):
        if 'created_at__gt' in request.query_params:
            created_at__gt = parser.isoparse(request.query_params['created_at__gt'])
            objects = []
            for obj in reverse_ordered_list:
                if obj.created_at > created_at__gt:
                    objects.append(obj)
                else:
                    break
            self.has_next_page = False
            return objects   

        index = 0
        if 'created_at__lt' in request.query_params:
            created_at__lt = parser.isoparse(request.query_params['created_at__lt'])
            for index, obj in enumerate(reverse_ordered_list):
                if obj.created_at < created_at__lt:
                    break
            else:
                reverse_ordered_list = []
        
        self.has_next_page = len(reverse_ordered_list) > index + self.page_size
        return reverse_ordered_list[index: index + self.page_size]



    def paginate_queryset(self, queryset, request, view=None):
        
        if 'created_at__gt' in request.query_params:
            """ used to refresh for latest content """
            created_at__gt = request.query_params['created_at__gt']
            queryset = queryset.filter(created_at__gt=created_at__gt)
            self.has_next_page = False
            return queryset.order_by('-created_at')
        
        if 'created_at__lt' in request.query_params:
            """ used for scrolling up to load next page """
            created_at__lt = request.query_params['created_at__lt']
            queryset = queryset.filter(created_at__lt=created_at__lt)
        
        queryset = queryset.order_by('-created_at')[:self.page_size + 1]
        self.has_next_page = len(queryset) > self.page_size
        return queryset[:self.page_size]
    
    def paginate_cached_list(self, cached_list, request):
        paginated_list = self.paginate_ordered_list(cached_list, request)
        # if page up, return all data in paginated_list 
        if 'created_at__gt' in request.query_params:
            return paginated_list
        # if we have next page, indicate cached_list still has data, return
        if self.has_next_page:
            return paginated_list
        # if cached_list length < LIMIT, indicate cached_list has all the data
        if len(cached_list) < settings.REDIS_LIST_LENGTH_LIMIT:
            return paginated_list
        
        # all other situations, find in database
        return None
    
    def get_paginated_response(self, data):
        return Response({
            'has_next_page': self.has_next_page,
            'results': data,
        })