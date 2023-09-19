from django.contrib import admin
from chatbot_app.models import (Context,
                                Tag,
                                Frequency,
                                Company,
                                Document,
                                Conversation,
                                Answers,
                                Rating,UntaggedQuestions,
                                FocusAddress, Feedback, Isin,
                                BranchAdress,)


admin.site.register(Context)
admin.site.register(Tag)
admin.site.register(Frequency)
admin.site.register(Company)
admin.site.register(Document)
admin.site.register(Conversation)
admin.site.register(Answers)
admin.site.register(Rating)
admin.site.register(UntaggedQuestions)
admin.site.register(FocusAddress)
admin.site.register(Feedback)
admin.site.register(Isin)
admin.site.register(BranchAdress)
