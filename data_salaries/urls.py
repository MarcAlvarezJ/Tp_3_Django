from django.urls import path

from data_salaries import views

urlpatterns = [
    path("",views.index,name="index"),
]