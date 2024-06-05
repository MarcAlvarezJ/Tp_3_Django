from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from data_salaries.forms import upload_file, view_filter, analize_filter
import pandas as pd
from IPython.display import HTML
import io
import urllib, base64
import matplotlib.pyplot as plt

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
    try:
        data = pd.read_csv('salaries.csv')
    except FileNotFoundError:
        return HttpResponse('Datos no cargados')
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
            html_filtered_data = HTML(filtered_data.to_html(classes='table table-stripped table-sm'))
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

def analize_data(request):
    try:
        data = pd.read_csv('salaries.csv')
    except FileNotFoundError:
        return HttpResponse('Datos no cargados')
    if request.method == 'POST':      
        form = analize_filter(request.POST)
        if form.is_valid():
            filtered_data = data
            filter_list = form.cleaned_data['filter_vars']
            def grouping_recursive(data_levels_list, row_vars_list, counter, recursive_count):
                if counter == -1:
                    n_mean = (data_levels_list[recursive_count])['salary_in_usd'].mean()
                    n_med = (data_levels_list[recursive_count])['salary_in_usd'].median()
                    n_max = (data_levels_list[recursive_count])['salary_in_usd'].max()
                    n_min = (data_levels_list[recursive_count])['salary_in_usd'].min()
                    n_Q1 = (data_levels_list[recursive_count])['salary_in_usd'].quantile(0.25)
                    n_Q3 = (data_levels_list[recursive_count])['salary_in_usd'].quantile(0.75)
                    n_count = len(data_levels_list[recursive_count].index)
                    new_list_data = [round(n_mean, 2), n_med, n_max, n_min, n_Q1, n_Q3, n_count]
                    for elem in new_list_data:
                        row_vars_list[recursive_count].append(elem)
                    analized_matrix.append(row_vars_list[recursive_count])
                    return
                else:
                    unique_values = data_levels_list[recursive_count][filter_list[counter]].unique()
                    for uniq in unique_values:
                        row_vars_list[recursive_count + 1] = (row_vars_list[recursive_count].copy())
                        row_vars_list[recursive_count + 1].append(uniq)
                        data_levels_list[recursive_count + 1] = data_levels_list[recursive_count][data_levels_list[recursive_count][filter_list[counter]] == uniq]
                        grouping_recursive(data_levels_list, row_vars_list, counter - 1, recursive_count + 1)
            counter = len(filter_list) - 1
            recursive_count = 0
            data_levels_list = [filtered_data, 1, 2, 3, 4, 5, 6]
            row_vars_list = [[], 1, 2, 3, 4, 5, 6]
            analized_matrix = []
            grouping_recursive(data_levels_list, row_vars_list, counter, recursive_count)

            columns = []
            analisis_vars = ['mean', 'median', 'max', 'min', 'Q1', 'Q3', 'Count']
            for var in filter_list:
                columns.append(var)
            for var in analisis_vars:
                columns.append(var)

            analized_df = pd.DataFrame(analized_matrix, columns=columns)
            html_analized_data = HTML(analized_df.to_html(classes='table table-stripped table-sm'))
            context = {
                'form': form,
                'data': html_analized_data.data
            }
            render(request, 'csv_analisis.html', context)
    else:
        form = analize_filter
        filtered_data = data
        n_mean = filtered_data['salary_in_usd'].mean()
        n_med = filtered_data['salary_in_usd'].median()
        n_max = filtered_data['salary_in_usd'].max()
        n_min = filtered_data['salary_in_usd'].min()
        n_Q1 = filtered_data['salary_in_usd'].quantile(0.25)
        n_Q3 = filtered_data['salary_in_usd'].quantile(0.75)
        analized_matrix = [n_mean, n_med, n_max, n_min, n_Q1, n_Q3]
        analized_df = pd.DataFrame([analized_matrix], columns=('Mean', 'Median', 'Max', 'Min', 'Q1', 'Q3'))
        html_analized_data = HTML(analized_df.to_html(classes='table table-stripped table-sm'))
        context = {
                'form': form,
                'data': html_analized_data.data
            }
    return render(request, 'view_csv.html', context)

def graphs(request):
    try:
        data = pd.read_csv('salaries.csv')
    except FileNotFoundError:
        return HttpResponse('Datos no cargados')
    
    plt.figure(figsize=(10, 6))
    plt.hist(data['salary_in_usd'], bins=30, color='skyblue', edgecolor='black')
    plt.title('Distribución de Salarios')
    plt.xlabel('Salario en USD')
    plt.ylabel('Frecuencia')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri_1 = urllib.parse.quote(string)


    plt.figure(figsize=(10, 6))
    plt.scatter(data['experience_level'], data['salary_in_usd'], color='skyblue')
    plt.title('Salario vs. Experiencia')
    plt.xlabel('Nivel de Experiencia')
    plt.ylabel('Salario en USD')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri_2 = urllib.parse.quote(string)
    
    plt.figure(figsize=(10, 6))
    data.groupby('employment_type')['salary_in_usd'].mean().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Salarios por Tipo de Empleo')
    plt.xlabel('Tipo de Empleo')
    plt.ylabel('Salario Promedio en USD')
    plt.xticks(rotation=0)
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri_3 = urllib.parse.quote(string)

    plt.figure(figsize=(10, 6))
    bp = data.boxplot(column='salary_in_usd', by='company_size', patch_artist=True,
                  boxprops=dict(facecolor='skyblue', color='black'), 
                  capprops=dict(color='black'),
                  whiskerprops=dict(color='black'),
                  flierprops=dict(color='black', markeredgecolor='black'),
                  medianprops=dict(color='black'))
    plt.suptitle('')
    plt.title('Salarios por Tamaño de la Empresa')
    plt.xlabel('Tamaño de la Empresa')
    plt.ylabel('Salario en USD')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri_4 = urllib.parse.quote(string)

    plt.figure(figsize=(10, 6))
    data.groupby('remote_ratio')['salary_in_usd'].mean().plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('Ratio de Trabajo Remoto vs. Salario')
    plt.xlabel('Ratio de Trabajo Remoto')
    plt.ylabel('Salario en USD')
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri_5 = urllib.parse.quote(string)

    context = {
        'sal_hist': uri_1,
        'el_scat': uri_2,
        'et_bars': uri_3,
        'cs_box': uri_4,
        'rr_bars': uri_5,
    }

    return render(request, 'graficos.html', context)

def redirect_start(request):
    return HttpResponseRedirect('/data_salaries/upload/')