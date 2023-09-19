
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# from io import BytesIO as IO

from rest_framework.pagination import PageNumberPagination

from link_chatbot.settings.base import *


from admin_panel_app.app.permissions import HasGroupPermission
from admin_panel_app.models import USER_LOGS
from admin_panel_app.app.pagination import UserLogPagination
from admin_panel_app.models import USER_LOGS
from admin_panel_app.app.serializers import UserLogsSerializer

from chatbot_app.models import (Context, Conversation,UntaggedQuestions,)

UserModel = get_user_model()

class AdminPanelAnalytics(APIView):
    '''
    Provides the Aanalytics on number
    of visitors and count of questions with answers and untagged questions.  
    '''
    def get(self, request, format=None):
        start_date = self.request.query_params.get('start_date', None)
        end_date = self.request.query_params.get('end_date', None)

        visitor_count, questions_with_answers, untaged_question_count = 0, 0, 0
        if not start_date and not end_date:
            visitor_count          = Conversation.objects.count()
            questions_with_answers = Context.objects.count()
            untaged_question_count = UntaggedQuestions.objects.count()

        if start_date and not end_date:
            visitor_count          = Conversation.objects.filter(started_at__date=start_date).count()
            questions_with_answers = Context.objects.filter(created_at__date=start_date).count()
            untaged_question_count = UntaggedQuestions.objects.filter(created_at__date=start_date).count()

        if start_date and end_date:
            visitor_count          = Conversation.objects.filter(started_at__date__gte=start_date,started_at__date__lte=end_date).count()
            questions_with_answers = Context.objects.filter(created_at__date__gte=start_date,created_at__date__lte=end_date).count()
            untaged_question_count = UntaggedQuestions.objects.filter(created_at__date__gte=start_date,created_at__date__lte=end_date).count()

        data = {
            "filter"            :"All",
            "visitors"          :visitor_count,
            "question_answers"  :questions_with_answers,
            "untagged_questions":untaged_question_count
        }
        
        return Response(data,status=200)

class UserLogsView(ModelViewSet):
    '''
    stores all the user logs.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins","Maintenance"]
    pagination_class   = UserLogPagination
    serializer_class   = UserLogsSerializer
    queryset = USER_LOGS.objects.all().order_by('-created_at')


class AdminPanelUserloagsView(APIView,PageNumberPagination):
    '''
    displays all the user logs based on search.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins","Maintenance"]
    
    page_size = 5

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

    def get(self,request, *args, **kwargs):

        search_by_user = [str(i) for i in UserModel.objects.all()]
        
        data ={"search_by_user":search_by_user}
        
        return Response(data,status=200)

    def post(self,request, *args, **kwargs):

        user = request.data['search_by_user']
        print(user)
        data= USER_LOGS.objects.filter(user_name = user).values().order_by('-created_at')

        final_data = self.paginate_queryset(data,request,view=self)

        serializer = UserLogsSerializer(final_data,many=True)
        return self.get_paginated_response(serializer.data)
