import  io 
import pandas as pd
from datetime import datetime
from django.http import HttpResponse
from django.db.models import TextField
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models.functions import Length, Cast

from chatbot_app.models import (Frequency, UntaggedQuestions, Conversation, Feedback, Answers, Document)
from chatbot_app.app.serializers import (FrequencySerializer, QuestionsSerializer, ListConversationSerializer, FeedbackSerializer)


from link_chatbot.settings.base import *

from chatbot_app.models import (Company,Isin)

UserModel = get_user_model()

class IsinLoadData(APIView):
    '''Load Isin Data to database from the user uploaded file'''
    def post(self, request, *args, **kwargs):
        file = request.FILES['file']
        Status = ''
        data = pd.read_excel(file)
        data.columns =['branch','branch_id','branch_name','isin','client','client_id','cin_number','VERTICAL','Flag']
        for i in data.itertuples():
            # if i.status =='I':
            #     Status ='Inactive'
            # elif i.status =='T':
            #     Status ='Temporary'
            # elif i.status =='A':
            #     Status ='Active'
            # if Isin.objects.filter(client=i.client).exists():
            #     Isin.objects.filter(client=i.client).update(isin=i.isin,status = Status)
            # else:
            Isin.objects.create_isin(i.branch,i.branch_id,i.branch_name,i.isin,i.client,i.client_id,i.cin_number,i.VERTICAL,i.Flag)
        
        Isin.objects.filter(client='__last__updated').update(isin=datetime.now())
        return Response({"Successfully updated the ISIN database."},status=200)

class IsinDataTemplate(APIView):
    '''Export Isin data scema/template from database to the user as an excel file'''
    def post(self, request, *args, **kwargs):
        companies_id = Company.objects.filter().values_list('id')
        Status = ['I','A','T','A']
        data ={'branch':[],'branch_id':[],'branch_name':[],'isin':[],'client':[],'client_id':[],'cin_number':[],'Vertical':[],'Flag':[],'status':[]}

        for i in companies_id:
            data_database = '//'.join(Isin.objects.filter(branch=i).values_list('branch__name','branch_code','branch_name','isin','client','client_id','cin_number','Vertical','flag','status').first())
            data_database = data_database.replace('skdc-consultants','SKDC').replace('linkintime','LIIPL').replace('tcplindia','TCPL').replace('unisec','UCS').split('//')
            data['branch'].append(data_database[0])
            data['branch_id'].append(data_database[1])
            data['branch_name'].append(data_database[2])
            data['isin'].append(data_database[3])
            data['client'].append(data_database[4])
            data['client_id'].append(data_database[5])
            data['cin_number'].append(data_database[6])
            data['Vertical'].append(data_database[7])
            data['Flag'].append(data_database[8])
            data['status'].append(Status[i[0]-1])
            
        df = pd.DataFrame(data)
        df.columns = ['Company','RTA_Branch_ID','RTA_BRANCH_NAME','ISIN_CODE','CLIENT_NAME','CLIENT_ID','CINNUMBER','VERTICAL','Flag','Status']
        df.set_index('Company', inplace=True)
        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer)
            
            data = output.getvalue()
        
        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=IsinDataTeplate.xlsx'

        response.write(data)
        return response
        


class ExportFAQ(APIView):
    """
    API to download the FAQ count to excel sheet
    """
    def get(self, request):
        freq_questions = Frequency.objects.select_related('context_id').order_by('-frequency')
        serializer = FrequencySerializer(freq_questions,many=True)
        
        df = pd.DataFrame(serializer.data)
        df = df.drop("context_id", axis='columns')
        df = df[["context_name", "frequency"]]
        # df.set_index('context_name', inplace=True)

        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer , sheet_name='FAQ count')
                workbook  = writer.book
                worksheet = writer.sheets['FAQ count']
                text_format = workbook.add_format({'text_wrap' : True, 'align': 'center'})

                worksheet.set_column('B:B', 45, text_format)
                writer.save()
            
            data = output.getvalue()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=IsinDataTeplate.xlsx'

        response.write(data)
        return response


class ExportUntaggedQuestions(APIView):
    """
    API to download the Untagged questions to excel sheet
    """
    def get(self, request, *args, **kwargs):
        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)

        questions = UntaggedQuestions.objects.filter()
        if start_date and end_date:
            questions = questions.filter(created_at__date__range=(start_date, end_date))
        questions = questions.order_by('-created_at').all()
        serializer = QuestionsSerializer(questions, many=True)


        df = pd.DataFrame(serializer.data)
        df = df.drop("id", axis='columns')
        df = df.drop("updated_at", axis='columns')
        # df.set_index('un_taged_question', inplace=True)
        df['created_at'] = df['created_at'].astype('str').str.split(".").str[0].str.replace("T"," ")

        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Untagged Questions')
                workbook  = writer.book
                worksheet = writer.sheets['Untagged Questions']
                text_format = workbook.add_format({'text_wrap' : True, 'align': 'center'})

                worksheet.set_column('B:F', 30, text_format)
                writer.save()
            
            data = output.getvalue()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=IsinDataTeplate.xlsx'

        response.write(data)
        return response
    

class ExportUserLogs(APIView):
    """
    API to download the user logs to excel sheet
    """
    def get(self, request, *args, **kwargs):
        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)

        queryset = Conversation.objects.annotate(text_len=Length(Cast('conversation_data', TextField()))).filter(text_len__gt = 300)
        if start_date and end_date:
            queryset = queryset.filter(started_at__date__range=(start_date, end_date)).order_by("-started_at")

        serializer = ListConversationSerializer(queryset, many=True)

        df = pd.DataFrame(serializer.data)
        df['started_at'] = df['started_at'].astype('str').str.split(".").str[0].str.replace("T"," ")
        # df['selected_options'] = df['selected_options'].astype('str').str.replace("None,","")
        df['selected_options'] = df['selected_options'].apply(lambda x: [elem for elem in x if elem is not None])
        df['selected_options'] = df['selected_options'].apply(lambda x: x[1:] if x and x[0] == '' else x)
        split_df = df
        split_df = split_df.explode('selected_options')
        split_df.loc[split_df.duplicated(subset=['started_at', 'session_id']), ['started_at', 'session_id']] = ''

        # split_df['selected_options_type'] = split_df['selected_options'].apply(lambda x: type(x).__name__)
        # code to split the selected_options column wise
        # df2 = pd.DataFrame(split_df['selected_options'].astype('str').str.replace("[","").str.replace("]","").str.split(",").values.tolist())
        # df2.columns = ['option selected {}'.format(x+1) for x in range(len(df2.columns))]
        # split_df = split_df.drop("selected_options", axis='columns')
        # split_df = split_df.join(df2)


        # df.set_index('started_at', inplace=True)

        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Combined Options')
                split_df.to_excel(writer, sheet_name='Seperated Options')
                workbook  = writer.book
                worksheet = writer.sheets['Combined Options']
                worksheet2 = writer.sheets['Seperated Options']
                text_format = workbook.add_format({'text_wrap' : True, 'align': 'center'})

                worksheet.set_column('B:D', 45, text_format)
                worksheet2.set_column('B:Z', 45, text_format)
                writer.save()
            
            data = output.getvalue()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=IsinDataTeplate.xlsx'

        response.write(data)
        return response


class ExportUserFeedback(APIView):
    """
    API to download the user feedback to excel sheet
    """
    def get(self, request, *args, **kwargs):
        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)

        queryset = Feedback.objects.filter()
        if start_date and end_date:
            queryset = queryset.filter(created_at__date__range=(start_date, end_date))
        queryset = queryset.order_by('-created_at').all()
        serializer = FeedbackSerializer(queryset, many=True)


        df = pd.DataFrame(serializer.data)
        df = df.drop("id", axis='columns')
        df = df.drop("updated_at", axis='columns')
        # df.set_index('reason', inplace=True)
        df['created_at'] = df['created_at'].astype('str').str.split(".").str[0].str.replace("T"," ")

        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='User Feedback')
                workbook  = writer.book
                worksheet = writer.sheets['User Feedback']
                text_format = workbook.add_format({'text_wrap' : True, 'align': 'center'})

                worksheet.set_column('B:D', 40, text_format)
                writer.save()
            
            data = output.getvalue()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=IsinDataTeplate.xlsx'

        response.write(data)
        return response
    

class ExportAllQuestions(APIView):
    """
    API to download the user feedback to excel sheet
    """

    def  add_data_recursively(self, data):

        for k,v in data.items():
            if(isinstance(v, list)):
                for i in v:
                    nodes = Answers.objects.select_related('context_id').filter(context_id__prev_context=str(i['uuid'])).order_by('context_id__context_name')
                    if not len(nodes):
                        continue
                    temp = {}
                    for y in nodes:
                        doc = Document.objects.get(document = y.document).document.url if y.document else None
                        obj = {"uuid": y.context_id.uuid, "question": y.context_id.context_name, "document": doc, "created_at": y.created_at}
                        if 'children' not in temp:
                            temp['children'] = [obj]
                            continue
                        temp['children'].append(obj)
                    
                    i.update(self.add_data_recursively(temp))

        return data
    
    def loop_children(self, resp, child_dict ,p_row):
        if isinstance(child_dict, list):
            for i in child_dict:
                if "children" not in i:
                    temp = []
                    temp.append(str(i["created_at"].strftime("%d-%m-%Y")))
                    temp.append(str(i["uuid"]))
                    temp.extend(p_row)
                    temp.append(str(i["question"]))
                    temp.append(str(i["uuid"]))
                    temp.append(str(i["document"]))
                    resp.append(temp)
                else: 
                    p_row.append(i["question"])
                    temp = []
                    temp.append(str(i["created_at"].strftime("%d-%m-%Y")))
                    temp.append(str(i["uuid"]))
                    temp.extend(p_row)
                    temp.append(str(i["question"]))
                    temp.append(str(i["uuid"]))
                    temp.append(str(i["document"]))
                    resp.append(temp)
                    self.loop_children(resp, i["children"], p_row)
                    p_row = p_row[:-1]

    def get(self, request, *args, **kwargs):
        data = {}
        root_nodes = Answers.objects.select_related('context_id').filter(context_id__prev_context=None).order_by('context_id__context_name')

        for x in root_nodes:
            doc = Document.objects.get(document = x.document).document.url if x.document else None
            obj = {"uuid": x.context_id.uuid, "question": x.context_id.context_name, "document": doc, "created_at": x.created_at }

            if str(x.context_id.prev_context) in data:
                data[str(x.context_id.prev_context)].append(obj)
            else:
                data[str(x.context_id.prev_context)] = [obj]

        
        data = self.add_data_recursively(data)

        data = data['None']

        resp = []
        for i in data:
            if "children" in i:
                main_topic = i["question"]
                print_row = []
                print_row.append(main_topic)
                temp = []
                temp.append(str(i["created_at"].strftime("%d-%m-%Y")))
                temp.append(str(i["uuid"]))
                temp.append(str(i["question"]))
                temp.append(str(i["uuid"]))
                temp.append(str(i["document"]))
                resp.append(temp)
                self.loop_children(resp, i["children"], print_row)

        df = pd.DataFrame(resp)

        with io.BytesIO() as output:
            with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
                df.to_excel(writer, sheet_name='Questions ID')
                workbook  = writer.book
                worksheet = writer.sheets['Questions ID']
                text_format = workbook.add_format({'text_wrap' : True, 'align': 'center'})

                worksheet.set_column('B:J', 40, text_format)
                writer.save()
            
            data = output.getvalue()

        response = HttpResponse(content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=IsinDataTeplate.xlsx'

        response.write(data)
        return response