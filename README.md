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








