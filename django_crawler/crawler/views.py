from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import send_mail
from crawler.models import History
from subprocess import run
import os
from django.http import HttpResponse
import pandas as pd

def index(request):
    current_path = os.getcwd()     
    if request.method == 'POST':        
        tecnologia = request.POST.get('tecnologia')
        arquivo = request.POST.get('arquivo')        
        if tecnologia == 'scrapy':   
            project_path = current_path + f'\\crawler\\imdb_{tecnologia}'
            response = run_scrapy('imdb', project_path)                              
            os.chdir(current_path)                
        elif tecnologia == 'selenium':
            project_path = current_path + f'\\crawler\\imdb_{tecnologia}'
            response = run_selenium(project_path)                              
            os.chdir(current_path)  
        historico = History(tipo_acionamento=tecnologia, data_acionamento=timezone.now())
        historico.save() 
        return response               
    return render(request, 'index.html')

def feedback(request):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        send_mail('Feedback', texto, 'seu_email@gmail.com', ['brunoduartedeoliveira@hotmail.com'])
        return redirect('index')

    return render(request, 'feedback.html')


def history(request):
    historico = History.objects.all()
    return render(request, 'history.html', {'historico': historico})

def run_scrapy(spider_name, project_path):
    df = pd.DataFrame()
    df.to_csv(project_path + f'\\{spider_name}.csv')
    while len(df) == 0:
        os.chdir(project_path) 
        run(['scrapy', 'crawl', spider_name]) 
        caminho_arquivo = project_path + '\\imdb.csv'
        df = pd.read_csv(project_path + f'\\{spider_name}.csv')
        if len(df) > 0:
            df = pd.read_csv(project_path + f'\\{spider_name}.csv', header=1)
            df.to_csv(project_path + f'\\{spider_name}.csv', index=False)
            with open(caminho_arquivo, 'rb') as arquivo:
                response = HttpResponse(arquivo.read(), content_type='application/octet-stream')                
                response['Content-Disposition'] = 'attachment; filename="imdb.csv"'                
    os.remove(project_path + f'\\{spider_name}.csv')
    return response

def run_selenium(project_path):
    os.chdir(project_path) 
    run(['python', 'main.py'])    
    caminho_arquivo = project_path + '\\imdb.csv'
    with open(caminho_arquivo, 'rb') as arquivo:
        response = HttpResponse(arquivo.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename="imdb.csv"' 
    return response 