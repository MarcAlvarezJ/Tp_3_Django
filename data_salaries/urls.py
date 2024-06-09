from django.urls import path
from data_salaries import views

urlpatterns = [
    path('upload/', views.upload, name='upload'),
    path('view/', views.view_csv, name='view'),
    path('analisis/', views.analize_data, name='analisis'),
    path('graphs/', views.graphs, name='graphs')
]