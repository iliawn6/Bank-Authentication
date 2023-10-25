from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from .forms import CreateUserForm, CheckNationalIdForm
from .models import User
from django.core.files.storage import default_storage

import pika, os

def hello(request):
    return HttpResponse("hello world!")


class collectApiView(APIView):

    def get(self, request):
        return Response({"ok": True})
    
    def post(self, request):
        pass


class SubmitInfoView(View):

    def get(self, request):
        return render(request, "create_user.html", {"form": CreateUserForm()})
    
    def post(self, request):
        form = CreateUserForm(request.POST, request.FILES)
        if not form.is_valid():
            return JsonResponse({"error": "bad request"}, status="400")
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        img1_name = form.instance.last_name + str(form.instance.national_id)[0:6] + "_img1.jpg"
        img2_name = form.instance.last_name + str(form.instance.national_id)[0:6] + "_img2.jpg"
        created_username = (form.instance.last_name + str(form.instance.national_id)[0:6])

        new_user = User(email = form.instance.email, last_name = form.instance.last_name, 
                        national_id = hash(form.instance.national_id), ip = ip,
                        image1 = img1_name,
                        image2 = img2_name,
                        username = created_username)
        
        new_user.save()


        url = os.environ.get('CLOUDAMQP_URL', "amqps://eixezsax:59gP2X5yKEVXRB7QlkGE6OE6ixNjPi9B@rat.rmq2.cloudamqp.com/eixezsax")
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)

        # channel = connection.channel() # start a channel
        # channel.queue_declare(queue='hello') # Declare a queue
        # channel.basic_publish(exchange='',
        #                     routing_key='hello',
        #                     body='Hello CloudAMQP!')

        # print(" [x] Sent 'Hello World!'")
        # connection.close()


        
        # connection = pika.BlockingConnection(pika.ConnectionParameters(
        #     host='amqps://eixezsax:59gP2X5yKEVXRB7QlkGE6OE6ixNjPi9B@rat.rmq2.cloudamqp.com/eixezsax/'))
        
        channel = connection.channel()
        channel.queue_declare(queue='users')

        channel.basic_publish(exchange='', routing_key='users', body=created_username)
        print(f"{created_username} has been added to queue!")
        connection.close()

        img1_storage_path = default_storage.save(img1_name, form.instance.image1)
        img2_storage_path = default_storage.save(img2_name, form.instance.image2)

        return HttpResponse("Your authentication request has been registered!!")
    

class ReceiverView(View):
    def get(self, request):
        url = os.environ.get('CLOUDAMQP_URL', "amqps://eixezsax:59gP2X5yKEVXRB7QlkGE6OE6ixNjPi9B@rat.rmq2.cloudamqp.com/eixezsax")
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()

        def callback(ch, method, properties, body):
            print(f" [x] Received {body}")
            
        channel.queue_declare(queue='users')

        channel.basic_consume(queue='users', on_message_callback=callback, auto_ack=True)

        channel.start_consuming()
        channel.close()
        return HttpResponse("done----")
    

class StatusView(View):
    
    def get(self, request):
        return render(request, "user_status.html", {"form": CheckNationalIdForm()})
    
    def post(self, request):
        form = CheckNationalIdForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": "bad request"}, status="400")   
        try:
            user = User.objects.get(national_id = hash(form.instance.national_id))
        except:
            return HttpResponse("User not found", status="404")
        if user.state == "pending":
            return HttpResponse("Pending...")
        elif user.state == "rejected":
            return HttpResponse("Your authentication request has been rejected. Please try again later.")     
        elif user.state == "confirmed":
            return HttpResponse(f"Your authentication was successfull!! Your username is {user.username}.")


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")

