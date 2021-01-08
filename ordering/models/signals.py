from django.db.models.signals import pre_save
from django.dispatch import receiver

from ordering.models.orders import Order
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


@receiver(pre_save, sender=Order)
def send_email_after_status_change(sender, instance, **kwargs):
    # this is a pre_save signal which send an email after status change
    old_instance = Order.objects.get(pk=instance.pk)
    if old_instance.status != instance.status:
        try:
            subject = 'Order status changed'
            mail_content = 'Dear Customer,\nYour Order\'s Status Has Changed to {}'.format(instance.status)
            send_email(subject, mail_content)
        except:
            print('Could Not Send Mail')


async def send_email(subject, mail_content):
    mail_content = mail_content

    # For testing this part you have to Turn on "Less secure app access" in your Gmail account
    # We should set customer\'s Email instead of receiver_address
    # The mail addresses and password
    sender_address = 'fahimehfathian@gmail.com'
    sender_pass = '********'
    receiver_address = 'fahimen2000@gmail.com'

    # Setup the MIME
    message = MIMEMultipart()
    message['From'] = sender_address
    message['To'] = receiver_address
    message['Subject'] = 'A test mail sent by Python. It has an attachment.'   # The subject line

    # The body and the attachments for the mail
    message.attach(MIMEText(mail_content, 'plain'))
    # Create SMTP session for sending the mail
    session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
    session.starttls()  # enable security
    session.login(sender_address, sender_pass)  # login with mail_id and password
    text = message.as_string()
    session.sendmail(sender_address, receiver_address, text)
    session.quit()
    print('Mail Sent')
