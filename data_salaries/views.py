from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from data_salaries.forms import upload_file, view_filter
import pandas as pd
from IPython.display import HTML

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
    atr_list = [
        'experience_level',
        'employment_type',
        'employee_residence',
        'remote_ratio',
        'company_location',
        'company_size'
        ]
    if request.method == 'POST':
        filtered_data = data
        form = view_filter(request.POST)
        if form.is_valid():
            for atr in atr_list:
                if form.cleaned_data[atr] != []:
                    filtered_data = filtered_data[filtered_data[atr].isin(form.cleaned_data[atr])]
            html_filtered_data = HTML(filtered_data.to_html()(classes='table table-stripped table-sm'))
            context = {
                'form': form,
                'data': html_filtered_data
            }
            render(request, 'view_csv.html', context)
    else:
        form = view_filter
        html_data = data.to_html()
        context = {
                'form': form,
                'data': html_data
            }
    return render(request, 'view_csv.html', context)
