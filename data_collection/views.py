from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from django.views import View
from .forms import CreateUserForm, CheckNationalIdForm
from .models import User

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
            
        new_user = User(email = form.instance.email, last_name = form.instance.last_name, 
                        national_id = hash(form.instance.national_id), ip = ip,
                        image1 = (form.instance.last_name + str(form.instance.national_id)[0:6] + ".img1"),
                        image2 = (form.instance.last_name + str(form.instance.national_id)[0:6] + ".img2"),
                        username = (form.instance.last_name + str(form.instance.national_id)[0:6]))
        
        new_user.save()

        return HttpResponse("Your authentication request has been registered!!")
    

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

