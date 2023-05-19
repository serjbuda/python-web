import json
import pika
from faker import Faker
from models import Contact

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='sms_queue')
channel.queue_declare(queue='email_queue')

fake = Faker()

for _ in range(10):
    fullname = fake.name()
    email = fake.email()
    phone_number = fake.phone_number()
    delivery_method = fake.random_element(elements=["SMS", "Email"])
    
    contact = Contact(fullname=fullname, email=email, phone_number=phone_number, delivery_method=delivery_method)
    contact.save()
    
    message = {'contact_id': str(contact.id)}
    queue_name = 'sms_queue' if contact.delivery_method == 'SMS' else 'email_queue'
    channel.basic_publish(exchange='', routing_key=queue_name, body=json.dumps(message))

connection.close()
