from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from chatbot_app.models import Isin, Frequency

class UserLogPagination(PageNumberPagination):

    page_size =5
    page_size_query_params ='size'
    # max_page_size =10
    
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'current': self.page.number,
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class TrashPagination(PageNumberPagination):

    page_size =10
    page_size_query_params ='size'
    # max_page_size =10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'current': self.page.number,
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })
    

class CustomPagination(PageNumberPagination):

    page_size =10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'current': self.page.number,
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })


class HTTPSPagination(PageNumberPagination):

    page_size = 20

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': str(self.get_next_link()).replace('http', 'https') if self.get_next_link() else None,
                'current': self.page.number,
                'previous': str(self.get_previous_link()).replace('http', 'https') if self.get_previous_link() else None
            },
            'count': self.page.paginator.count,
            'results': data
        })

class ISINPagination(PageNumberPagination):

    page_size = 10

    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'current': self.page.number,
                'last_updated': Isin.objects.filter(client='__last__updated').values('isin').first(),
                'total_visits': Frequency.objects.filter(context_id__context_name='Find ISIN / CIN').values('frequency').first(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'results': data
        })