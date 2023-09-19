
from django.urls import path, include
from external_apis_app.views import QuestionListView, ContextDetailView, FocusAddressView

urlpatterns = [

    path('question-list/',QuestionListView.as_view(),name = 'question-list'),
    path('context-list/',ContextDetailView.as_view(), name ='context-list'),
    path('focus-address-list/',FocusAddressView.as_view(), name ='focus-address-list'),
    
]