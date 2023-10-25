from celery import Celery, shared_task
import pika, os
from Authorization.celery import app
from .models import Test

#app = Celery()
  
@app.task
def consume(): 

    # url = os.environ.get('CLOUDAMQP_URL', "amqps://eixezsax:59gP2X5yKEVXRB7QlkGE6OE6ixNjPi9B@rat.rmq2.cloudamqp.com/eixezsax")
    # params = pika.URLParameters(url)
    # connection = pika.BlockingConnection(params)
    # channel = connection.channel()

    # def callback(ch, method, properties, body):
    #     #print(f" [x] Received {body}")
    #     test = Test(username = body)
    #     test.save()
        
    # channel.queue_declare(queue='users')

    # channel.basic_consume(queue='users', on_message_callback=callback, auto_ack=True)

    # channel.start_consuming()
    # channel.close()
    #print("hey")
    test = Test(username = "done")
    test.save()
    
    
# from celery import Celery
# from celery.schedules import crontab

# app = Celery()

# @app.on_after_configure.connect
# def setup_periodic_tasks(sender, **kwargs):
#     # Calls test('hello') every 10 seconds.
#     sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

#     # Calls test('hello') every 30 seconds.
#     # It uses the same signature of previous task, an explicit name is
#     # defined to avoid this task replacing the previous one defined.
#     sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

#     # Calls test('world') every 30 seconds
#     sender.add_periodic_task(30.0, test.s('world'), expires=10)

#     # Executes every Monday morning at 7:30 a.m.
#     sender.add_periodic_task(
#         crontab(hour=7, minute=30, day_of_week=1),
#         test.s('Happy Mondays!'),
#     )

# @app.task
# def test(arg):
#     print(arg)

# @app.task
# def myadd(x, y):
#     z = x + y
#     print(z)