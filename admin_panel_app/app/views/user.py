from rest_framework.generics import  ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import uuid
import base64

from link_chatbot.settings.base import *


from admin_panel_app.app.permissions import HasGroupPermission
from admin_panel_app.models import USER_LOGS
from admin_panel_app.app.helper import send_forgot_password_email
from admin_panel_app.app.serializers import (
                                        UserSerializer,GroupSerializer,
                                        UserUpdateSerializer,
                                        MyTokenObtainPairSerializer,
                                        )


UserModel = get_user_model()

class AdminPannelUserDeactivateView(APIView):
    '''
    provides the admin user to decativate any user account.
    '''
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins"]

    def get(self, request, format=None ):
        return Response({'user_email':""},status=200)
    
    def post(self, request,format=None):
        user_email = request.data['user_email']

        user_account = UserModel.objects.filter(email=user_email).values_list('email','is_active').first()
        if len(user_account)==0 or user_account[1]==False:
            return Response({"No active account found with the given email!"},status=status.HTTP_400_BAD_REQUEST)
        user_account_instace = UserModel.objects.get(email=user_email)
        user_account_instace.is_active =False
        user_account_instace.save()

        user_type=Group.objects.get(user = request.user.id)
        USER_LOGS.objects.create_user_logs(request.user,str(user_type),"Deactivated "+user_email+" account",{"previous_data":[{"Account":"Active"}],"current_data":[{"Account":"Deactivated"}]},True)
        

        
        return Response({f"{user_email} account has been deactivated successfully!"},status=200)



class CreateUserView(ListCreateAPIView):
    """
    Create a new user.
    Only users in the Admins group can create new users
    """
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins"]
    

    queryset           = UserModel.objects.all()
    
    def post(self, request, *args, **kwargs):
        
        
        serializer =UserSerializer(data =request.data)

        first_name = request.data['first_name']
        last_name = request.data['last_name']
    
        if serializer.is_valid():
            
            serializer.save()
    
            me = env('EMAIL_USER')
            me_pass = env('EMAIL_PASS') #sender mail Id password
            print(me)
            to = str(request.data['email'])
            cc = str(request.user)

            mail_content = f'''
Hello {first_name} {last_name},

This is to inform you that your Link Intime chatbot Admin Panel account has been sucessfully created.

Here are the login credentials,
e-mail: {to}
password:{request.data['password']}

Regards,
I-Dia. 


Please do not reply directly to this autogenerated email. If you have any questions or concerns, please contact Link Intime.
            '''
            msg = MIMEMultipart('alternative')
            msg['From'] = me
            msg['To'] = to
            msg['Cc'] =cc
            msg['Subject'] ="Account creation successful!" 
            msg.attach(MIMEText(mail_content, 'plain'))

            #Create SMTP session for sending the mail
            session = smtplib.SMTP('smtp.gmail.com', 587) #use gmail with port
            session.starttls() #enable security
            session.login(me, me_pass) #login with mail_id and password
            text = msg.as_string()
            session.sendmail(me, to, text)
            session.quit()
            print('Mail Sent')
            
            return Response({"account creation successful!"},status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors)
            
    def put(self,request):
        User = UserModel.objects.filter(email=request.data['email'])
        serializer = UserSerializer(User,data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        User = UserModel.objects.get(email=request.data['email'])
        
        User.delete()

        
        return Response({"account deleted successfully"})

class UserDetailView(RetrieveUpdateDestroyAPIView ):
    """
    fetch or update or delete an existing  user.
    """
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins"]
    model              = UserModel
    serializer_class   = UserUpdateSerializer
    queryset           = UserModel.objects.all()
    lookup_field       = "email"

    def get_object(self):
        try:
            pk = self.kwargs.get('pk')
            return UserModel.objects.get(email=pk)
        except UserModel.DoesNotExist:
            return Response({'detail': "User not found"}, status=status.HTTP_404_NOT_FOUND)


class AddUserGroupView(ListCreateAPIView):
    """
    Assign a user to a specific group.
    Only users in the Admins group can assign users to groups
    """
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins"]
    model              = Group
    serializer_class   = GroupSerializer
    queryset           = Group.objects.all()


class ListGroupUserView(ListAPIView):
    """
    List all the users under a specific group
    """
    permission_classes = [HasGroupPermission]
    required_groups    = ["Admins","Maintenance"]
    model              = UserModel
    serializer_class   = UserSerializer

    def get_queryset(self):
        return UserModel.objects.filter(groups__name=self.kwargs['pk'])

class MyObtainTokenPairView(TokenObtainPairView):
    """
    Generate token for logged in user
    """
    permission_classes = [AllowAny]
    serializer_class   = MyTokenObtainPairSerializer

class ForgotPasswordView(APIView):
    '''
    Provides the user reset password link to mail id via email.
    '''
    def get(self, request, *args, **kwargs):
        return Response({"email":None},status=200)
    
    def post(self, request, *args, **kwargs):
        # global token,encoded_email

        email         = request.data['email']
        encoded_email = base64.b64encode(email.encode('utf-8'))
        
        host          = request.get_host()
        if UserModel.objects.filter(email = email).exists():
            user_obj = UserModel.objects.get(email=email)
            
            token   = str(uuid.uuid4())
   
            send_forgot_password_email(user_obj,token,host,encoded_email)
            return Response("A password reset link has been sent to your mail.",status=200)
        else:
            return Response("No user found with given mail id.",status=status.HTTP_400_BAD_REQUEST)

class RestPasswordView(APIView):
    '''
    Provides user to reset the password of their account.
    '''

    def post(self, request, *args, **kwargs):
        t, encoded_email = self.kwargs['pk'].split(',')
        encoded_email = encoded_email[1:]
        
        # global token
        
        # if  str(encoded_email)==self.kwargs['pk'].split(',')[1]:

        password = request.data['password']
        confirm_password = request.data['confirm_password']

        if password == confirm_password:

            email = base64.b64decode(encoded_email).decode("utf-8")
            user = UserModel.objects.get(email = email)
            user.set_password(password)
            user.save()
            # token =None
            return Response("Password hase beeen successfully changed!")

        return Response("Page Not Found",status=status.HTTP_404_NOT_FOUND)
