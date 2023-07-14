from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.core.mail import send_mail
from crawler.models import History, Movie
from subprocess import run, call
import os, time
from django.http import HttpResponse
import pandas as pd


def index(request):
    current_path = os.getcwd()     
    if request.method == 'POST':     
        #tecnologia = request.POST.get('tecnologia')
        tecnologia = 'scrapy'
        tipo_arquivo = request.POST.get('arquivo') 
        historico = History(
            tipo_acionamento=tecnologia, 
            tipo_saida = tipo_arquivo,
            data_acionamento=timezone.now(), 
            tempo_de_coleta=0)        
        historico.save()          
        #if tecnologia == 'scrapy':   
        project_path_docker = os.path.join(current_path, 'django_crawler', 'crawler', 'imdb_scrapy')
        project_path_local = os.path.join(current_path, 'crawler', 'imdb_scrapy')
        try:
            response, tempo = run_scrapy('imdb', project_path_docker, tipo_arquivo, historico.id) 
            project_path =  project_path_docker
        except:
            response, tempo = run_scrapy('imdb', project_path_local, tipo_arquivo, historico.id)
            project_path = project_path_local
        '''elif tecnologia == 'selenium':
            project_path = os.path.join(current_path, 'django_crawler', 'crawler', 'imdb_selenium')
            response, tempo = run_selenium('imdb', project_path, tipo_arquivo, historico.id) '''  
        update_history(project_path, historico, tempo)  
        os.chdir(current_path)           
        return response
    return render(request, 'index.html')

def feedback(request):
    if request.method == 'POST':
        texto = request.POST.get('texto')
        send_mail('Feedback', texto, 'desafio_beemon@hotmail.com', ['brunoduartedeoliveira@hotmail.com'])
        return redirect('index')
    return render(request, 'feedback.html')


def history(request):
    historico = History.objects.all().order_by('-id')
    return render(request, 'history.html', {'historico': historico})

def len_df(file_path):
    if file_path.split('.')[-1] == 'csv':
        try:
            return len(pd.read_csv(file_path))      
        except:
            return 0
    elif file_path.split('.')[-1] == 'json':
        try:
            return len(pd.read_json(file_path))    
        except:
            return 0    

def medir_tempo_de_execucao(funcao):
    def wrapper(*args, **kwargs):
        inicio = time.time()  
        resultado = funcao(*args, **kwargs)  
        fim = time.time()  
        tempo_total = fim - inicio 
        return resultado, tempo_total  
    return wrapper

@medir_tempo_de_execucao
def run_scrapy(spider_name, project_path, file_type, history_id):   
    os.chdir(project_path) 
    run(['scrapy', 'crawl', spider_name, f'-o{spider_name}.{file_type}', '-a', f'history_id={history_id}']) 
    caminho_arquivo = os.path.join(project_path, f'{spider_name}.{file_type}')
    while len_df(caminho_arquivo) == 0:
        run(['scrapy', 'crawl', spider_name, f'-o{spider_name}.{file_type}', '-a', f'history_id={history_id}']) 
    with open(caminho_arquivo, 'rb') as arquivo:
        response = HttpResponse(arquivo.read(), content_type='application/octet-stream')                
        response['Content-Disposition'] = f'attachment; filename="{spider_name}.{file_type}"'
    os.remove(os.path.join(project_path, f'{spider_name}.{file_type}'))
    return response
   
'''@medir_tempo_de_execucao
def run_selenium(name, project_path, tipo_arquivo, historico_id):
    #path = os.path.abspath("..")
    comando_ativar_ambiente = f'python {os.path.join(project_path, "main.py")} {project_path} {name} {tipo_arquivo} {historico_id}'
    call(comando_ativar_ambiente, shell=True)
    caminho_arquivo = os.path.join(project_path, f'{name}.{tipo_arquivo}')
    with open(caminho_arquivo, 'rb') as arquivo:
        response = HttpResponse(arquivo.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{name}.{tipo_arquivo}"'
    os.remove(os.path.join(project_path, f'{name}.{tipo_arquivo}'))
    return response'''


def update_history(project_path, historico, tempo):
    historico.tempo_de_coleta = tempo
    with open(os.path.join(project_path, 'imdb.log'), "r", encoding='utf-8') as file:
        log_content = file.read()
    historico.log = log_content
    historico.save()
    os.remove(os.path.join(project_path, 'imdb.log'))


def infos(request, history_id):    
    historico = History.objects.get(id=history_id)
    crawler_movies = Movie.objects.filter(history_id=history_id)    
    context = {
        'history': historico,
        'crawler_movies': crawler_movies
    }    
    return render(request, 'infos.html', context)

def log_view(request, history_id):
    history = get_object_or_404(History, id=history_id)
    return render(request, 'log.html', {'history': history})