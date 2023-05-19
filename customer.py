import json
import pika
import smtplib
from models import Contact

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue='email_queue')
channel.queue_declare(queue='sms_queue')

def send_email(contact):
    print(f"Sending email to {contact.email}")
    print("Email sent successfully")
    contact.is_sent = True
    contact.save()

def send_sms(contact):
    print(f"Sending SMS to {contact.phone_number}")
    print("SMS sent successfully")
    
    contact.is_sent = True
    contact.save()
    
def callback(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects.get(id=contact_id)
    send_email(contact)
    ch.basic_ack(delivery_tag=method.delivery_tag)

def callback_sms(ch, method, properties, body):
    message = json.loads(body)
    contact_id = message['contact_id']
    contact = Contact.objects.get(id=contact_id)
    send_sms(contact)
    ch.basic_ack(delivery_tag=method.delivery_tag)

channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='email_queue', on_message_callback=callback)
channel.basic_consume(queue='sms_queue', on_message_callback=callback_sms)

print('Waiting for messages. To exit, press CTRL+C')
channel.start_consuming()
