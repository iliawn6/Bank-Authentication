from django.urls import path
from .views import hello, collectApiView, SubmitInfoView, StatusView


urlpatterns = [
    path("hello/", hello),
    path("info/", SubmitInfoView.as_view(), name= "info"),
    path("status/", StatusView.as_view(),name= "status"),
]