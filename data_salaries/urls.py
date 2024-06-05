from django.urls import path
from data_salaries import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('view/', views.view_csv, name='view'),
    path('graficos/', views.graficos, name='graficos'),
    path('Analisis/', views.Analisis, name='Analisis'),
]