from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from .forms import CreateUserForm, CheckNationalIdForm
from .models import User
from django.core.files.storage import default_storage

import pika, os
import requests
import time

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

        def callback(ch, method, properties, body):
            print(f" [x] Received {body}")

            def dbChanges(check_bool, username):
                user = User.objects.get(username = username)
                email = user.email
                state = ""
                if check_bool == True:
                    user.state = "confirmed."
                    state = "confirmed."
                    user.save()
                else:
                    user.state = "rejected."
                    state = "confirmed"
                    user.save()
                print("State successfully changed")
                response = requests.post(
                        "https://api.mailgun.net/v3/sandbox48978a765fbd4c369c0513220ca1273d.mailgun.org/messages",
                        auth=("api", "42818c350b22a4e25a0ee16768ebaa6c-324e0bb2-71e16711"),
                        data={"from": "Cloud Computing <mailgun@sandbox48978a765fbd4c369c0513220ca1273d.mailgun.org>",
                            "to": [email],
                            "subject": "Bank Authentication Result",
                            "text": f"Your authentications request has been {state}"})

                print(response.json())


            api_key = 'acc_e68549d6c13fa79'
            api_secret = '6c88ec182a38feee0ba4ede9ebf672ad'
            image_path1 = str(body)[2:-1] + "_img1.jpg"
            image_path2 = str(body)[2:-1] + "_img2.jpg"
            username = str(body)[2:-1]

            response1_bool = False
            response2_bool = False
            
            try:
                response = requests.post(
                    'https://api.imagga.com/v2/faces/detections?return_face_id=1',
                    auth=(api_key, api_secret),
                    files={'image': default_storage.open(image_path1).read()})
                face_id_1 = response.json()["result"]["faces"][0]["face_id"]
                response1_bool = True
                print(face_id_1)
            except:
                print("Wrong image1(it's not face image)!!")

            try:
                response = requests.post(
                    'https://api.imagga.com/v2/faces/detections?return_face_id=1',
                    auth=(api_key, api_secret),
                    files={'image': default_storage.open(image_path2).read()})
                face_id_2 = response.json()["result"]["faces"][0]["face_id"] 
                response2_bool = True
                print(face_id_2)
            except:
                print("Wrong image2(it's not face image)!!")


            try:
                if response1_bool and response2_bool:
                    response = requests.get(
                        'https://api.imagga.com/v2/faces/similarity?face_id=%s&second_face_id=%s' % (face_id_1, face_id_2),
                        auth=(api_key, api_secret))
                    print(response.json())

                    if response.json()["result"]["score"] >= 80:
                        dbChanges(True, username)
                    else:
                        dbChanges(False, username)
                else:
                    dbChanges(False, username)
                    print("Invalid images!!")
            except:
                dbChanges(False, username)
                print("Wrong Input!!")
           
        

        url = os.environ.get('CLOUDAMQP_URL', "amqps://eixezsax:59gP2X5yKEVXRB7QlkGE6OE6ixNjPi9B@rat.rmq2.cloudamqp.com/eixezsax")
        params = pika.URLParameters(url)
        connection = pika.BlockingConnection(params)
        channel = connection.channel()
        
        channel.queue_declare(queue='users')
        channel.basic_consume(queue='users', on_message_callback=callback, auto_ack=True)
        channel.start_consuming()
        channel.close()
    
    

class StatusView(View):
    
    def get(self, request):
        return render(request, "user_status.html", {"form": CheckNationalIdForm()})
    
    def post(self, request):
        form = CheckNationalIdForm(request.POST)
        if not form.is_valid():
            return JsonResponse({"error": "bad request"}, status="400")   
        try:
            user = User.objects.get(national_id = hash(form.instance.national_id))
            user_ip = user.ip
        except:
            return HttpResponse("User not found", status="404")
        
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        if ip != user_ip:
            return HttpResponse("Illegal Access!!")
        
        if user.state == "pending":
            return HttpResponse("Pending...")
        elif user.state == "rejected.":
            return HttpResponse("Your authentication request has been rejected. Please try again later.")     
        elif user.state == "confirmed.":
            return HttpResponse(f"Your authentication was successfull!! Your username is {user.username}.")


class HomeView(View):
    def get(self, request):
        return render(request, "home.html")

