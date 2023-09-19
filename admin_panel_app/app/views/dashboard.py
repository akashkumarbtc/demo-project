from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
import pandas as pd
# from io import BytesIO as IO
from django.http import HttpResponse
import  io 

from rest_framework.pagination import PageNumberPagination

from link_chatbot.settings.base import *


from admin_panel_app.app.permissions import HasGroupPermission

from chatbot_app.app.serializers import (
                                        FrequencySerializer,
                                        QuestionsSerializer)

from chatbot_app.models import (Frequency,UntaggedQuestions,
                                Rating,)

UserModel = get_user_model()

class AdminPanelDashboardRatingView(APIView):
    '''
    provides Analytics on Ratings
    given to the chatbot from users.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins", "Maintenance"]

    def get(self,request, *args, **kwargs):
        ragtings        = Rating.objects.filter().values_list("rating_5","rating_4","rating_3","rating_2","rating_1").first()
        
        total_ratings   =ragtings[0]+ragtings[1]+ragtings[2]+ragtings[3]+ragtings[4]

        if total_ratings ==0:
            average_rating =0
        
        else:
            average_rating = round((ragtings[0]*5+ragtings[1]*4+ragtings[2]*3+ragtings[3]*2+ragtings[4])/total_ratings,2)
            
        data={
            "ratings":[{"rating": "1 star", "val": ragtings[4]},{"rating": "2 star", "val": ragtings[3]},
                       {"rating": "3 star", "val": ragtings[2]},{"rating": "4 star", "val": ragtings[1]},
                       {"rating": "5 star", "val": ragtings[0]},{"rating":"average_ratiing","val":average_rating}]
        }
        
        return Response(data,status=200)

class DashboardCustomerRatingGraph(APIView):
    '''
    provides Total Average Rating
    given to the chatbot from users.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins", "Maintenance"]

    def get(self, request, format=None):
        ragtings  = Rating.objects.filter().values().first()
        total_ratings =ragtings["rating_5"]+ragtings["rating_4"]+ragtings["rating_3"]+ragtings["rating_2"]+ragtings["rating_1"]
        if total_ratings ==0:
            data = {"percentage":0}
        else:   
            average_rating = (ragtings["rating_5"]*5+ragtings["rating_4"]*4+ragtings["rating_3"]*3+ragtings["rating_2"]*2+ragtings["rating_1"])/total_ratings
            percentage = round((average_rating/5)*100,2)
            data = {"percentage":percentage}

        return Response(data,status=200)

class FrequentlyAskedQuestionsView(APIView,PageNumberPagination):
    '''
    provides list of top 10
    frequently asked questions.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins", "Maintenance"]
    page_size          = 10

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
        
        freq_questions = Frequency.objects.select_related('context_id').order_by('-frequency')

        final_data = self.paginate_queryset(freq_questions,request,view=self)

        serializer = FrequencySerializer(final_data,many=True)
        return self.get_paginated_response(serializer.data)


       

class DashboardListUntaggedQuestions(APIView,PageNumberPagination):
    '''
    Provides list of all the untagged questions.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins", "Maintenance"]
    page_size          = 10

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
    
    def patch(self,request, *args, **kwargs):
        r_id     = request.data['id']
        resolved = request.data['resolved']
        UntaggedQuestions.objects.filter(id = r_id).update(is_resolved=resolved)
        return Response(status=200)

    def get(self, request, *args, **kwargs):
        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)
        order_by   = self.request.query_params.get('order_by', None)

        questions = UntaggedQuestions.objects.filter()
        if start_date and end_date:
            questions = questions.filter(created_at__date__range=(start_date, end_date))
        if order_by:
            questions = questions.order_by(order_by).all()
        else:
            questions = questions.order_by('-created_at').all()
        
        final_data = self.paginate_queryset(questions,request,view=self)

        serializer = QuestionsSerializer(final_data,many=True)
        return self.get_paginated_response(serializer.data)
    
    def post(self, request, *args, **kwargs):

        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)

        if start_date and end_date:
            untaged_ques = UntaggedQuestions.objects.filter(created_at__date__range=(start_date, end_date)).values('un_taged_question', 'frequency', 'is_resolved', 'mail_click', 'created_at').order_by('-created_at').all()
        else:
            untaged_ques = UntaggedQuestions.objects.values('un_taged_question', 'frequency', 'is_resolved', 'mail_click', 'created_at').order_by('-created_at').all()
        
        untaged_questions = [x for x in untaged_ques]
        # print(untaged_questions)
        df = pd.DataFrame(untaged_questions)
        df['created_at'] = df['created_at'].apply(lambda a: pd.to_datetime(a).date())
        def update_status(a):
            if "true" in str(a).lower():
                return "Resolved"
            elif "false" in str(a).lower():
                return "Removed"
            else:
                return "Pending"

        df['is_resolved'] = df['is_resolved'].apply(lambda a: update_status(a))

        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer)
            data = output.getvalue()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=test.xlsx'

        response.write(data)
        return response

