from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group


from admin_panel_app.models import USER_LOGS, TrashedQuestions

UserModel = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    group_name = serializers.CharField(write_only=True)

    class Meta:
        model = UserModel
        fields = ('id', 'first_name', 'last_name', 'email',
                  'password','group_name')
        read_only_fields = ('id',)
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate_email(self, value):
        if UserModel.objects.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists!.")
        return value

    def validate_group_name(self, value):
        group = Group.objects.filter(name=value).first()
        if not group:
            raise serializers.ValidationError("Group not found")
        return group
        

    def create(self, validated_data):

        user = UserModel.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],)

        user.groups.add(validated_data['group_name'])
        return user


class UserUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserModel
        exclude = ('user_permissions',"password" )
        lookup_field = 'email'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ("name",)
class UserSerializerWithToken(serializers.ModelSerializer):

    class Meta:
        model = UserModel

        fields = ['email', 'first_name', 'last_name', "group_name"]
        
    group_name = serializers.SerializerMethodField('get_group_name')

    def get_first_name(self, obj):
        name = obj.first_name
        if len(name) == 0:
            name = obj.email
        return name

    def get_last_name(self, obj):
        name = obj.last_name
        if len(name) == 0:
            name = obj.email
        return name

    def get_group_name(self, obj):
        grp = Group.objects.filter(user = obj)
        grp = [x.name for x in grp]

        return grp


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super(MyTokenObtainPairSerializer, cls).get_token(user)
        token['email'] = user.email
        return token

    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data
        for k, v in serializer.items():
            data[k] = v

        return data



class UserLogsSerializer(serializers.ModelSerializer):
    '''
    Serializer for the ANSWERS MODEL
    '''
    class Meta:
        model   = USER_LOGS
        fields  = "__all__"

class TrashedSerializer(serializers.ModelSerializer):
    '''
    Serializer for the TrashedQuestions MODEL
    '''
    #uuid = serializers.ReadOnlyField()
    class Meta:
        model   = TrashedQuestions
        fields  = "__all__"
    def create(self, validated_data):

        trash = TrashedQuestions.objects.create(question = validated_data['question'],
                                                keywords   = validated_data['keywords'],
                                                frequency  = validated_data['frequency'],
                                                answer     = validated_data['answer'],
                                                user_name  = validated_data['user_name'] )
       
        return trash
