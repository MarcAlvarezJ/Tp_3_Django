from django.urls import path
from data_salaries import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('success/', views.success, name='success'),
    path('view/', views.view_csv, name='view')
]