"""
Email backend that uses the Mailersend API.
"""
import logging

from django.conf import settings
from django.core.mail import EmailMessage
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.message import sanitize_address

from mailersend import emails
from requests import RequestException

logger = logging.getLogger(__name__)


class MailersendBackend(BaseEmailBackend):
    def send_message(self, email_message: EmailMessage):
        if not email_message.recipients():
            return False

        encoding = email_message.encoding or settings.DEFAULT_CHARSET

        mailer = emails.NewEmail(settings.MAILERSEND_API_KEY)

        mail_body = {}
        mailer.set_mail_from(
            dict(email=sanitize_address(email_message.from_email, encoding)), mail_body
        )
        mailer.set_mail_to(
            [
                dict(email=sanitize_address(addr, encoding))
                for addr in email_message.to
            ],
            mail_body,
        )
        mailer.set_cc_recipients(
            [
                dict(email=sanitize_address(addr, encoding))
                for addr in email_message.cc
            ],
            mail_body,
        )
        mailer.set_bcc_recipients(
            [
                dict(email=sanitize_address(addr, encoding))
                for addr in email_message.bcc
            ],
            mail_body,
        )
        mailer.set_subject(email_message.subject, mail_body)
        mailer.set_plaintext_content(email_message.body, mail_body)

        try:
            mailer.send(mail_body)
        except RequestException:
            if not self.fail_silently:
                raise
            return False
        return True

    def send_messages(self, email_messages):
        if not email_messages:
            return 0

        num_sent = 0
        for message in email_messages:
            if self.send_message(message):
                num_sent += 1

        return num_sent
