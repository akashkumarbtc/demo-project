from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model

# from io import BytesIO as IO

from rest_framework.pagination import PageNumberPagination

from link_chatbot.settings.base import *


from admin_panel_app.app.permissions import HasGroupPermission
from admin_panel_app.app.pagination import HTTPSPagination
from rest_framework import generics
from chatbot_app.models import Conversation
from chatbot_app.app.serializers import ListConversationSerializer
from django.db.models.functions import Length, Cast
from django.db.models import TextField
from datetime import date


class ConversationView(generics.ListAPIView):
    # queryset = Conversation.objects.annotate(text_len=Length(Cast('conversation_data', TextField()))).filter(text_len__gt = 300).all().order_by("-started_at")
    
    # queryset = Conversation.objects.all().order_by("-started_at")
    serializer_class = ListConversationSerializer
    pagination_class = HTTPSPagination
    HTTPSPagination.page_size = 20

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)

        queryset = Conversation.objects.annotate(text_len=Length(Cast('conversation_data', TextField()))).filter(text_len__gt = 300)
        if start_date and end_date:
            queryset = queryset.filter(started_at__date__range=(start_date, end_date))

        return queryset.all().order_by("-started_at")

    def list(self, request):
        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)
        total_users, active_users, inactive_users = 0, 0, 0

        queryset = self.get_queryset()

        page = self.paginate_queryset(queryset)
        if page is not None:

            serializer = self.get_serializer(page, many=True)
            response_list = self.get_paginated_response(serializer.data)

            count_queryset = Conversation.objects.annotate(text_len=Length(Cast('conversation_data', TextField()))).filter(text_len__gt = 300)

            if not start_date:
                start_date = str(date.today())
                end_date   = str(date.today())

            active_users   = count_queryset.filter(started_at__date__range=(start_date, end_date)).count()
            total_users    = Conversation.objects.filter(started_at__date__gte=start_date,started_at__date__lte=end_date).count()
            inactive_users = total_users - active_users

            response_list.data['details'] = {"details": {"total_users": total_users, "active_users": active_users, "inactive_users": inactive_users}}

            return Response(data=response_list.data)

class CountOfEmptyConversations(APIView):
    def get(self, request):
        start_date = self.request.query_params.get('start_date')
        sessions = Conversation.objects.filter(started_at__date=start_date).values_list('session_id')
        count=0
        for j in sessions:
            conv = Conversation.objects.filter(session_id=j[0]).values('conversation_data')[0]['conversation_data']
            if len(conv)==1 and conv[0]['selected'] == None and not conv[0]['response']['bot_message']:
                count+=1
        return Response(count,200)