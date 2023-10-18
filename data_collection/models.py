from django.db import models

class User(models.Model):
    email = models.CharField(max_length= 255)
    last_name = models.CharField(max_length= 255)
    national_id = models.CharField(max_length=255 ,primary_key=True)
    ip = models.CharField(max_length= 20 , default="local_host")
    image1 = models.ImageField(upload_to= "images/")
    image2 = models.ImageField(upload_to= "images/")
    state = models.CharField(max_length= 255, default= "pending")
    username = models.CharField(max_length= 255, default="user" )

    def __str__(self):
        return self.email


