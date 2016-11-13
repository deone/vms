from django.template import loader
from django.core.mail import EmailMultiAlternatives
from django.conf import settings

def send_report(context):
    subject_template = 'vouchers/report_subject.txt'
    email_template = 'vouchers/report_email.html'
    subject = loader.render_to_string(subject_template, context)
    subject = ''.join(subject.splitlines())
    body = loader.render_to_string(email_template, context)

    email_message = EmailMultiAlternatives(subject, body, settings.DEFAULT_FROM_EMAIL, settings.VOUCHER_GEN_REPORT_TO)

    email_message.send()