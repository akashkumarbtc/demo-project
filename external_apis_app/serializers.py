from chatbot_app.models import Context
from rest_framework import serializers

class ContextSerializer(serializers.ModelSerializer):
    '''
    Serializer for the Context MODEL
    '''
    #uuid = serializers.ReadOnlyField()
    class Meta:
        model   = Context
        fields  = ('context_name', 'uuid')