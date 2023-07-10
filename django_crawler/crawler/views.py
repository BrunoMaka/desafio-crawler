from django.shortcuts import render, redirect
from django.utils import timezone
from django.core.mail import send_mail
from crawler.models import History
from subprocess import run, call
import os, time
from django.http import HttpResponse
import pandas as pd

def index(request):
    current_path = os.getcwd()     
    if request.method == 'POST':     
        tecnologia = request.POST.get('tecnologia')
        tipo_arquivo = request.POST.get('arquivo') 
        historico = History(
            tipo_acionamento=tecnologia, 
            tipo_saida = tipo_arquivo,
            data_acionamento=timezone.now(), 
            tempo_de_coleta=0)        
        historico.save()          
        if tecnologia == 'scrapy':   
            project_path = current_path + f'\\crawler\\imdb_{tecnologia}'
            response, tempo = run_scrapy('imdb', project_path, tipo_arquivo, historico.id)      
        elif tecnologia == 'selenium':
            project_path = current_path + f'\\crawler\\imdb_{tecnologia}'
            response, tempo = run_selenium('imdb', project_path, tipo_arquivo, historico.id)   
        update_history(project_path, historico, tempo)  
        os.chdir(current_path)                      
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
    caminho_arquivo = project_path + f'\\{spider_name}.{file_type}'  
    while len_df(caminho_arquivo) == 0:
        run(['scrapy', 'crawl', spider_name, f'-o{spider_name}.{file_type}', '-a', f'history_id={history_id}']) 
    with open(caminho_arquivo, 'rb') as arquivo:
        response = HttpResponse(arquivo.read(), content_type='application/octet-stream')                
        response['Content-Disposition'] = f'attachment; filename="{spider_name}.{file_type}"'
    os.remove(project_path + f'\\{spider_name}.{file_type}')
    return response
   
@medir_tempo_de_execucao
def run_selenium(name, project_path, tipo_arquivo, historico_id):
    '''import ipdb
    ipdb.set_trace()
    pass'''
    path = os.path.abspath("..\\")
    comando_ativar_ambiente = f'{path}\\venv\\Scripts\\activate && python {project_path}\\main.py {project_path} {name} {tipo_arquivo} {historico_id}'
    call(comando_ativar_ambiente, shell=True)    
    caminho_arquivo = project_path + f'\\{name}.{tipo_arquivo}'
    with open(caminho_arquivo, 'rb') as arquivo:
        response = HttpResponse(arquivo.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = f'attachment; filename="{name}.{tipo_arquivo}"'        
    os.remove(project_path + f'\\{name}.{tipo_arquivo}')
    return response 


def update_history(project_path, historico, tempo):
    historico.tempo_de_coleta = tempo
    with open(project_path + '\\imdb.log', "r", encoding='utf-8') as file:
        log_content = file.read()
    historico.log = log_content
    historico.save()   
    os.remove(project_path + '\\imdb.log')



