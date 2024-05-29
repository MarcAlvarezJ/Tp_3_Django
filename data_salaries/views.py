from django.http import HttpResponse, HttpResponseRedirect

from django.shortcuts import render
from data_salaries.forms import upload_file

import pandas as pd

# Create your views here.

def upload(request):
    if request.method == 'POST':
        form = upload_file(request.POST, request.FILES)
        if form.is_valid():
            handle_file(request.FILES['upload_file'])
            return HttpResponseRedirect('/data_salaries/success/')
    else:
        form = upload_file
    return render(request, 'upload.html', {'form': form})

def handle_file(file):
    with open("salaries.csv", "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)

def success(request):
    return HttpResponse('Archivo cargado exitosamente')

def view_csv(request):
    data = pd.read_csv('salaries.csv')
    return render(request, 'view_csv.html', {'data': data})
