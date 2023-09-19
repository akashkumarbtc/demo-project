from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile, TemporaryUploadedFile


from chatbot_app import models
from chatbot_app.app import serializers
from chatbot_app.app import views


class ContextTestCase(APITestCase):
    '''
    Test case for Context model
    '''
    def setUp(self):
        self.context = models.Context.objects.create(uuid           ='e507691c-a4fe-490b-92b8-0a6091be6b99',
                                                    context_name    ="what is KYC?",
                                                    prev_context    ='e507691c-a4fe-490b-92b8-0a6091be6b99',
                                                    leaf_node       =True,
                                                    inputs_required =False) 

    def test_context_creat(self):
        data = {
            "uuid"              :'e507691c-a4fe-490b-92b8-0a6091be6b88',
            "context_name"      :"what?",
            "prev_context"      :'e507691c-a4fe-490b-92b8-0a6091be6b99',
            "leaf_node"         :True,
            "inputs_required"   :False
        }

        response = self.client.post(reverse('CONTEXT'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_context_list(self):

        response = self.client.get(reverse('CONTEXT'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_context_individual(self):

        response = self.client.get(reverse('CONTEXT'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_context_put(self):
        data_update = {
            "uuid"              :'e507691c-a4fe-490b-92b8-0a6091be6b99',
            "context_name"      :"what is KYC?",
            "prev_context"      :'e507691c-a4fe-490b-92b8-0a6091be6b99',
            "leaf_node"         :True,
            "inputs_required"   :False
        }

        response = self.client.put(reverse('CONTEXT'),data_update)
        self.assertEqual(response.status_code,status.HTTP_200_OK)


    def test_context_delete(self):
        data_update = {
            "uuid"              :'e507691c-a4fe-490b-92b8-0a6091be6b99',
            "context_name"      :"what is KYC?",
            "prev_context"      :'e507691c-a4fe-490b-92b8-0a6091be6b99',
            "leaf_node"         :True,
            "inputs_required"   :False
        }

        response = self.client.delete(reverse('CONTEXT'),data_update)
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)



class CompanyTestCase(APITestCase):
    '''
    Test case for company model
    '''

    def setUp(self):
        self.company = models.Company.objects.create(name  ="TCPL India",
                                                     url   ="https://tcplindia.co.in/")


    def test_company_creat(self):
        data = {
            "name"  : "linkintime",
            "url"   : "https://linkintime.co.in/"
        }

        response = self.client.post(reverse('Company-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_company_list(self):

        response = self.client.get(reverse('Company-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_company_individual(self):

        response = self.client.get(reverse('Company-detail',args=(self.company.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_company_put(self):
        data_update = {
            "name"  : "linkintime-updated",
            "url"   : "https://linkintime.co.in/"
        }

        response = self.client.put(reverse('Company-detail',args=(self.company.id,)),data_update)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_company_delete(self):

        response = self.client.delete(reverse('Company-detail',args=(self.company.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)


class RatingTestCase(APITestCase):
    '''
    Test case for rating model
    '''
    def setUp(self):
        self.rating = models.Rating.objects.create(five_star    =5,
                                                   four_star    =18,
                                                   three_star   =7,
                                                   two_star     =8,
                                                   one_star     =0)

    def test_rating_creat(self):
        data = {
            "five_star"    : 5,
            "four_star"    : 7,
            "three_star"   : 2,
            "two_star"     : 2,
            "one_star"     : 0
        }

        response = self.client.post(reverse('Rating-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_rating_list(self):

        response = self.client.get(reverse('Rating-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_rating_individual(self):

        response = self.client.get(reverse('Rating-detail',args=(self.rating.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_rating_put(self):
        data_update = {
            "five_star"    : 5,
            "four_star"    : 9,
            "three_star"   : 3,
            "two_star"     : 2,
            "one_star"     : 0
        }

        response = self.client.put(reverse('Rating-detail',args=(self.rating.id,)),data_update)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_company_delete(self):

        response = self.client.delete(reverse('Rating-detail',args=(self.rating.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

class FrequencyTestCase(APITestCase):
    '''
    Test case for frequency model
    '''
    
    def setUp(self):
        self.context = models.Context.objects.create(uuid           ='e507691c-a4fe-490b-92b8-0a6091be6b99',
                                                    context_name    ="what is KYC?",
                                                    prev_context    ='e507691c-a4fe-490b-92b8-0a6091be6b99',
                                                    leaf_node       =True,
                                                    inputs_required =False)
        
        self.frequency = models.Frequency.objects.create(context_id = self.context,
                                                         frequency  = 8)

    def test_frequency_creat(self):
        data = {
            "context_id"    :self.context.uuid,
            "frequency"     :7
        }

        response = self.client.post(reverse('Frequency-list'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)

    def test_frequency_list(self):

        response = self.client.get(reverse('Frequency-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_frequency_individual(self):

        response = self.client.get(reverse('Frequency-detail',args=(self.frequency.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_frequency_put(self):
        data_update = {
            "context_id"    :self.context.uuid,
            "frequency"     :10
        }

        response = self.client.put(reverse('Frequency-detail',args=(self.frequency.id,)),data_update)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_company_delete(self):

        response = self.client.delete(reverse('Frequency-detail',args=(self.frequency.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

class TagTestCase(APITestCase):
    '''
    Test case for Tag model
    '''
    def setUp(self):
        self.context = models.Context.objects.create(uuid           ='e507691c-a4fe-490b-92b8-0a6091be6b97',
                                                    context_name    ="what is KYC?",
                                                    prev_context    ='e507691c-a4fe-490b-92b8-0a6091be6b99',
                                                    leaf_node       =True,
                                                    inputs_required =False)
        
        self.context1 = models.Context.objects.create(uuid          ='e507691c-a4fe-490b-92b8-0a6091be6b88',
                                                    context_name    ="KYC?",
                                                    
                                                    leaf_node       =True,
                                                    inputs_required =False)

        self.tags   = models.Tag.objects.create(context_id          = self.context,
                                                tags                = ["what is KYC"])

    def test_tag_create(self):
        data = {
            "tags"      :'["what is"]',
            "context_id": self.context1.uuid
        }

        response = self.client.post(reverse('TagS-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

        data = {
            "tags"      :'["what is"]',
            "context_id": self.context.uuid
        }

        response = self.client.post(reverse('TagS-list'),data)
        self.assertEqual(response.status_code,status.HTTP_400_BAD_REQUEST)
        
        
    def test_tag_list(self):

        response = self.client.get(reverse('TagS-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_tag_individual(self):

        response = self.client.get(reverse('TagS-detail',args=(self.tags.id,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_tag_put(self):
        data_update = {
            "context_id"    :self.context.uuid,
            "tags"      :'["what is KYC","what"]'
        }

        response = self.client.put(reverse('TagS-detail',args=(self.tags.id,)),data_update)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_tag_delete(self):

        response = self.client.delete(reverse('TagS-detail',args=(self.tags.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)



class ConversationTestCase(APITestCase):
    '''
    Test case for Conversation model
    '''
    def setUp(self):
        self.conversation = models.Conversation.objects.create(uuid              ='e507691c-a4fe-490b-92b8-0a6091be6b98',
                                                               session_id        ="xvvb",
                                                               inputs            ='[{"name":"pan","type":"varchar","max_char":"10","value":""},{"name":"OTP","type":"numeric","max_char":"x","value":""},{"name":"DPID","type":"varchar","max_char":"16","value":""}]',
                                                               output            ='{"name": "pan"}',
                                                               conversation_data ='{"session_id" : "","selected"   : "","response"   : ""}'
                                                               )

    def test_conversation_create(self):
        data = {
            "uuid"              : 'e507691c-a4fe-490b-92b8-0a6091be6b79',
            "session_id"        : "xyz",
            "inputs"            :'[{"name":"pan","type":"varchar","max_char":"10","value":""},{"name":"OTP","type":"numeric","max_char":"x","value":""},{"name":"DPID","type":"varchar","max_char":"16","value":""}]',
            "output"            : '{"name": "pan"}',
            "conversation_data" : '{"session_id" : "","selected"   : "","response"   : ""}'
        }

        response = self.client.post(reverse('Conversation-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    def test_conversation_list(self):

        response = self.client.get(reverse('Conversation-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_conversation_individual(self):

        response = self.client.get(reverse('Conversation-detail',args=(self.conversation.uuid,)))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_conversation_put(self):
        data_update = {
            "uuid"              : 'e507691c-a4fe-490b-92b8-0a6091be6b98',
            "session_id"        : "xyz-updated",
            "inputs"            :'[{"name":"pan","type":"varchar","max_char":"10","value":""},{"name":"OTP","type":"numeric","max_char":"x","value":""},{"name":"DPID","type":"varchar","max_char":"16","value":""}]',
            "output"            : '{"name": "pan"}',
            "conversation_data" : '{"session_id" : "","selected"   : "","response"   : ""}'
        }

        response = self.client.put(reverse('Conversation-detail',args=(self.conversation.uuid,)),data_update)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_conversation_delete(self):

        response = self.client.delete(reverse('Conversation-detail',args=(self.conversation.uuid,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)


class DocumentTestCase(APITestCase):
    '''
    Test case for company model
    '''
    def setUp(self):
        
        self.company = models.Company.objects.create(name           ="TCPL India",
                                                     url            ="https://tcplindia.co.in/")

        self.doc     = models.Document.objects.create(company_id    = self.company,
                                                      document       ="null"
                                                    )

    def test_document_creat(self):
        

        data = {
            "company_id"    : self.company.id,
            }

        response = self.client.post(reverse('Document-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_document_list(self):

        response = self.client.get(reverse('Document-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_document_delete(self):

        response = self.client.delete(reverse('Document-detail',args=(self.doc.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)
    


class AswersTestCase(APITestCase):
    '''
    Test case for Answers model
    '''
    def setUp(self):
        self.context = models.Context.objects.create(uuid           ='e507691c-a4fe-490b-92b8-0a6091be6b99',
                                                    context_name    ="what is KYC?",
                                                    prev_context    ='e507691c-a4fe-490b-92b8-0a6091be6b99',
                                                    leaf_node       =True,
                                                    inputs_required =False)
        
        self.company = models.Company.objects.create(name           = "TCPL India",
                                                     url            ="https://tcplindia.co.in/")

        self.doc     = models.Document.objects.create(company_id    =self.company,
                                                      document      ="null")
        
        self.answer     = models.Answers.objects.create(context_id     = self.context,
                                                        answer         = "Please select any kyc option"
                                                        )
        
    def test_answers_creat(self):
        data = {
            "context_id"    :self.context.uuid,
            "answer"        :''' In-Person Verification (IPV): by producing the originals to the authorized person of the RTA, who will retain copy(ies) of the document(s).
                                In hard copy: by furnishing self-attested photocopy(ies) of the relevant document, with date.
                                With e-sign:
                                In case your email is already registered with us, you may send the scanned copies of your KYC documents with e-sign at our dedicated email-id: kyc@linkintime.co.in Kindly mention the email subject line as KYC Updation - (Company Name) - Folio No:________________
                                Investors can also upload KYC documents with e-sign on our website''',
            "documnet"      :self.doc,
            "url"           :"https://www.linkintime.co.in/"
        }

        response = self.client.post(reverse('Answers-list'),data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)

    def test_answers_list(self):

        response = self.client.get(reverse('Answers-list'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_answers_delete(self):

        response = self.client.delete(reverse('Answers-detail',args=(self.answer.id,)))
        self.assertEqual(response.status_code,status.HTTP_204_NO_CONTENT)

    
class WorkFlowViewTestCase(APITestCase):
    '''
    Test cases for work flow view
    '''
    def setUp(self):
        self.context    = models.Context.objects.create(uuid            = 'e507691c-a4fe-490b-92b8-0a6091be6b98',
                                                        context_name    = "what is KYC?",
                                                        
                                                        leaf_node       = True,
                                                        inputs_required = False)
        
        self.frequency  = models.Frequency.objects.create(context_id    = self.context,
                                                          frequency     = 8)
        
        self.tags       = models.Tag.objects.create(context_id          = self.context,
                                                    tags                = ["KYC","kyc","k y c"])
        
        self.company    = models.Company.objects.create(name           = "TCPL India",
                                                        url            = "https://tcplindia.co.in/")

        self.doc        = models.Document.objects.create(company_id    = self.company)

        self.answer     = models.Answers.objects.create(context_id     = self.context,
                                                        answer         = "Please select any kyc option"
                                                        )
        
    
    def test_workflow_list(self):

        response = self.client.get(reverse('chatbot_view'))
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_workflow_put(self):

        response = self.client.put(reverse('chatbot_view'))
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_workflow_delete(self):

        response = self.client.delete(reverse('chatbot_view'))
        self.assertEqual(response.status_code,status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_workflow_create(self):
        '''
        test case where selected_context and typed_msg are empty
        '''
        data = {
                "session_id"        :"",
                
              }
        
        response = self.client.post(reverse('chatbot_view'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)

    def test_workflow_selected_create(self):
        '''
        test case where context has been selected
        '''
        data = {
                "session_id"        :"",
                "selected_context"  :"e507691c-a4fe-490b-92b8-0a6091be6b98"
                
              }
        
        response = self.client.post(reverse('chatbot_view'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_workflow_typed_create(self):
        '''
        test case where there is a typed message
        '''
        data = {
                "session_id"  :"",
                "typed_msg"   :"KYC"
                
              }
        
        response = self.client.post(reverse('chatbot_view'),data)
        self.assertEqual(response.status_code,status.HTTP_200_OK)
    
    def test_frequency_updation(self):
        data = {
                "session_id"  :"",
                "typed_msg"   :"KYC"
                
              }

        response = self.client.post(reverse('chatbot_view'),data)
        self.assertEqual(models.Frequency.objects.get(context_id=self.context.uuid).frequency,self.frequency.frequency+1)
        