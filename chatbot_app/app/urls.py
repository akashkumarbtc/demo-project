from django.urls import path, include
from rest_framework.routers import DefaultRouter


from chatbot_app.app.views import (TagView,
                                   FrequencyView,
                                   CompanyView,
                                   DocumentView,
                                   ConversationView,
                                   AnswersView,
                                   ContextView,
                                   WorkFlowView,
                                   RatingView,
                                   MainMenuView,
                                   BannerView,
                                   UntaggedQuestionsMailClick,
                                   FeedbackView,
                                   IsinView,
                                   BranchAddressView,
                                   CreateToken
                                   )

router = DefaultRouter()
router.register('context',         ContextView,           basename='Context')
router.register('tags',            TagView,               basename='TagS')
router.register('frequency',       FrequencyView,         basename='Frequency')
router.register('company',         CompanyView,           basename='Company')
router.register('document',        DocumentView,          basename='Document')
router.register('conversation',    ConversationView,      basename='Conversation')
router.register('answers',         AnswersView,           basename='Answers')
router.register('feedback',        FeedbackView,          basename='Feedback')
router.register('isin',            IsinView,              basename='Isin')
router.register('branch-address',  BranchAddressView,     basename='branch_address')

urlpatterns = [
    path('', include(router.urls)),
    path('chatbot-view/',WorkFlowView.as_view(),name = 'chatbot_view'),
    path('rating/',RatingView.as_view(), name ='Rating'),
    path('main-menu-options/',MainMenuView.as_view(),name = 'mainmenu_view'),
    path('banner-options/',BannerView.as_view(),name = 'banner_view'),
    path('mail-selected/',UntaggedQuestionsMailClick.as_view(),name = 'mail_selected'),
    path('create-token/',CreateToken.as_view(),name = 'create_token'),
    
]