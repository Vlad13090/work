import imaplib
import email
from email.header import decode_header
from django.utils import timezone
from .models import EmailMessage


def fetch_emails(email_account):
    mail = imaplib.IMAP4_SSL('imap.' + email_account.provider + '.com')
    mail.login(email_account.email, email_account.password)
    mail.select("inbox")

    # Поиск всех сообщений в почтовом ящике
    status, messages = mail.search(None, 'ALL')

    for num in messages[0].split():
        status, data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(data[0][1])

        subject, encoding = decode_header(msg["Subject"])[0]
        if isinstance(subject, bytes):
            subject = subject.decode(encoding or 'utf-8')

        from_email = msg.get("From")
        date = msg.get("Date")

        # Обработка тела письма
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" in content_disposition:
                    # Обработка вложений
                    pass
                elif content_type == "text/plain":
                    body = part.get_payload(decode=True).decode()
        else:
            body = msg.get_payload(decode=True).decode()

        # Сохранение сообщения в базу данных
        EmailMessage.objects.create(
            email_account=email_account,
            subject=subject,
            send_date=timezone.now(),  # корректно конвертировать date в datetime
            received_date=timezone.now(),
            body=body,
            attachments=[]
        )

    mail.logout()
