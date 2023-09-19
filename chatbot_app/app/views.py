from re import A, compile, sub, escape, IGNORECASE
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models.functions import Cast
from django.db.models.functions import Concat
from django.db.models import F, Q
from django.db import models
import uuid
from django.contrib.auth import get_user_model
from rest_framework import status
import random
from collections import Counter
from admin_panel_app.app.pagination import CustomPagination, ISINPagination
import jwt
from chatbot_app.models import (Tag, Frequency,
                                Company, Rating,
                                Document, Conversation,
                                Answers, Context,UntaggedQuestions, 
                                FocusAddress, Feedback, Isin,BranchAdress)
from chatbot_app.app.serializers import (TagSerializer,
                                        CompnaySerializer,
                                        RatingSerializer,
                                        DocumentSerializer,
                                        ConversationSerializer,
                                        AnswersSerializer,
                                        FrequencySerializer,
                                        ContextSerializer,QuestionsSerializer,
                                        FeedbackSerializer, ISINSerializer, BranchAdressSerializer)

from admin_panel_app.app.permissions import HasGroupPermission
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk import regexp_tokenize
import nltk
from rest_framework.throttling import ScopedRateThrottle 
from rest_framework.exceptions import PermissionDenied

# nltk.download('stopwords')
# nltk.download('punkt')

UserModel = get_user_model()


class CustomModelViewSet(ModelViewSet):
    def dispatch(self, request, *args, **kwargs):
        header = self.request.META.get('HTTP_AUTHORIZATION', None)

        if header is None:
            raise PermissionDenied("No Auth Token provided. Refresh the chatbot")
        
        header = header.replace('Bearer ', '')
        session_id = jwt.decode(header, "secret", algorithms="HS256")['session_id']

        if not Conversation.objects.filter(session_id=session_id).exists():
            raise PermissionDenied("Invalid Auth Token")

        
        response = super().dispatch(request, *args, **kwargs)
        return response
    

class CustomAPIDispatch(APIView):
    def dispatch(self, request, *args, **kwargs):
        header = self.request.META.get('HTTP_AUTHORIZATION', None)

        if header is None:
            raise PermissionDenied("No Auth Token provided. Refresh the chatbot")
        
        header = header.replace('Bearer ', '')
        session_id = jwt.decode(header, "secret", algorithms="HS256")['session_id']

        if not Conversation.objects.filter(session_id=session_id).exists():
            raise PermissionDenied("Invalid Auth Token")

        
        response = super().dispatch(request, *args, **kwargs)
        return response

def conversation_logger(session_id, user_input, conv_response):
    conv = []
    conv_data = {
                    "session_id" : session_id,
                    "selected"   : user_input,
                    "response"   : conv_response
                }
    
    if Conversation.objects.filter(session_id=session_id).exists():
        conv_instance = Conversation.objects.get(session_id=session_id)
        pre_res = Conversation.objects.filter(session_id=session_id).values_list('conversation_data').first()
        pre_res[0].append(conv_data)
        
        conv_obj = {
            "session_id"        : session_id,
            "inputs"            : None,
            "output"            : None,
            "conversation_data" : pre_res[0]
        }

        conversation_serializer = ConversationSerializer(conv_instance,data =conv_obj)
        if conversation_serializer.is_valid():
            conversation_serializer.save()
        else:
            return Response(conversation_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    else:
        conv.append(conv_data)
        conv = {
            "session_id"        : session_id,
            "inputs"            : None,
            "output"            : None,
            "conversation_data" : conv
        }
        
        conversation_serializer = ConversationSerializer(data =conv)
        if conversation_serializer.is_valid():
            conversation_serializer.save()
        else:
            return Response(conversation_serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class BannerView(CustomAPIDispatch):
    '''
    API to provide response to banner options
    '''
    throttle_classes = [ScopedRateThrottle]
    throttle_scope   = 'banner_scope'

    def get(self, request, format=None):
        data = list(Context.objects.filter(context_name='KYC').values('uuid', 'context_name').all())
        data.append(list(Context.objects.filter(context_name='IEPF').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Public / Rights Issues / Buyback Offers').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Bond Servicing').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Depository Services').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Registry').values('uuid', 'context_name').all())[0])
        # data.append(list(Context.objects.filter(context_name='Disclaimer').values('uuid', 'context_name').all())[0])
        # data = Context.objects.filter(prev_context = None).exclude(context_name='Service Request Form').values('uuid', 'context_name').all()
        res = []
        for i in data:
            resp = {}
            resp["name"] = i['context_name']
            resp["uuid"] = i['uuid']
            resp["status"] = "active"
            res.append(resp)

        # res.append({"name" : "Registry", "status": "inactive"})
        res.append({"name" : "CSR", "status": "inactive"})
        res.append({"name" : "Insta", "status": "inactive"})
        res.append({"name" : "Insta-meet", "status": "inactive"})
        res.append({"name" : "Digital Signature", "status": "inactive"})
        disclaimer = list(Context.objects.filter(context_name='Disclaimer').values('uuid', 'context_name').all())[0]
        res.append({"name" : disclaimer['context_name'], "uuid": disclaimer['uuid'], "status": "inactive"})
        return Response(res, status=200)

class MainMenuView(CustomAPIDispatch):
    '''
    API to provide response to main menu options
    '''
    throttle_classes = [ScopedRateThrottle]
    throttle_scope   = 'main_menu_scope'

    def get(self, request, format=None):
        data = list(Context.objects.filter(context_name='KYC').values('uuid', 'context_name').all())
        data.append(list(Context.objects.filter(context_name='IEPF').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Public Issues').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Rights Issues').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Bond Servicing').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Depository Services').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Buy-Back').values('uuid', 'context_name').all())[0])
        data.append(list(Context.objects.filter(context_name='Registry').values('uuid', 'context_name').all())[0])
        resp = {}
        for i in data:
            resp[(i['context_name']).strip("-")] = list(Context.objects.filter(prev_context = i['uuid']).values('uuid', 'context_name').order_by('context_name').all())
        return Response(resp, status=200)

class WorkFlowView(APIView):
    '''
    API to provide response to workflow
    resquest(session_id,selected_context,typed_msg)
    '''

    def add_branch_adress(self, answer,host):
        if '__Total__Address' not in answer:
            return answer
        elif 'All'==answer.split('-')[-1]:
            answer = answer.replace('__Total__Address-All','<br/><br/>')
            addresses = BranchAdress.objects.filter(company__name=host).values('branch_name','total_address').exclude(branch_id ='179-1').exclude(branch_id ='194-1').all()
            for adress in addresses:
                answer+=f'''
                <div class="popup"><strong>{adress['branch_name']}</strong></div><div class="popup">{adress['total_address']}</div>
                '''
                answer += "<p> <br/></p>"

            return answer
        else:
            branch_name =answer.split('-')[-1]
            addresses = BranchAdress.objects.filter(company__name=host,branch_name=branch_name.upper()).values('branch_name','total_address').first()
            answer = answer.replace(str(answer.split('\n')[-1]),'<br/><br/>')
            if not addresses:
                return f"<p>{host} does not happen to have a branch in {branch_name} location.<br/>Please search for the key word 'our branch addresses' to find all the branchs.</p>"
            answer += addresses['total_address']
            return answer
        


    def add_focus_address(self, answer, host):
        focus_address = '''<a href="/" rel="noopener noreferrer" target="_blank">Focus Address</a>'''
        email_r_t     = '''<a href="/" rel="noopener noreferrer" target="_blank">Email-R-T</a>'''
        email_public  = '''<a href="/" rel="noopener noreferrer" target="_blank">Email-Public-Issues</a>'''
        email_bonds   = '''<a href="/" rel="noopener noreferrer" target="_blank">Email-Bonds</a>'''

        if answer.find(focus_address):
            address = FocusAddress.objects.filter(company_id__name=host).values('focus_answer').first()['focus_answer']
            answer = answer.replace(focus_address, address)

        if answer.find(email_r_t):
            address = FocusAddress.objects.filter(company_id__name=host, topic="R and T").values('contact_info').first()
            if address: 
                answer = answer.replace(email_r_t, address['contact_info'])
            else:
                answer = answer.replace(email_r_t, "")


        if answer.find(email_public):
            address = FocusAddress.objects.filter(company_id__name=host, topic="Public Issues").values('contact_info').first()
            if address: 
                answer = answer.replace(email_public, address['contact_info'])
            else:
                answer = answer.replace(email_public, "")

        if answer.find(email_bonds):
            address = FocusAddress.objects.filter(company_id__name=host, topic="Bonds").values('contact_info').first()
            if address: 
                answer = answer.replace(email_bonds, address['contact_info'])
            else:
                answer = answer.replace(email_bonds, "")

        return answer
            

    def update_url_as_per_company(self, answer, url, host):

        invalid_values = [ "", None, "null" ]
        prefix         = compile(escape('link_'), IGNORECASE)

        if host =="tcplindia":
            answer = answer.replace("helpdesk@tcplindia.co.in","csg-unit@tcplindia.co.in")
            answer = answer.replace("kyc@linkintime.co.in","kyc@tcplindia.co.in")
            answer = answer.replace("W-Link","W-TCPL")
            answer = answer.replace("web.linkintime.co.in/admin/DownloadFiles","www.tcplindia.co.in/admin/DownloadFiles")

            if "https://web.linkintime.co.in/website/Chatbot" in answer:
                answer = prefix.sub("TCPL_", answer)

            if url not in invalid_values:
                url = url.replace("linkintime.co.in","tcplindia.co.in")
                    
                
        elif host =="unisec":
            answer = answer.replace("helpdesk@tcplindia.co.in","info@unisec.in")
            answer = answer.replace("kyc@linkintime.co.in","kyc@unisec.in")
            answer = answer.replace("W-Link","W-Unisec")
            answer = answer.replace("web.linkintime.co.in/admin/DownloadFiles","unisec.in/admin/DownloadFiles")

            if "https://web.linkintime.co.in/website/Chatbot" in answer:
                answer = prefix.sub("UNSC_", answer)

            if url not in invalid_values:
                url = url.replace("linkintime.co.in","unisec.in")
                

        elif host =="skdc-consultants":
            answer = answer.replace("helpdesk@tcplindia.co.in","info@skdc-consultants.com")
            answer = answer.replace("kyc@linkintime.co.in","kyc@skdc-consultants.com")
            answer = answer.replace("W-Link","W-SKDC")
            answer = answer.replace("web.linkintime.co.in/admin/DownloadFiles","www.skdc-consultants.com/admin/DownloadFiles")

            if "https://web.linkintime.co.in/website/Chatbot" in answer:
                answer = prefix.sub("SKDC_", answer)
            
            if url not in invalid_values:
                url = url.replace("linkintime.co.in","skdc-consultants.com")


        else:
            if "https://web.linkintime.co.in/website/Chatbot" in answer:
                answer = prefix.sub("LINK_", answer)

        return answer, url


    def search_for_client(self, typed_msg):
        found = False
        bot_msg = ""
 
        res = Isin.objects.filter(client__istartswith=typed_msg).exclude(client='__last__updated').values_list('branch__name', 'client', 'isin', 'status', 'cin_number', "branch_code").first()
  
        if res:
            found = True
            Frequency.objects.filter(context_id__context_name='Find ISIN Number').update(frequency=F('frequency') + 1)
            company, client, isin, status, cin, branch_code = res
   
            address = BranchAdress.objects.filter(company__name=company, branch_id=branch_code).values('total_address').first()
            bot_msg = f"For any queries related to <strong>'{client}'</strong><br/> Please contact: <br/>" + address['total_address']

        return bot_msg, found

    def get(self, request, format=None):
        return Response({
                "session_id": "",
                "selected_context":"",
                "typed_msg":""
            }, status=200)
    
    def authenticate(self, header):
        error = ""
        if header is None:
            error = "No Auth Token provided. Refresh the chatbot"
        
        header = header.replace('Bearer ', '')
        session_id = jwt.decode(header, "secret", algorithms="HS256")['session_id']

        if not Conversation.objects.filter(session_id=session_id).exists():
            error = "Invalid Auth Token"
        
        return session_id, error
    
    def parse_using_nltk(self, typed_msg):

        # tokenize the given user input and remove all the stop words.
        text_tokens       = regexp_tokenize(typed_msg, pattern=r"\s", gaps=True)
        tokens_without_sw = [word for word in text_tokens if not word in stopwords.words()]
        
        tagObj = []  
        res    = []
        for x in tokens_without_sw:
            if len(x) == 1: continue
            res.append(list(Tag.objects.annotate(name=Concat(Cast('tags', models.TextField()),Cast('context_id__context_name', models.TextField())),)\
                    .filter(name__iregex=r"\y{0}\y".format(x)).distinct('context_id__context_name').values_list('context_id', flat=True)))
        
        res = [ x for x in res if x]

        # if res: tagObj = list(set.intersection(*map(set, res)))
        if res: 
            counter = Counter(res[0])
            for i in res[1:]:
                counter.update(i)
            tagObj = [x[0] for x in counter.most_common()]
            tagObj = tagObj[:5]
        return tagObj
    
    def save_to_untagged_question(self, typed_msg_org):
        if UntaggedQuestions.objects.filter(un_taged_question = typed_msg_org).exists():
            UntaggedQuestions.objects.filter(un_taged_question = typed_msg_org).update(frequency=F('frequency') + 1)
                        
        else:
            data = {"un_taged_question":typed_msg_org}
            serializer = QuestionsSerializer(data=data)
            if serializer.is_valid():
                serializer.save()

        # Select 1 of 3 contexts in random
        ContextList      =  list(Context.objects.filter(context_name__contains = "key word not found").values('uuid', 'context_name').all())
        option_id = random.choice([0, 1, 2, 3])
        select = str(ContextList[option_id]['uuid'])
        context_id  =  select if "option 3" in ContextList[option_id]['context_name']  else None

        return context_id, select
    
    def response_generation_with_choices(self, tagObj, session_id, selected_context, typed_msg, is_untagged):
        
        options = []
        bot_message = []

        for i in tagObj:
            context_ind = Context.objects.filter(uuid = str(i)).values('context_name','uuid','prev_context','leaf_node','inputs_required').first()
            # uncomment -2023
            # if context_ind["context_name"].startswith("-2023"):
            #     continue
            options.append(context_ind)
        
        msg_gound = [""] * 8 +  [
            'Let me find you the right answer!',
            'Sure. I can assist you with any query related to ' + typed_msg,
            'Kindly select from below to help you further',
            'Kindly choose the specific items from the below provided options for which you are seeking information.',
            'Sure! I can help you with your request.',
            'Alright, please select from below to help you further.',
            f'<p>Okay, what is your question about?</p><p>Ah yes!! {typed_msg}</>'
        ]

        bot_message.append(random.choice(msg_gound))

        response = {
                "session_id"        : session_id,
                "selected_context"  : selected_context,
                "typed_msg"         : typed_msg,
                "bot_message"       : bot_message,
                "is_untagged"       : is_untagged,
                "options"           : sorted(options, key=lambda d: d['context_name']),
                "h_view"            : True,
                "document"          : "null",
                "answer_url"        : "null"
                }
        conv_response = {
            "bot_message"       : bot_message,
            "options"           : [str(i['context_name']) for i in options],
            "document"          :  "null",
            "answer_url"        : "null"
            }
        return response, conv_response
    

    def generate_response_to_single_context(self, session_id, selected_context, typed_msg, bot_message, input_required, context_id, select, host, typed_msg_org):
        search_context = Context.objects.filter(uuid = context_id).values('context_name','leaf_node').first()

        if typed_msg_org and not typed_msg:
            bot_message.append(f"Unacceptable keyword: {typed_msg_org}. Please select from the menu.")
        
        if search_context and search_context['context_name'] == 'Main Menu':  
            context_id = None
            

        if search_context and search_context['leaf_node'] == True:
            context_id = Context.objects.filter(context_name = "closure").values('uuid').first()['uuid']
            bot_message.append("Is there anything else that I can help you with?")

        # .exclude(context_name__startswith="-2023") [-2023]
        options     = Context.objects.filter(prev_context = context_id).\
                                values('context_name','uuid','prev_context','leaf_node','inputs_required').order_by('context_name')
        
        answer      = Answers.objects.filter(context_id = select).values('answer', 'document__document', 'url').first()

        if answer:
            answer['answer'], answer['url'] = self.update_url_as_per_company(answer['answer'], answer['url'], host)
            answer['answer']  = self.add_focus_address(answer['answer'], host)
            answer['answer']  = self.add_branch_adress(answer['answer'],host) 

        if answer: bot_message.insert(0,answer['answer'])
        doc = Document.objects.get(document = answer['document__document']).document.url if answer and answer['document__document'] else "null"
        
        
        # increment the frequency of that context by 1 
        if select and not Frequency.objects.filter(context_id = select).exists():
            Frequency.objects.create(context_id = Context.objects.get(uuid = select), frequency = 0)
        Frequency.objects.filter(context_id = select).update(frequency=F('frequency') + 1)   
        
        response = {
            "session_id"        : session_id,
            "selected_context"  : selected_context,
            "typed_msg"         : typed_msg,
            "bot_message"       : bot_message,
            "is_untagged"       : False,
            "options"           : options,
            "input_required"    : input_required,
            "document"          : doc if doc else "null",
            "h_view"            : True if len(options) > 8 else False,
            "answer_url"        : answer['url'] if answer else "null"
            }
        
        conv_response = {
            "bot_message"       : bot_message,
            "options"           : [str(i['context_name']) for i in options],
            "document"          : doc if doc else "null",
            "answer_url"        : answer['url'] if answer else "null"
            }
        return response, conv_response  
    
    
    def post(self, request, format=None):
        # request parameters
        session_id          = request.data.get('session_id')
        selected_context    = request.data.get('selected_context')
        typed_msg           = request.data.get('typed_msg').lower().strip()
        host                = request.data.get('host')

        ''' Authentication'''
        header = self.request.META.get('HTTP_AUTHORIZATION', None)

        session_id, error = self.authenticate(header)

        if error: raise PermissionDenied(error)
        if session_id == "": session_id = str(uuid.uuid4())
        
        # logic starts here
        context_id, select, user_input  = None, None, None
        is_untagged, input_required     = False, False
        bot_message                     = []
        invalid_values                  = ["", None, "null"]

        # keep a copy of original user message received. On the copy created, remove all charactes except alphabets, . and @
        typed_msg_org = typed_msg
        typed_msg = sub('[^a-zA-Z0-9.@_\- ]', '', typed_msg)
        typed_msg = typed_msg.replace("office address", "branch address").replace("office location", "branch address")
        
        
        # if both selected_context and typed_msg is null then retrieve main menu options
        if selected_context in invalid_values and typed_msg in invalid_values:
            context_id  = None
            
        # if selected_context is available. i.e, user has clicked a button.  
        elif selected_context not in invalid_values:
            if selected_context == "IPO Allotment Status": selected_context = Context.objects.get(context_name = selected_context).uuid
            context_id = select = selected_context
            user_input          = Context.objects.get(uuid = context_id).context_name
            input_required      = Context.objects.get(uuid = context_id).inputs_required

        # if typed_msg is available,. i.e, user has written a message in text area.
        elif typed_msg not in invalid_values:
    
            tagObj      = list(Tag.objects.annotate(name=Concat(Cast('tags', models.TextField()),Cast('context_id__context_name', models.TextField())),)\
                            .filter(name__iregex=r"\y{0}\y".format(typed_msg)).distinct('context_id__context_name').values_list('context_id', flat=True))

            user_input  = typed_msg
            
            # if there are no tag matches from database, then parse the data using NLTK and then match in database.
            if len(tagObj) == 0:
                tagObj = self.parse_using_nltk(typed_msg)

            # if there is no tag matches found even after parsing the user data, 
            # then check in client table to match ISIN number and CIN number
            if len(tagObj) == 0:
                bot_msg, found = self.search_for_client(typed_msg)
                if found:
                    bot_message.append(bot_msg)
                    user_input = typed_msg

                else:
                    # saving the un tagged question into database
                    context_id, select = self.save_to_untagged_question(typed_msg_org)
                    is_untagged = True
            # if there is a single match in database, use the same.   
            elif len(tagObj) == 1:
                context_id  =  str(tagObj[0])
                select      =  str(tagObj[0])
                input_required = Context.objects.get(uuid = context_id).inputs_required
            # if there are more than one match in database
            else:
                response, conv_response = self.response_generation_with_choices(tagObj, session_id, selected_context, typed_msg, is_untagged)
                response = Response(response)
                conversation_logger(session_id, typed_msg_org, conv_response)
                return response
                
        # if there is a single match in database, then fetch data related to that context and send response.
        response, conv_response = self.generate_response_to_single_context(session_id, selected_context, typed_msg, bot_message, input_required, context_id, select, host, typed_msg_org)
        
        #log the conversation
        log_data = user_input if user_input else typed_msg_org
        conversation_logger(session_id, log_data, conv_response)
        
        return Response(response,status=200)
    


class RatingView(CustomAPIDispatch):
    """
    Rating view is used to take ratings for chatbot from user.
    """
    throttle_classes = [ScopedRateThrottle]
    throttle_scope   = 'rating_scope'
    def get(self, request, format=None):
        """
        Get method to return an empty rating response.
        """
        return Response({"rating":""}, status=200)

    def post(self, request, format=None):
        """
        Post method to update the rating for the chatbot.
        """
        rating = request.data["rating"]
        if rating in "rating_5":
            Rating.objects.filter(pk=1).update(rating_5=F("rating_5")+1)

        elif rating in "rating_4":
            Rating.objects.filter(pk=1).update(rating_4=F("rating_4")+1)
        
        elif rating in "rating_3":
            Rating.objects.filter(pk=1).update(rating_3=F("rating_3")+1)

        elif rating in "rating_2":
            Rating.objects.filter(pk=1).update(rating_2=F("rating_2")+1)

        elif rating in "rating_1":
            Rating.objects.filter(pk=1).update(rating_1=F("rating_1")+1)


        return Response({"Thanks for your rating."},status=200)


class ContextView(CustomModelViewSet):
    '''API to allow CRUD operations on Context model'''

    queryset           = Context.objects.all()
    serializer_class   = ContextSerializer

class TagView(CustomModelViewSet):
    '''API to allow CRUD operations on Tag model'''

    queryset           = Tag.objects.all()
    serializer_class   = TagSerializer


class FrequencyView(CustomModelViewSet):
    '''API to allow CRUD operations on Frequency model'''

    queryset            = Frequency.objects.all()
    serializer_class    = FrequencySerializer



class CompanyView(CustomModelViewSet):
    '''API to allow CRUD operations on Company model'''

    queryset            = Company.objects.all()
    serializer_class    = CompnaySerializer


class DocumentView(CustomModelViewSet):
    '''API to allow CRUD operations on Document model'''

    queryset            = Document.objects.all()
    serializer_class    = DocumentSerializer


class ConversationView(CustomModelViewSet):
    '''API to allow CRUD operations on Conversation model'''

    queryset            = Conversation.objects.all()
    serializer_class    = ConversationSerializer


class AnswersView(CustomModelViewSet):
    '''API to allow CRUD operations on Answers model'''

    queryset            = Answers.objects.all()
    serializer_class    = AnswersSerializer

class TestView(APIView):
    '''
    provides the server running status. 
    '''
    def get(self, request, format=None):
        return Response({"sucess"},status=200)


class UntaggedQuestionsMailClick(CustomAPIDispatch):
    throttle_classes    = [ScopedRateThrottle]
    throttle_scope      = 'mail_selected'
    def patch(self,request, *args, **kwargs):
        question     = request.data['question']
        UntaggedQuestions.objects.filter(un_taged_question = question).update(mail_click=True)
        return Response(status=200)



class FeedbackView(ModelViewSet):
    queryset            = Feedback.objects.all().order_by('-created_at')
    serializer_class    = FeedbackSerializer
    pagination_class    = CustomPagination
    throttle_classes    = [ScopedRateThrottle]
    throttle_scope      = 'feedback_scope'

    def get_queryset(self):
        start_date = self.request.query_params.get('start_date', None)
        end_date   = self.request.query_params.get('end_date', None)

        queryset = Feedback.objects.filter()
        if start_date and end_date:
            queryset = queryset.filter(created_at__date__range=(start_date, end_date))

        return queryset.all().order_by("-created_at")
    
    def perform_update(self, serializer):
        pk = self.kwargs['pk']
        Feedback.objects.filter(id = pk)
        serializer.save(is_resolved=self.request.data['is_resolved'], partial=True)


class IsinView(ModelViewSet):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope   = 'isin_scope'

    queryset            = Isin.objects.all().order_by('client')
    serializer_class    = ISINSerializer
    pagination_class    = ISINPagination
    
    def get_queryset(self):
        search   = self.request.query_params.get('search', None)
        order_by = self.request.query_params.get('order_by', None)

        query_set = ""
        if search:
            query_set =  Isin.objects.filter(client__icontains = search).exclude(client='__last__updated').all()
        else:
            query_set = Isin.objects.exclude(client='__last__updated').all()
        
        if order_by:
            query_set = query_set.order_by(str(order_by))
            if search: query_set = query_set[:5]
            
        return query_set

    def create(self, request):
        pk = request.data['client']
        search = request.data['search_by']
        data = Isin.objects.filter(client__icontains=pk).values('client', 'isin', 'status', 'cin_number').first()
        if data:
            res = ""
            if "ISIN" ==  search :
                res += "<p>" + f"{data['isin']} [ {data['status']} ] is the ISIN number for {data['client']}." + "</p>"
            elif "CIN" ==  search: 
                if data['cin_number'] and data['cin_number'] != "nan":
                    res += "<p>" + f"{data['cin_number']} [ {data['status']} ] is the CIN number for {data['client']}." + "</p>"
                else: res += f"<p>CIN number for {data['client']} is not available</p>"
            else:
                res += "<p>" + f"{data['isin']} [ {data['status']} ] is the ISIN number for {data['client']}." + "</p><br/>"
                if data['cin_number'] and data['cin_number'] != "nan": res += "<p>" + f"{data['cin_number']} [ {data['status']} ] is the CIN number for {data['client']}." + "</p>"
                else: res += f"<p>CIN number for {data['client']} is not available</p>"
            Frequency.objects.filter(context_id__context_name='Find ISIN Number').update(frequency=F('frequency') + 1)
            return Response(res)
        return Response({f"ISIN number for {pk} is not found"},status=404)



class BranchAddressView(CustomModelViewSet):
    throttle_classes = [ScopedRateThrottle]
    throttle_scope   = 'branch_scope'
    queryset            = BranchAdress.objects.all().order_by('branch_name')
    serializer_class    = BranchAdressSerializer


    def get_queryset(self):
        host   = self.request.query_params.get('host', None)
        field   = self.request.query_params.get('field', None)
        
        queryset = BranchAdress.objects.filter(company__name=host)
        if field == "address":
            queryset = queryset.values('branch_name', 'branch_address', 'g_maps_link', 'g_maps_iframe')
        if field == "telephone":
            queryset = queryset.values('branch_name', 'phone_number')
        if field == "email":
            queryset = queryset.values('branch_name', 'email_address')

        return queryset.distinct('branch_name')



    def list(self, request):
        serializer = BranchAdressSerializer(self.get_queryset(), many=True)
        response = serializer.data
        bot_message = []

        context_id = Context.objects.filter(context_name = "closure").values('uuid').first()['uuid']
        bot_message.append("Is there anything else that I can help you with?")
        options     = Context.objects.filter(prev_context = context_id).\
                                values('context_name','uuid','prev_context','leaf_node','inputs_required').order_by('context_name')


        response.append({"options": options, "bot_message"       : bot_message})
        return Response(response)


class CreateToken(APIView):
    def get(self,request, *args, **kwargs):
        session_id = str(uuid.uuid4())
        encoded_jwt = jwt.encode({"session_id": session_id}, "secret", algorithm="HS256")
        conv = {
                "session_id"        : session_id,
                "inputs"            : None,
                "output"            : None,
                "conversation_data" : []
            }
            
        conversation_serializer = ConversationSerializer(data =conv)
        if conversation_serializer.is_valid():
            conversation_serializer.save()
        else:
            return Response(conversation_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

        return Response({"token": encoded_jwt})