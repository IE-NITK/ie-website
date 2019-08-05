from django.contrib import admin
from accounts.models import Profile, Account, Status, RoundOneSubmission, ActivationRecord


admin.site.register(Profile)
admin.site.register(Account)
admin.site.register(Status)
admin.site.register(RoundOneSubmission)
admin.site.register(ActivationRecord)
