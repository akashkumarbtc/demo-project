from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from chatbot_app.app.views import TestView

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('chatbot/',    include('chatbot_app.app.urls')),
    path('account/',    include('admin_panel_app.app.urls')),
    path('external-api/',    include('external_apis_app.urls')),
    path('',  TestView.as_view(),name=''),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += path('__debug__/',include(debug_toolbar.urls)),
