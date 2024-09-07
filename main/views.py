from django.shortcuts import render
from .models import EmailMessage, EmailAccount
from .services import fetch_emails


def email_messages(request):
    # Получаем учетные записи email из базы данных
    email_accounts = EmailAccount.objects.all()

    # Импортируем сообщения для каждой учетной записи
    for account in email_accounts:
        fetch_emails(account)

    messages = EmailMessage.objects.all()
    return render(request, 'main/email_messages.html', {'messages': messages})
