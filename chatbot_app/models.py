from django.db import models
from uuid import uuid4
from django.contrib.auth.models import User
from django.db.models import F

class ContextManager(models.Manager):
    def create_context(self, context_name,uuid,prev_context,leaf_node,inputs_required):
        if self.filter(uuid    =uuid).exists():
            return
        context = self.create(context_name    =context_name,
                              uuid            =uuid,
                              prev_context    =prev_context,
                              leaf_node       =leaf_node,
                              inputs_required = inputs_required)
        
        return context

class Context(models.Model):
    '''
    Context model is used to define
    parent child relation between all the nodes.
    '''

    context_name    = models.CharField(max_length=500, null=True, blank=True)
    uuid            = models.UUIDField(primary_key=True, default=uuid4)
    prev_context    = models.UUIDField(default=None, null=True, blank=True)
    leaf_node       = models.BooleanField(default=True)
    inputs_required = models.BooleanField(default=False)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects         = ContextManager()


    def __str__(self):
        return self.context_name
    
    # @property
    # def sub_question(self):
    #     questions = self.objects.filter(prev_context=self.uuid)
    #     return questions



class TagManager(models.Manager):
    def create_tags(self, context_id,tags):

        if self.filter(context_id  =context_id).exists():
            return

        tag = self.create(context_id  =context_id,
                              tags    =tags)
        
        return tag


class Tag(models.Model):
    '''
    Tag model is used to define
    relations between the tags and the context model
    '''

    context_id      = models.OneToOneField(Context, on_delete=models.CASCADE)
    tags            = models.JSONField(default=list, null=True, blank=True)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects = TagManager()

    def __str__(self):
        return str(self.tags)

class FrequencyManager(models.Manager):
    def create_frequency(self, context_id,frequency):

        if self.filter(context_id =context_id).exists():
            return

        freq = self.create(context_id  =context_id,
                           frequency   =frequency)
        
        return freq


class Frequency(models.Model):
    '''
    Frequency model is used to represent
    frequency of each options used. 
    '''
    context_id      = models.OneToOneField(Context, on_delete=models.CASCADE)
    frequency       = models.PositiveIntegerField(default=0)
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects = FrequencyManager()

    def __str__(self):
        return str(self.context_id)+'||'+str(self.frequency)


class CompanyManager(models.Manager):
    def create_company(self, name,url):

        if self.filter(name =name).exists():
            return

        comp = self.create(name    =name,
                           url     =url)
        
        return comp


class  Company(models.Model):
    '''
    Company model is used to 
    determine the company name and url link.
    '''
    name            = models.CharField(max_length=500, null=True, blank=True)
    url             = models.URLField(max_length=1000, null=True, blank=True)

    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects         = CompanyManager()

    def __str__(self):
        return self.name

class DocumentManager(models.Manager):
    def create_document(self, company_id,document):

        doc = self.create(company_id   =company_id,
                           document    =document)
        
        return doc


class Document(models.Model):
    '''
    Document model is used to
    store company ralated document.
    '''
    company_id      = models.ForeignKey(Company, on_delete=models.CASCADE)
    document        = models.FileField(max_length=500, null=True, blank=True)
    
    created_at      = models.DateTimeField(auto_now_add=True)
    updated_at      = models.DateTimeField(auto_now=True)

    objects         = DocumentManager()

    def __str__(self):
        return str(self.document.name)


def json_conversation_inputs_value():
    inputs = [{"name":"pan","type":"varchar","max_char":"10","value":""},

              {"name":"OTP","type":"numeric","max_char":"x","value":""},

              {"name":"DPID","type":"varchar","max_char":"16","value":""}
              ]
    return inputs


class ConversationManager(models.Manager):
    def create_Conversation(self, session_id,inputs,output,conversation_data):

        Conversation = self.create(session_id   =session_id,
                                    inputs      =inputs,
                                    output      =output,
                           conversation_data    =conversation_data)
        
        return Conversation

class Conversation(models.Model):
    '''
    Conversation model is used to record all the user actions
    '''

    uuid                = models.UUIDField(primary_key=True, default=uuid4)
    started_at          = models.DateTimeField(auto_now_add=True)
    session_id          = models.CharField(max_length=150,unique=True,null=True,blank=True)
    #user_id             = models.ForeignKey(User, on_delete=models.CASCADE)
    inputs              = models.JSONField(default=None, null=True, blank=True)
    output              = models.JSONField(default=None, null=True, blank=True)
    conversation_data   = models.JSONField(default=list, null=True, blank=True)

    objects         = ConversationManager()

    
    def __str__(self):
        return str(self.session_id)

    
class AnswersManager(models.Manager):
    def create_answers(self, context_id,answer,document,url=None):

        if self.filter(context_id =context_id).exists():
            return

        ans = self.create(context_id    =context_id,
                          answer        =answer,
                          document      =document if document and "None" not in document else None,
                          url           =url)
        
        return ans



class Answers(models.Model):
    '''
    Answers model used to define
    the relation between query and solution provided.
    '''
    context_id          = models.OneToOneField(Context,on_delete=models.CASCADE)
    answer              = models.TextField(blank=True,null=True,default=None)
    document            = models.ForeignKey(Document, on_delete=models.CASCADE,null=True, blank=True,default=None)
    url                 = models.URLField(blank=True,null=True,default=None)

    created_at          = models.DateTimeField(auto_now_add=True)
    updated_at          = models.DateTimeField(auto_now=True)

    objects             = AnswersManager()

    def __str__(self):
        return str(self.context_id)

class RatingsManager(models.Manager):
    def create_rating(self, rating_5,rating_4,rating_3,rating_2,rating_1):

        if len(self.filter()) >1:
            return

        rating = self.create(rating_5    =rating_5,
                            rating_4     =rating_4,
                            rating_3     =rating_3,
                            rating_2     =rating_2,
                            rating_1     =rating_1)
        return rating

class Rating(models.Model):
    '''
    Rating model is used to store
    the rating given by user.
    '''

    rating_5        = models.PositiveIntegerField(default=0)
    rating_4        = models.PositiveIntegerField(default=0)
    rating_3        = models.PositiveIntegerField(default=0)
    rating_2        = models.PositiveIntegerField(default=0)
    rating_1        = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    objects = RatingsManager()

    

    def __str__(self):
        return "5 star="+str(self.rating_5)+'||4 star='+str(self.rating_4)+'||3 star='+str(self.rating_3)+'||2 star='+str(self.rating_2)+'||1 star='+str(self.rating_1)

class UntaggedQuestionsManager(models.Manager):
    def create_untagged_questions(self, un_taged_question,frequency):
        if self.filter(un_taged_question =un_taged_question).exists():
            self.filter(un_taged_question = un_taged_question).update(frequency=F('frequency') + 1)
            return

        untaged_question = self.create(un_taged_question   =un_taged_question)
        
        return untaged_question


class UntaggedQuestions(models.Model):
    '''
    Questions model is used to store
    the un taged questions provided by
    the user.
    '''


    un_taged_question = models.CharField(max_length=300,null=True, blank=True,default=None)
    frequency         = models.PositiveIntegerField(null=True, blank=True, default=1)
    is_resolved       = models.BooleanField(null=True, blank=True, default=None)
    mail_click        = models.BooleanField(null=True, blank=True, default=None)

    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    objects           = UntaggedQuestionsManager()

    def _str_(self):
        return self.un_taged_question


class FocusAddress(models.Model):
    '''
    Focus Address model used to define
    address, contact info and address of each company
    '''
    focus_answer      = models.TextField(blank=True,null=True,default=None)
    company_id        = models.ForeignKey(Company, on_delete=models.CASCADE)
    contact_info      = models.TextField(blank=True,null=True,default=None)
    topic             = models.CharField(max_length=300,null=True, blank=True,default=None)

    created_at        = models.DateTimeField(auto_now_add=True)
    updated_at        = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.company_id) + " | " + str(self.topic)


class Feedback(models.Model):
    '''
    Feedback is used to collect user feedback
    '''
    reason           = models.CharField(max_length=300,blank=True,null=True,default=None)
    description      = models.TextField(blank=True,null=True,default=None)
    is_resolved      = models.BooleanField(null=True, blank=True, default=None)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

class IsinManager(models.Manager):
    def create_isin(self, branch,branch_code,branch_name,isin,client,client_id,cin_number,Vertical,flag):

        if branch == 'SKDC': branch = Company.objects.get(name='skdc-consultants')
        elif branch == 'LIIPL': branch = Company.objects.get(name='linkintime')
        elif branch == 'TCPL': branch = Company.objects.get(name='tcplindia')
        elif branch == 'UCS': branch = Company.objects.get(name='unisec')
        ISIN =""
        if self.filter(cin_number =cin_number.strip()).exists():
            ISIN = Isin.objects.filter(cin_number=cin_number).update(branch = branch,
                            branch_code   = branch_code,
                            branch_name = branch_name,
                            isin        = isin,
                            client_id   = client_id,
                            cin_number  = cin_number,
                            Vertical    = Vertical,
                            flag    = flag)

        else: 
            ISIN = self.create(branch       =branch,
                            branch_code   = branch_code,
                            branch_name = branch_name,
                            client      = client,
                            isin        = isin,
                            client_id   = client_id,
                            cin_number  = cin_number,
                            Vertical=Vertical,
                            flag =flag)
        return ISIN


class Isin(models.Model):
    '''Isin is used provide the isin details.'''
    branch      = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True,default=None)
    client      = models.CharField(max_length=500, null=True, blank=True,default=None)
    isin        = models.CharField(max_length=200, null=True, blank=True,default=None)
    branch_code = models.CharField(max_length=50, null=True, blank=True,default=None)
    branch_name = models.CharField(max_length=50, null=True, blank=True,default=None)
    client_id   = models.CharField(max_length=100,null=True, blank=True,default=None)
    cin_number  = models.CharField(max_length=150, null=True, blank=True,default=None)
    status      = models.CharField(max_length=200, null=True, blank=True,default="Active")
    Vertical    = models.CharField(max_length=100, null=True, blank=True, default=None)
    flag        = models.CharField(max_length=50, null=True, blank=True,default=None)
    
    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    objects          = IsinManager()


    def __str__(self):
        return str(self.branch) + " | " + str(self.client)

class BranchAdressManager(models.Manager):
    def create_BranchAdress(self, company,branch_name,branch_id,branch_address,phone_number,email_address,total_address):

        if self.filter(branch_id =branch_id).exists():
            return
        
        if company == 'skdc-consultants': company = Company.objects.get(name='skdc-consultants')
        elif company == 'linkintime': company = Company.objects.get(name='linkintime')
        elif company == 'tcplindia': company = Company.objects.get(name='tcplindia')
        elif company == 'unisec': company = Company.objects.get(name='unisec')

        branchadress = self.create(company          = company,
                                    branch_name     = branch_name,
                                    branch_id       = branch_id,
                                    branch_address  = branch_address,
                                    phone_number    = phone_number,
                                    email_address   = email_address,
                                    total_address   = total_address)
        return branchadress



class BranchAdress(models.Model):
    '''BranchAdress has all the adresses of companies.'''

    company         = models.ForeignKey(Company, on_delete=models.CASCADE, blank=True, default=None,null=True)
    branch_name     = models.CharField(max_length=100, null=True, blank=True, default=None)
    branch_id       = models.CharField(max_length=25, null=True, blank=True,default=None)
    branch_address  = models.TextField(null=True, blank=True,default=None)
    phone_number    = models.CharField(max_length=50, null=True, blank=True,default=None)
    email_address   = models.CharField(max_length=50, null=True, blank=True,default=None)
    total_address   = models.TextField(blank=True,null=True,default=None)
    g_maps_link     = models.CharField(max_length=500, null=True, blank=True, default=None)
    g_maps_iframe   =  models.TextField(null=True, blank=True, default=None)

    created_at       = models.DateTimeField(auto_now_add=True)
    updated_at       = models.DateTimeField(auto_now=True)

    objects          = BranchAdressManager()


    def __str__(self):
        return str(self.company) + " | " + str(self.branch_name)
