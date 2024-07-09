from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from data_salaries.forms import upload_file, view_filter, analize_filter, employee_info, business_info, employee_amnt
import pandas as pd
import numpy as np
from IPython.display import HTML
import io
import urllib, base64
import matplotlib.pyplot as plt
import itertools
from random import sample, randint

# Create your views here.

def upload(request):
    if request.method == 'POST':
        form = upload_file(request.POST, request.FILES)
        if form.is_valid():
            handle_file(request.FILES['upload_file'])
            return HttpResponseRedirect('/data_salaries/view/')
    else:
        form = upload_file
    return render(request, 'upload.html', {'form': form,'active':0} )

def handle_file(file):
    with open("salaries.csv", "wb+") as destination:
        for chunk in file.chunks():
            destination.write(chunk)


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
                    filtered_data = filtered_data.head(3000).to_dict(orient='records')
            context = {
                'form': form,
                'data': filtered_data,
                'active': 1
            }
            render(request, 'view_csv.html', context)
    else:
        form = view_filter
        data = data.head(3000).to_dict(orient='records')
        context = {
                'form': form,
                'data': data,
                'active': 1
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

            name_change_dict = {
                'experience_level': 'Nivel de Expreiencia', 'employment_type': 'Tipo de Trabajo',
                'employee_residence': 'Residencia Empledo', 'remote_ratio': 'Pct. Remoto',
                'company_location': 'Ubicacion Empresa', 'company_size': 'Tamaño Empresa'
            }

            column_names = [name_change_dict[elem] for elem in filter_list]
            columns = []
            analisis_vars = ['Promedio', 'Mediana', 'Maximo', 'Minimo', 'Q1', 'Q3', 'Cantidad']
            for var in reversed(column_names):
                columns.append(var)
            for var in analisis_vars:
                columns.append(var)

            analized_df = pd.DataFrame(analized_matrix, columns=columns)
            html_analized_data = HTML(analized_df.to_html(classes='table table-stripped table-sm'))
            context = {
                'form': form,
                'data': html_analized_data.data,
                'active': 2
            }
            render(request, 'analisis_dataset.html', context)
    else:
        form = analize_filter
        filtered_data = data
        n_mean = filtered_data['salary_in_usd'].mean()
        n_med = filtered_data['salary_in_usd'].median()
        n_max = filtered_data['salary_in_usd'].max()
        n_min = filtered_data['salary_in_usd'].min()
        n_Q1 = filtered_data['salary_in_usd'].quantile(0.25)
        n_Q3 = filtered_data['salary_in_usd'].quantile(0.75)
        n_count = len(filtered_data)
        analized_matrix = [n_mean, n_med, n_max, n_min, n_Q1, n_Q3, n_count]
        analized_df = pd.DataFrame([analized_matrix], columns=('Promedio', 'Mediana', 'Maximo', 'Minimo', 'Q1', 'Q3', 'Cantidad'))
        html_analized_data = HTML(analized_df.to_html(classes='table table-stripped table-sm'))
        context = {
                'form': form,
                'data': html_analized_data.data,
                'active': 2
            }
    return render(request, 'analisis_dataset.html', context)

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
        'active': 3
    }

    return render(request, 'graficos.html', context)

def redirect_start(request):
    return HttpResponseRedirect('/data_salaries/upload/')

def prediction_select(request):
    context={
        'active': 4,
    }
    return render(request, 'prediction_select.html',context)

def prediction_employee(request):
    try:
        data = pd.read_csv('salaries.csv')
    except FileNotFoundError:
        return HttpResponse('Datos no cargados')
    if request.method == "POST":
        employee_form = employee_info(request.POST)
        if employee_form.is_valid():
            employee_filtered_data = data
            if employee_form.cleaned_data['experience']:
                employee_filtered_data = employee_filtered_data[employee_filtered_data['experience_level'] == employee_form.cleaned_data['experience']]
            if employee_form.cleaned_data['remote']:
                employee_filtered_data = employee_filtered_data[employee_filtered_data['remote_ratio'] == int(employee_form.cleaned_data['remote'])]
            if employee_form.cleaned_data['residence']:
                employee_filtered_data = employee_filtered_data[employee_filtered_data['employee_residence'] == employee_form.cleaned_data['residence']]
            if employee_form.cleaned_data['type']:
                employee_filtered_data = employee_filtered_data[employee_filtered_data['employment_type'] == employee_form.cleaned_data['type']]
            if len(employee_filtered_data) == 0:
                employee_form = employee_info
                context= {
                    'employee_form': employee_form,
                    'error': f'Datos para el empleado no disponibles'
                }                    
                return render(request, 'employee_predict.html', context)
            
            median = employee_filtered_data['salary_in_usd'].median()
            Q1 = employee_filtered_data['salary_in_usd'].quantile(0.25)
            Q3 = employee_filtered_data['salary_in_usd'].quantile(0.75)
            value_list = employee_filtered_data['salary_in_usd'].to_list()

            plt.figure(figsize=(10, 6))
            plt.hist(value_list, weights=np.ones(len(value_list))/len(value_list), bins=30, color='skyblue', edgecolor='black')
            plt.title('Distribución de posibles salarios')
            plt.xlabel('Salario en USD')
            plt.ylabel('Frecuencia')
            plt.ticklabel_format(style='plain')
            buf = io.BytesIO()
            plt.savefig(buf, format='png')
            buf.seek(0)
            string = base64.b64encode(buf.read())
            uri = urllib.parse.quote(string)

            employee_form = employee_info
            context= {
                'employee_form': employee_form,
                'median': median,
                'range': f'{Q1}-{Q3}',
                'uri': uri
            }                    
            return render(request, 'employee_predict.html', context)
        
    else:
        employee_form = employee_info
        context= {
            'employee_form': employee_form
            }                    
        return render(request, 'employee_predict.html', context)
        
def prediction_business(request):
    try:
        data = pd.read_csv('salaries.csv')
    except FileNotFoundError:
        return HttpResponse('Datos no cargados')
    if request.method == "POST":
        amount = (len(request.POST) -3) // 4
        business_form = business_info(request.POST)
        employee_forms = [employee_info(request.POST, prefix=str(x)) for x in range(0,amount)]
        amount_form = employee_amnt(request.POST)
        if amount_form.is_valid():
            amount = amount_form.cleaned_data['amount']
            business_form = business_info()
            employee_forms = [employee_info(prefix=str(x)) for x in range(0,amount)]
            amount_form = employee_amnt()
            context= {
                'business_form': business_form,
                'employee_form': employee_forms,
                'amount_form': amount_form
            }
            return render(request, 'business_predict.html', context)
        if 'location' in dict(request.POST).keys():
            if business_form.is_valid() and all([form.is_valid() for form in employee_forms]):
                business_filtered_data = data
                if business_form.cleaned_data['location']:
                    business_filtered_data = business_filtered_data[business_filtered_data['company_location'] == business_form.cleaned_data['location']]
                if business_form.cleaned_data['size']:
                    business_filtered_data = business_filtered_data[business_filtered_data['company_size'] == business_form.cleaned_data['size']]
                if len(business_filtered_data) == 0:
                    business_form = business_info()
                    employee_forms = [employee_info(prefix=str(x)) for x in range(0,amount)]
                    amount_form = employee_amnt()
                    context= {
                        'business_form': business_form,
                        'employee_form': employee_forms,
                        'amount_form': amount_form,
                        'error': 'Datos para la compania no disponibles'
                    }
                    return render(request, 'business_predict.html', context)
                medians_list = []
                Q1_list = []
                Q3_list = []
                value_list_list = []
                for i, form in enumerate(employee_forms):
                    employee_filtered_data = business_filtered_data
                    if form.cleaned_data['experience']:
                        employee_filtered_data = employee_filtered_data[employee_filtered_data['experience_level'] == form.cleaned_data['experience']]
                    if form.cleaned_data['remote']:
                        employee_filtered_data = employee_filtered_data[employee_filtered_data['remote_ratio'] == int(form.cleaned_data['remote'])]
                    if form.cleaned_data['residence']:
                        employee_filtered_data = employee_filtered_data[employee_filtered_data['employee_residence'] == form.cleaned_data['residence']]
                    if form.cleaned_data['type']:
                        employee_filtered_data = employee_filtered_data[employee_filtered_data['employment_type'] == form.cleaned_data['type']]
                    if len(employee_filtered_data) == 0:
                        business_form = business_info()
                        employee_forms = [employee_info(prefix=str(x)) for x in range(0,amount)]
                        amount_form = employee_amnt()
                        context= {
                            'business_form': business_form,
                            'employee_form': employee_forms,
                            'amount_form': amount_form,
                            'error': f'Datos para el empleado {i + 1} no disponibles'
                        }                    
                        return render(request, 'business_predict.html', context)
                    medians_list.append(employee_filtered_data['salary_in_usd'].median())
                    Q1_list.append(employee_filtered_data['salary_in_usd'].quantile(0.25))
                    Q3_list.append(employee_filtered_data['salary_in_usd'].quantile(0.75))
                    value_list_list.append(employee_filtered_data['salary_in_usd'].to_list())

                median = sum(medians_list)
                Q1 = sum(Q1_list)
                Q3 = sum(Q3_list)

                lengths = [len(lst) for lst in value_list_list]
                total_combinations = 1
                for lst in value_list_list:
                    total_combinations *= len(lst)                
                if total_combinations <= 1000000:
                    combinations = list(itertools.product(*value_list_list))
                else:
                    combinations = []
                    while len(combinations) < 1000000:
                        combination = tuple(lst[randint(0, length - 1)] for lst, length in zip(value_list_list, lengths))
                        combinations.append(combination)
                sums = [sum(list(combination)) for combination in combinations]

                plt.figure(figsize=(10, 6))
                plt.hist(sums, weights=np.ones(len(sums))/len(sums), bins=30, color='skyblue', edgecolor='black')
                plt.title('Distribución de posibles costos')
                plt.xlabel('Costo en USD')
                plt.ylabel('Frecuencia')
                plt.ticklabel_format(style='plain')
                buf = io.BytesIO()
                plt.savefig(buf, format='png')
                buf.seek(0)
                string = base64.b64encode(buf.read())
                uri = urllib.parse.quote(string)

                business_form = business_info()
                employee_forms = [employee_info(prefix=str(x)) for x in range(0,amount)]
                amount_form = employee_amnt()
                context= {
                    'business_form': business_form,
                    'employee_form': employee_forms,
                    'amount_form': amount_form,
                    'median': median,
                    'range': f'{Q1}-{Q3}',
                    'uri': uri
                }                    
                return render(request, 'business_predict.html', context)
            
        amount_form = employee_amnt()
        context={
            'amount_form': amount_form,
            'error': 'El valor tiene que ser positivo con 5 como maximo'
            }
        return render(request, 'business_predict.html', context)  
    else:
        amount_form = employee_amnt()
        return render(request, 'business_predict.html', {'amount_form': amount_form})  