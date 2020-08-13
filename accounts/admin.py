from django.contrib import admin
from accounts.models import Profile, Account, Status, RoundOneSubmission, ActivationRecord, BasicResponses


admin.site.register(Profile)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('role', 'profile', 'user', 'is_active',
                    'archive', 'SIG', 'roll_no')


@admin.register(BasicResponses)
class ResponsesAdmin(admin.ModelAdmin):
    list_display = ('user', 'ans1', 'ans2', 'ans3', 'created_at')


admin.site.register(Status)
admin.site.register(RoundOneSubmission)
admin.site.register(ActivationRecord)
