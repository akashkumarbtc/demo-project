from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView


from admin_panel_app.app.views.dashboard import (AdminPanelDashboardRatingView,DashboardCustomerRatingGraph,
                                                FrequentlyAskedQuestionsView,DashboardListUntaggedQuestions,)
                                            
from admin_panel_app.app.views.trash import AdminPanelTrashWithKeyword,AdminPanelTrash

from admin_panel_app.app.views.home import AdminPanelAnalytics,UserLogsView,AdminPanelUserloagsView

from admin_panel_app.app.views.user import(AdminPannelUserDeactivateView,CreateUserView,UserDetailView,
                                            AddUserGroupView,ListGroupUserView,MyObtainTokenPairView,
                                            ForgotPasswordView,RestPasswordView,)

from admin_panel_app.app.views.workflow import AdminPanelContextView,AdminPanelContextDetailView,AdminPanelContextCreation,ConextDuplicationView

from admin_panel_app.app.views.file_upload import IsinLoadData,IsinDataTemplate, ExportFAQ, ExportUntaggedQuestions, ExportUserLogs, ExportUserFeedback, ExportAllQuestions

from admin_panel_app.app.views.conversation import ConversationView, CountOfEmptyConversations


router = DefaultRouter()
router.register("userlogs",UserLogsView,basename='user_logs')

urlpatterns = [
    # User urls 
    path('create-user/', CreateUserView.as_view(), name='create_user'),
    path('user/<str:pk>/', UserDetailView.as_view(), name='user_detail'),

    # Import and Export Data
    path('data-load/',IsinLoadData.as_view(), name='data_load'),
    path('data-export/',IsinDataTemplate.as_view(), name='data_export'),
    path('export-faq/',ExportFAQ.as_view(), name='faq_export'),
    path('export-untagged-questions/',ExportUntaggedQuestions.as_view(), name='untagged_export'),
    path('export-user-logs/',ExportUserLogs.as_view(), name='user_logs_export'),
    path('export-user-feedback/',ExportUserFeedback.as_view(), name='user_feedback_export'),
    path('export-all-questions/',ExportAllQuestions.as_view(), name='all_questions_export'),


    # Group urls 
    path('list-group/', AddUserGroupView.as_view(), name='add_user_to_group'),
    path('list-group-users/<str:pk>/', ListGroupUserView.as_view(), name='list_group_users'),


    # login and logout 
    path('login/', MyObtainTokenPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    #forgot Password
    path('forgot-password/', ForgotPasswordView.as_view(),name='forgot_password'),
    path('reset-password/<str:pk>/', RestPasswordView.as_view(), name='reset_password'),


    # user deactivate
    path('deactivate/',AdminPannelUserDeactivateView.as_view(), name='user_deactiavate'),


    # add default router urls
    path('', include('rest_framework.urls', namespace='rest_framkework')),

    path('admin-context/', AdminPanelContextView.as_view(), name='admin_context'),
    path('admin-context-delete/<str:pk>/', AdminPanelContextView.as_view(), name='admin_context_delete'),
    path('admin-context-detail/<str:pk>/', AdminPanelContextDetailView.as_view(), name='admin_context_detail'),
    path('admin-context-creation/',AdminPanelContextCreation.as_view(), name='admin_context_creation'),
    path('context-duplication/',ConextDuplicationView.as_view(), name='context_duplication'),

    path('admin-trash/',AdminPanelTrash.as_view(), name='admin_tarsh'),
    path('admin-trash-keyword/',AdminPanelTrashWithKeyword.as_view(), name='admin_trash_keyword'),

    #user search based logs 
    path('search-userlogs/',AdminPanelUserloagsView.as_view(), name='search_user_logs'),
 
    
    #Analytics urls
    path('analytics/',AdminPanelAnalytics.as_view(), name='admin_analytics'),

    # Admin Panel Dashboard urls
    path('dashboard-ratings/',AdminPanelDashboardRatingView.as_view(), name='admin_dashboard_rating'),
    path('dashboard-frequent-questions/',FrequentlyAskedQuestionsView.as_view(), name='dashboard_frequent_questions'),
    path('dashboard-customer-satisfaction-graph/',DashboardCustomerRatingGraph.as_view(), name='dashboard_customer_satisfaction_graph'),
    path('dashboard-untagged-questions/',DashboardListUntaggedQuestions.as_view(), name='dashboard_untagged_question'),
    # path('dashboard-untagged-questions/<str:pk>/',DashboardListUntaggedQuestions.as_view(), name='dashboard_untagged_question'),
    
    # Conversations View Url
    path('conversations/', ConversationView.as_view(), name='conversations'),
    path('empytconv/', CountOfEmptyConversations.as_view(), name='emptyconv'),
    path('', include(router.urls))
]