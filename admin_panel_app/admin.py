from django.contrib import admin
from admin_panel_app.models import User,USER_LOGS, TrashedQuestions


admin.site.register(User)
admin.site.register(USER_LOGS)
admin.site.register(TrashedQuestions)