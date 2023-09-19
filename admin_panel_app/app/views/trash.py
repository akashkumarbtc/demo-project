
from rest_framework.generics import ListCreateAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
# from io import BytesIO as IO

from rest_framework.pagination import PageNumberPagination
from django.db.models import Q

from link_chatbot.settings.base import *

from admin_panel_app.app.permissions import HasGroupPermission
from admin_panel_app.models import USER_LOGS, TrashedQuestions
from admin_panel_app.app.pagination import  TrashPagination
from admin_panel_app.models import USER_LOGS
from admin_panel_app.app.serializers import TrashedSerializer

from chatbot_app.app.serializers import (TagSerializer,
                                        AnswersSerializer,
                                        ContextSerializer,
                                        FrequencySerializer,)



UserModel = get_user_model()



class AdminPanelTrashWithKeyword(APIView,PageNumberPagination):
    '''
    search for context in of trash table.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins", "Maintenance"] 
    page_size =10
    
    def get(self, request, *args, **kwargs):
        data={'key':None} 
        return Response(data,status=200)
        
    def post(self, request,*args, **kwargs):
        key = request.data['key']
        queryset = TrashedQuestions.objects.filter(Q(question__context_name__icontains=key) | Q(keywords__tags__icontains=key))
        final_data = self.paginate_queryset(queryset,request)
        serializer = TrashedSerializer(final_data,many=True)
        return self.get_paginated_response(serializer.data)
    


    
class AdminPanelTrash(ListCreateAPIView,PageNumberPagination):
    '''
    Provides the list of all the deleted context 
    along with an option to restore.
    '''
    queryset = TrashedQuestions.objects.all().order_by('-created_at')
    serializer_class = TrashedSerializer
    pagination_class = TrashPagination
    page_size          = 10
    

    def post(self, request, *args, **kwargs):
        
        trash_id = request.data['id']
        empty    = ["null",None,"None",""]

        context_data = TrashedQuestions.objects.filter(id=trash_id).values('question','frequency','keywords','answer').first()

        context = {
            "uuid"           : str(context_data['question']['uuid']),
            "context_name"   : context_data['question']['context_name'],
            "prev_context"   : str(context_data['question']['prev_context']) if context_data['question']['prev_context'] not in ["null",None,"","None"] else None,
            "leaf_node"      : context_data['question']['leaf_node'],
            "inputs_required": context_data['question']['inputs_required']
        }

        context_serializer    = ContextSerializer(data =context)
        frequency_serializer  = FrequencySerializer(data =context_data['frequency'] if context_data['frequency'] not in empty else{"context_id":context['uuid'],"frequency":0})
        keywords_serializer   = TagSerializer(data = context_data['keywords'] if context_data['keywords'] not in empty else{"context_id":context['uuid'],"tags":[""]})
        answer = {
                'context_id':context['uuid'],
                'answer':None,
                'document': None,
                'url': None 
            }

        if context_data['answer']:
            answer = {
                'context_id':context['uuid'],
                'answer':context_data['answer']['answer'],
                'document': context_data['answer']['document'] if context_data['answer']['document'] not in empty else None ,
                'url': context_data['answer']['url'] if context_data['answer']['url'] not in empty else None 
            }

            
        answer_serializer     = AnswersSerializer(data = answer )
        if context_serializer.is_valid():
            context_serializer.save()
            
        else:
            return Response({"context error":context_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        if  keywords_serializer.is_valid() and frequency_serializer.is_valid() and answer_serializer.is_valid():

            keywords_serializer.save()
            frequency_serializer.save()
            answer_serializer.save()

            TrashedQuestions.objects.filter(id = trash_id).delete()
            user_type=Group.objects.get(user = request.user.id)

            USER_LOGS.objects.create_user_logs(request.user,str(user_type),"Restored "+str(context_data['question']['context_name']),{"previous_data":[{"Question":None}],"current_data":[{"Question":str(context_data['question']['context_name'])}]},True)
        
            return Response({f"{context_data['question']['context_name']} hass been restored from trash."},status=200)
        else:
            return Response({
                            "frequency error":frequency_serializer.errors,
                             "tags error": keywords_serializer.errors,
                             "answer error":answer_serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST)
