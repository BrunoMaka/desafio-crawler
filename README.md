# Crawler - IMDb

Este é um projeto desenvolvido em Python, para coletar os dados dos top 250 filmes segundo IMDb e os armazenar em um banco de dados. Foram utilizados Django, Scrapy e Selenium para realização do projeto

## Configurações iniciais

Faça o clone do projeto  https://github.com/BrunoMaka/desafio-crawler.git

Na raiz do projeto, crie um arquivo .env que deve conter:

```
DB_NAME = 'nome_do_banco_de_dados'
DB_USER = 'usuario_banco_de_dados'
DB_PASSWORD = 'senha_banco_de_dados'
DB_HOST = 'host_banco_de_dados'
DB_PORT = 'porta_banco_de_dados'
```

## Instalação (local)

Recomenda-se a instalação das dependências do projeto em um ambiente virtual. Siga os passos abaixo:

1. Dentro da raiz do projeto, crie um ambiente virtual:
```
python3 -m venv venv
```

2. Ative o ambiente virtual:
- No Linux/Mac:
  ```
  source venv/bin/activate
  ```
- No Windows:
  ```
  venv\Scripts\activate
  ```

3. Instale as dependências do projeto:
```
pip install -r requirements.txt
```

4. Entre na pasta do projeto ```cd django_crawler``` e execute o comando:

```
python runserver_migrate.py
```

Este comando irá criar um banco de dados conforme o nome estabelecido dentro do arquivo .env (caso ele não exista), fará as migrações necessárias e executará o runserver

Caso não tenha mais migrações para serem feitas, execute o comando do runserver diretamente

```
python manage.py runserver
```

## Projeto

O projeto possui 3 telas principais:

1. Index (home)
Nesta tela, escolhe o tipo de tecnologia (scrapy ou selenium) e o tipo de saída do arquivo (csv ou json).
Após o clique no botão, um subprocess é realizado para executar o crawler escolhido

É necessário aguardar o processo ser concluído para mudar de página

Um ponto de melhoria seria incluir um overlay e uma mensagem de "aguarde" até o arquivo ser baixado

2. Feedback
Nesta tela, há um campo de mensagem para escrever um feedback do projeto e enviá-lo para meu e-mail

3. Histórico
Nesta tela, háum histórico de coletas, com o tipo de tecnologia e a data da coleta.

Ao clicar, é mostrado alguns dados da coleta, como por exemplo, o tempo em segundos em que a coleta foi feita. É possível ver o Log da coleta nessa tela

## Docker
Apesar dos arquivos Dockerfile e docker-compose.yml estarem no projeto, não foi possível concluir a criação da imagem do projeto para roda-lo em um container.

O erro acontece quando vai executar o makemigrations, no qual, não encontra o host e port do banco de dados especificado

Acredito que este seja um ponto de melhoria do projeto





