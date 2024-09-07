from django.contrib import admin
from .models import EmailAccount, EmailMessage

@admin.register(EmailAccount)
class EmailAccountAdmin(admin.ModelAdmin):
    list_display = ['email', 'provider']

@admin.register(EmailMessage)
class EmailMessageAdmin(admin.ModelAdmin):
    list_display = ['subject', 'email_account', 'send_date', 'received_date']
    list_filter = ['email_account', 'send_date']
    search_fields = ['subject', 'body']