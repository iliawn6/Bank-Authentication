from django import forms
from .models import User

class CreateUserForm(forms.ModelForm):
     
    class Meta:
            model = User
            fields = [
               "email",
               "last_name",
               "national_id",
               "image1",
               "image2",
            ]


class CheckNationalIdForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ["national_id"]
    