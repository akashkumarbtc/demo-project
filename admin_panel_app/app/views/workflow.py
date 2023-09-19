from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import uuid
from rest_framework.parsers import MultiPartParser, FormParser,JSONParser

from link_chatbot.settings.base import *

from admin_panel_app.models import USER_LOGS
from admin_panel_app.app.serializers import TrashedSerializer

from chatbot_app.app.serializers import (TagSerializer,
                                        DocumentSerializer,
                                        AnswersSerializer,
                                        ContextSerializer,
                                        FrequencySerializer,)

from chatbot_app.models import (Answers, Context,Tag, Document,
                                Company,Frequency,)

UserModel = get_user_model()

class AdminPanelContextView(APIView):
    '''
    Provides list of contexts in in the admin pannel. 
    '''
    def  add_data_recursively(self, data):

        for k,v in data.items():
            if(isinstance(v, list)):
                for i in v:
                    nodes = Answers.objects.select_related('context_id').filter(context_id__prev_context=str(i['uuid'])).order_by('context_id__context_name')
                    if not len(nodes):
                        continue
                    temp = {}
                    for y in nodes:
                        obj = {"uuid": y.context_id.uuid, "question": y.context_id.context_name, "answer": y.answer }
                        if 'children' not in temp:
                            temp['children'] = [obj]
                            continue
                        temp['children'].append(obj)
                    
                    i.update(self.add_data_recursively(temp))

        return data


    def get(self, request, format=None):

        data = {}
        root_nodes = Answers.objects.select_related('context_id').filter(context_id__prev_context=None).order_by('context_id__context_name')

        for x in root_nodes:
            obj = {"uuid": x.context_id.uuid, "question": x.context_id.context_name, "answer": x.answer }

            if str(x.context_id.prev_context) in data:
                data[str(x.context_id.prev_context)].append(obj)
            else:
                data[str(x.context_id.prev_context)] = [obj]

        
        data = self.add_data_recursively(data)
                    
        return Response(data['None'],status=200)

    def delete(self, request,format=None, **kwargs):
        uuid_context = self.kwargs['pk']
        context = Context.objects.filter(pk=uuid_context).values('uuid','context_name','prev_context','leaf_node','inputs_required').first()
        frequency = Frequency.objects.filter(context_id=context['uuid']).values('context_id','frequency').first()
        tags    = Tag.objects.filter(context_id=context['uuid']).values('context_id','tags').first()
        answers = Answers.objects.filter(context_id =context['uuid']).values('context_id','answer','url','document').first()
        
        print(str(request.user))
        trash_data = {
            "question":{"uuid":str(context['uuid']),"context_name":context['context_name'],
                        "prev_context":str(context['prev_context']),"leaf_node":context['leaf_node'],"inputs_required":context['inputs_required']} if context else None,
            "keywords":{"context_id":str(tags['context_id']),"tags":tags['tags']}if tags else None,
            "frequency":{"context_id":str(frequency['context_id']),"frequency":frequency['frequency']} if frequency else None,
            "answer":{"context_id":str(answers['context_id']),"answer":answers['answer'],"url":answers['url'],"document":answers['document']} if answers else None,
            "user_name":str(request.user)
        }

        Trashed_Serializer = TrashedSerializer(data=trash_data)

        if Trashed_Serializer.is_valid():
            Trashed_Serializer.save()
            Context.objects.filter(pk=uuid_context).delete()

        else:
            return Response(Trashed_Serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        user_type=Group.objects.get(user = request.user.id)
        USER_LOGS.objects.create_user_logs(request.user,str(user_type),"Deleted "+str(context['context_name'])+" context",{"previous_data":[{"Question":str(context['context_name'])}],"current_data":[{"Question":None}]},False)

        return Response({f"{trash_data['question']['context_name']} has been moved to trash."},status=status.HTTP_204_NO_CONTENT)


class AdminPanelContextDetailView(APIView):
    '''
    updated all related fields of indual context in in the admin pannel. 
    '''
    parser_classes = ([MultiPartParser, FormParser,JSONParser,])
    def get(self, request, format=None,**kwargs):
        
        uuid_context = self.kwargs['pk']
        
        question = Context.objects.filter(uuid = uuid_context).values('context_name','prev_context').first()
        keywords = Tag.objects.filter(context_id=uuid_context).values('tags').first()
        answer   = Answers.objects.filter(context_id = uuid_context).values('answer','url','document').first()
        doc = Document.objects.filter(id = answer['document']).values('document').first() if answer and answer['document'] else None
        

        return Response({"uuid" : uuid_context,
                        "question":question['context_name'],
                         "answer":answer['answer'] if answer else "null",
                         "document":doc['document'] if doc else None,
                         "url":answer['url'],
                         "prev_context":question['prev_context'],
                         "keywords":",".join(keywords['tags'])},status=200)

    def patch(self, request, format=None, **kwargs):

        uuid_context     = self.kwargs['pk']
        prev_context    = request.data['prev_context'] if request.data['prev_context'] else None
 
        context = Context.objects.get(uuid=uuid_context)
        context_data = { "prev_context":prev_context}
        context_serializer = ContextSerializer(context,data=context_data)
        if Context.objects.get(uuid=uuid_context).prev_context!= prev_context:
            Context.objects.filter(uuid=prev_context).update(leaf_node =False)

        if context_serializer.is_valid():
            context_serializer.save()

        return Response(f"Updated question successfully!",status=200)
    
    #@parser_classes([MultiPartParser, FormParser])
    def put(self, request, format=None, **kwargs):

        uuid_context     = self.kwargs['pk']
        update_question  = request.data['question']
        updated_tags     = [i.strip() for i  in request.data['keywords'].split(',')]
        updated_url      = request.data['url'] 
        updated_doc      = request.data['document']
        updated_answer   = request.data['answer']
        prev_context     = request.data['prev_context'] if request.data['prev_context'] else None
        history          = {"previous_data":[],"current_data":[]}

        if updated_doc in ["null",None,""]: updated_doc=None
            
        context = Context.objects.get(uuid=uuid_context)
        context_data = {'context_name':update_question, "prev_context":prev_context}
        context_serializer = ContextSerializer(context,data=context_data)
        if Context.objects.get(uuid=uuid_context).prev_context!= prev_context:
            Context.objects.filter(uuid=prev_context).update(leaf_node =False)
        
        tags_instance = Tag.objects.get(context_id =uuid_context)
        tags = Tag.objects.filter(context_id =uuid_context).values("tags").first()
        tags_data = {'context_id':uuid_context,
                     'tags':updated_tags}
        tags_TagSerializer = TagSerializer(tags_instance,data = tags_data)

        answer_instance = Answers.objects.get(context_id =uuid_context)

        answer = Answers.objects.filter(context_id =uuid_context).values('answer','url','document').first()

        document = Document.objects.filter(id=answer['document']).values('document','id').first()

        if str(context)!= update_question:
            history['previous_data'].append({"Question":str(context)}),history['current_data'].append({"Question":str(update_question)})
        
        if updated_tags != tags['tags']:
            history['previous_data'].append({"Keywords":tags['tags']}),history['current_data'].append({"Keywords":updated_tags})
        
        
        if updated_doc !=None and document!=None:
            if updated_doc!=str(document['document']):
                    
                document_instance = Document.objects.get(id=answer['document'])
                company  = Document.objects.get(id=answer['document']).company_id
                
                company_id = Company.objects.get(name = company).id

                document_data = {"id":answer['document'],"company_id":company_id,"document":updated_doc}
                doc_serializer = DocumentSerializer(document_instance,data =document_data)
            
                if doc_serializer.is_valid():
                    doc_serializer.save()
                    if str(document['document'])!=str(updated_doc):
                        
                        history['previous_data'].append({"Document":str(document['document']) if document!=None else None}),history['current_data'].append({"Document":str(updated_doc)})

                else:
                    return Response(doc_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                Doc =Document.objects.get(id=doc_serializer.data['id']).id if  updated_doc not in ["null",None,""] else None
            else:
                Doc = document['id']
            
        elif updated_doc!=None and document==None:
            document_data = {"company_id":Company.objects.get(name = "linkintime").id,"document":updated_doc}
            doc_serializer = DocumentSerializer(data =document_data)

            if doc_serializer.is_valid():
                doc_serializer.save()
                
                history['previous_data'].append({"Document":None}),history['current_data'].append({"Document":str(updated_doc)})
                
            else:
                return Response(doc_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            Doc =Document.objects.get(id=doc_serializer.data['id']).id if  updated_doc not in ["null",None,""] else None

        if updated_doc ==None:
            history['previous_data'].append({"Document":str(document['document']) if document!=None else None}),history['current_data'].append({"Document":None})
            Doc = None
        answer_data = {'context_id':uuid_context,
                    'answer':updated_answer,
                    'url':updated_url if updated_url not in ["null",None,""] else None ,
                    'document':Doc}
        
        for key in ["url","answer"]:
            if answer[key]!= answer_data[key]:
                    history['previous_data'].append({str(key):str(answer[key])}),history['current_data'].append({str(key):str(answer_data[key])})
        
        answer_serializer = AnswersSerializer(answer_instance,data =answer_data)
        
        if context_serializer.is_valid() and tags_TagSerializer.is_valid() and answer_serializer.is_valid():
            
            context_serializer.save()
            
            tags_TagSerializer.save()
            answer_serializer.save()

            user_type=Group.objects.get(user = request.user.id)
            USER_LOGS.objects.create_user_logs(request.user,str(user_type),"updated "+str(context)+" question",history,True)
            
            return Response(f"Updated {update_question} question successfully!",status=200)
        else:
            return Response({"context error":context_serializer.errors,
                             "tags error": tags_TagSerializer.errors,
                             "answer error":answer_serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST)


class AdminPanelContextCreation(APIView):
    parser_classes = ([MultiPartParser, FormParser,JSONParser,])
    def get(self, request, format=None):

        return Response({
                        "question":None,
                        "prev_context":None,
                        "leaf_node":None,
                        "inputs_required":None,
                        "answer":None,
                        "company_name":None,
                        "document":None,
                        "url":None,
                        "keywords":None},status=200)

    
    # @parser_classes([MultiPartParser, FormParser])
    def post(self, request, format=None):
        
        context_name    = request.data['question'].strip()
        prev_context    = request.data['prev_context']
        leaf_node       = request.data['leaf_node']
        inputs_required = request.data['inputs_required']
        keywords        = [i.strip() for i  in request.data['keywords'].split(',')]
        url             = request.data['url']
        doc             = request.data['document']
        answer          = request.data['answer']
        company_name    = request.data['company_name']

        context_data = {
            "uuid"          :str(uuid.uuid4()),
            "context_name"  :context_name,
            "prev_context"  :prev_context if prev_context not in [None,"null","","None"] else None,
            "leaf_node"     :True,
            "inputs_required":inputs_required
            }
        context_serializer = ContextSerializer(data=context_data)

        if context_serializer.is_valid():
            if Context.objects.filter(context_name=context_name).exists()==False:
                context_uuid = context_serializer.save()
            else:
                return Response({"Same question exists"},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"context error":context_serializer.errors},status=status.HTTP_400_BAD_REQUEST)

        # context_uuid =Context.objects.get(context_name=context_name).uuid

        tags_data ={
            "context_id":context_uuid,
            "tags":keywords
            }

        frequency_data ={
            "context_id":context_uuid,
            "frequency":0
            }
        doc_id = ""
        if doc:
            doc_data = {
                "company_id":Company.objects.get(name=company_name).id,
                "document":doc
                }
            doc_serializer = DocumentSerializer(data = doc_data)
            if doc_serializer.is_valid():
                doc_serializer.save()
            else:
                return Response({"document error":doc_serializer.errors},status=status.HTTP_400_BAD_REQUEST)

            doc_id =Document.objects.filter(id=doc_serializer.data["id"]).values('id').first()
        
        answer_data = {
                       "context_id":context_uuid,
                       'answer':answer,
                       'url':url,
                       'document':doc_id["id"] if doc_id else None
                       }
        
        tags_TagSerializer = TagSerializer(data = tags_data)
        
        answer_serializer = AnswersSerializer(data= answer_data)
        Frequency_Serializer = FrequencySerializer(data = frequency_data)
        freq_exists = Frequency.objects.filter(context_id=context_uuid).exists()
        answer_exists = Answers.objects.filter(context_id=context_uuid).exists()
        tags_exists = Tag.objects.filter(context_id=context_uuid).exists()


        if Frequency_Serializer.is_valid() and tags_TagSerializer.is_valid() and answer_serializer.is_valid():
            if freq_exists==False and answer_exists==False and tags_exists==False:
                Frequency_Serializer.save()
                tags_TagSerializer.save()
                answer_serializer.save()
                
                user_type=Group.objects.get(user = request.user.id)

                USER_LOGS.objects.create_user_logs(request.user,str(user_type),"Added "+context_name+" context",{"previous_data":[{"Question":None}],"current_data":[{"Question":context_name}]},True)

                nodes  = Answers.objects.select_related('context_id').filter(context_id__context_name=context_name)
                for y in nodes:
                    obj = {"status": f"Added {context_name} question successfully!","uuid": y.context_id.uuid, "question": y.context_id.context_name, "answer": y.answer }
                return Response(obj,status=201)
        else:
            return Response({"frequency error":Frequency_Serializer.errors,
                             "tags error": tags_TagSerializer.errors,
                             "answer error":answer_serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST)


class ConextDuplicationView(APIView):
    '''
    creates a duplicates of a context along with
    all it's related models. 
    '''
    def post(self, request, *args, **kwargs):
        update_question  = request.data['question'].strip()
        updated_tags     = [i.strip() for i  in request.data['keywords'].split(',')]
        updated_url      = request.data['url']
        updated_doc      = request.data['document']
        updated_answer   = request.data['answer']
        prev_context     = request.data['prev_context'] if request.data['prev_context'] else None
        empty            = ["null",None,""]
        company_id       = Company.objects.get(name = "linkintime").id
        
        if updated_doc in empty  : updated_doc=None
        
        if Context.objects.filter(context_name=update_question).exists():
            return Response({"Same question already exists!"},status=status.HTTP_400_BAD_REQUEST)

        context = {'context_name':update_question, 'uuid':str(uuid.uuid4()),'prev_context':prev_context,'leaf_node':True,'inputs_required':False}
        
        context_serializer = ContextSerializer(data = context)
        tags = {'context_id':context['uuid'],"tags":updated_tags}
        tags_TagSerializer = TagSerializer(data = tags)

        document = Document.objects.filter(document=updated_doc).values('document','id').first()
        if updated_doc !=None  and document!=None:
            if updated_doc!=str(document['document']):
                
                document_data = {"company_id":company_id,"document":updated_doc}
                doc_serializer = DocumentSerializer(data =document_data)
            
                if doc_serializer.is_valid():
                    doc_serializer.save()
                    
                else:
                    return Response(doc_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                Doc =Document.objects.get(id=doc_serializer.data['id']).id if  updated_doc not in ["null",None,""] else None
            else:
                Doc = document['id']
            
        elif updated_doc!=None and document==None:
            document_data = {"company_id":company_id,"document":updated_doc}
            doc_serializer = DocumentSerializer(data =document_data)

            if doc_serializer.is_valid():
                doc_serializer.save()
                
            else:
                return Response(doc_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
            Doc =Document.objects.get(id=doc_serializer.data['id']).id if  updated_doc not in ["null",None,""] else None

        if updated_doc ==None:
            Doc = None
        answer_data = {'context_id':context['uuid'],
                    'answer':updated_answer,
                    'url':updated_url if updated_url not in ["null",None,""] else None ,
                    'document':Doc}
        
        answer_serializer = AnswersSerializer(data =answer_data)

        frequency_data = {'context_id':context['uuid'],'frequency':0}
        frequency_serializer = FrequencySerializer(data = frequency_data)
        if context_serializer.is_valid():
            context_serializer.save()
        else:
            return Response({"context error":context_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        
        if answer_serializer.is_valid():
            answer_serializer.save()
        else:
            return Response({"context error":answer_serializer.errors},status=status.HTTP_400_BAD_REQUEST)
        

        if tags_TagSerializer.is_valid() and frequency_serializer.is_valid():
            
            tags_TagSerializer.save()
            
            frequency_serializer.save()

            user_type=Group.objects.get(user = request.user.id)
            USER_LOGS.objects.create_user_logs(request.user,str(user_type),"Created a duplicate of "+str(context['context_name'])+" question.",{"previous_data":[{"context_duplication":"No duplicates"}],"current_data":[{"context_duplication":f"Duplicated {str(context['context_name'])}"}]},True)
            
            nodes  = Answers.objects.select_related('context_id').filter(context_id__context_name=update_question)
            for y in nodes:
                obj = {"status": f"Created a duplicate of {str(context['context_name'])} question.", "uuid": y.context_id.uuid, "question": y.context_id.context_name, "answer": y.answer }
            return Response(obj, status=200)
        else:
            return Response({
                             "tags error": tags_TagSerializer.errors,
                             "frequency error":frequency_serializer.errors
                            },status=status.HTTP_400_BAD_REQUEST)

