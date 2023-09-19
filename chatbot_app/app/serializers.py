from chatbot_app.models import (Context, Tag,
                                Frequency, Company,
                                Rating, Document,
                                Conversation, Answers,
                                UntaggedQuestions, Feedback, Isin,BranchAdress)
from rest_framework import serializers

from admin_panel_app.app.serializers import UserLogsSerializer
import re

class ContextSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Context MODEL
    '''
    #uuid = serializers.ReadOnlyField()
    class Meta:
        model   = Context
        fields  = "__all__"
    def create(self, validated_data):

        context = Context.objects.create(uuid           = validated_data['uuid'],
                                        context_name   = validated_data['context_name'],
                                        prev_context   = validated_data['prev_context'],
                                        leaf_node      = validated_data['leaf_node'],
                                        inputs_required = validated_data['inputs_required'],)
       
        return validated_data['uuid']

class TagSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Tag MODEL
    '''
    class Meta:
        model   = Tag
        fields  = "__all__"

class FrequencySerializer(serializers.ModelSerializer):
    '''
    Serializer for the Frequency MODEL
    '''
    context_name = serializers.SerializerMethodField()
    class Meta:
        model   = Frequency
        fields  = ["context_id","frequency","context_name"]
    def get_context_name(self,object):
        context_name = Context.objects.filter(context_name=object.context_id).values('context_name').first()['context_name']
        return context_name

class CompnaySerializer(serializers.ModelSerializer):
    '''
    Serializer for the Company MODEL
    '''
    class Meta:
        model   = Company
        fields  = "__all__"

class RatingSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Rating MODEL
    '''
    class Meta:
        model   = Rating
        fields  = "__all__"

class DocumentSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Document MODEL
    '''
    class Meta:
        model   = Document
        fields  = "__all__"
    def create(self, validated_data):

        document = Document.objects.create(company_id    = validated_data['company_id'],
                                         document      = validated_data['document'],)
        
        return document

class ConversationSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Conversation MODEL
    '''
    class Meta:
        model   = Conversation
        fields  = "__all__"
    

class ListConversationSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Conversation MODEL
    '''
    selected_options = serializers.SerializerMethodField()
    class Meta:
        model   = Conversation
        fields  = ('started_at','session_id','selected_options',)
    def get_selected_options(self,object):
        conv = object.conversation_data
        conv_data=[]
        for j in range(len(conv)):
            if conv[j]['selected'] == None and conv[j]['response']['bot_message']:
                s = str(conv[j]['response']['bot_message'])
                data = re.search('<strong>(.*)</strong>', s)
                # data = s[s.find('<strong>')+len('<strong>'):s.rfind('</strong>')]
                if data: 
                    data= data.group(1)
                    conv_data.append(data)
            else:
                conv_data.append(conv[j]['selected'] )
        return conv_data


class AnswersSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Answers MODEL
    '''
    class Meta:
        model   = Answers
        fields  = "__all__"

class QuestionsSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Answers MODEL
    '''
    class Meta:
        model   = UntaggedQuestions
        fields  = "__all__"


class FeedbackSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Feedback MODEL
    '''
    class Meta:
        model   = Feedback
        fields  = "__all__"


class ISINSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Isin MODEL
    '''
    branch_name = serializers.SerializerMethodField('get_branch_name')
    class Meta:
        model   = Isin
        fields  = ("id", "branch", "client", "isin", "cin_number", "created_at", "branch_name" , "status")
        read_only_fields = ("branch_name","id",  "cin_number")

    def get_branch_name(self, obj):
        return obj.branch.name


class BranchAdressSerializer(serializers.ModelSerializer):
    '''
    Serializer for the BranchAdress Model
    '''
    class Meta:
        model   = BranchAdress
        fields  = "__all__"

    def to_representation(self, instance):
        data = super().to_representation(instance)
        return {k: v for k, v in data.items() if v is not None}
        


