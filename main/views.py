from django.shortcuts import render
from .models import EmailMessage, EmailAccount
from .services import fetch_emails


def email_messages(request):
    email_accounts = EmailAccount.objects.all()

    for account in email_accounts:
        fetch_emails(account)

    messages = EmailMessage.objects.all()
    return render(request, 'main/email_messages.html', {'messages': messages})
