from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import PermissionsMixin
from django.utils.translation import gettext_lazy as _

from admin_panel_app.managers import UserManager


class User(AbstractUser):

    first_name       = models.CharField(max_length=100)
    last_name        = models.CharField(max_length=100)
    email            = models.EmailField(max_length=100, unique=True)
    password         = models.CharField(max_length=100)
   
    # values to satisfy djangos User model constraints
    
    USERNAME_FIELD   = 'email'
    username         = models.CharField(max_length=40, unique=False, default='', null=True)

    REQUIRED_FIELDS  = []

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    objects          = UserManager()

    def __str__(self):
        return self.email


class UserLogsManager(models.Manager):
    def create_user_logs(self, user_name,user_type,actions,history,display_button):

        log = self.create(user_name  = user_name,
                         user_type   = user_type,
                         actions     = actions,
                         history = history,
                         display_button = display_button)
        
        return log

class USER_LOGS(models.Model):
    '''
    user_logs povides user activity details.
    '''
    user_name   = models.CharField(max_length=200, null=True, blank=True)
    user_type   = models.CharField(max_length=50, null=True, blank=True)
    date        = models.DateField(auto_now_add=True)
    time        = models.TimeField(auto_now=True)
    actions     = models.CharField(max_length=500, null=True, blank=True)
    history     = models.JSONField(default=dict, null=True, blank=True)

    display_button = models.BooleanField(default=True,null=True, blank=True)
    
    created_at  = models.DateTimeField(auto_now=True) 

    objects = UserLogsManager()

    def _str_(self):
        return self.user_name + '||' + self.actions



class TrashedQuestions(models.Model):
    '''
    Trashed Question model is used to store
    deleted questions from context table.
    '''

    question        = models.JSONField(default=dict, null=True, blank=True)
    keywords        = models.JSONField(default=dict, null=True, blank=True)
    frequency       = models.JSONField(default=dict, null=True, blank=True)
    answer          = models.JSONField(default=dict, null=True, blank=True)
    user_name       = models.CharField(max_length=255,null=True, blank=True)
    

    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.question["context_name"]

