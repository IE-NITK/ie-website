from django.contrib import admin
from accounts.models import Profile, Account, Status, RoundOneSubmission, ActivationRecord


admin.site.register(Profile)
@admin.register(Account)
class itemAdmin(admin.ModelAdmin):
    list_display = ('role', 'profile', 'user', 'is_active', 'archive', 'SIG', 'roll_no')
admin.site.register(Status)
admin.site.register(RoundOneSubmission)
admin.site.register(ActivationRecord)
