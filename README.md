# Crawler - IMDb

Este é um projeto desenvolvido em Python, para coletar os dados dos top 250 filmes segundo IMDb e os armazenar em um banco de dados. Foram utilizados Django, Scrapy e Selenium para realização do projeto

## Configurações iniciais

Faça o clone do projeto  https://github.com/BrunoMaka/desafio-crawler.git

## Django - Scrapy

### Instalação local

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

Este comando fará as migrações necessárias e executará o runserver

Caso não tenha mais migrações para serem feitas, execute o comando do runserver diretamente

```
python manage.py runserver
```

### Docker

1. Para criar a imagem, execute o comando ```docker-compose up --build```

2. Após subir a imagem, o projeto estará rodando em http://localhost:8000/

## Projeto

O projeto possui 3 telas principais:

1. Index (home)
Nesta tela, escolhe o tipo de saída do arquivo (csv ou json).
Após o clique no botão, um subprocess é realizado para executar o crawler.

É necessário aguardar o processo ser concluído para mudar de página

Um ponto de melhoria seria incluir um overlay e uma mensagem de "aguarde" até o arquivo ser baixado

2. Feedback
Nesta tela, há um campo de mensagem para escrever um feedback do projeto e enviá-lo para meu e-mail

3. Histórico
Nesta tela, há um histórico de coletas, com o tipo de tecnologia e a data da coleta.

Ao clicar, é mostrado alguns dados da coleta, como por exemplo, o tempo em segundos em que a coleta foi feita. É possível ver o Log da coleta nessa tela

## Selenium

Não foi possível incluir o crawler do Selenium para ser executado no Django, porém é possível executa-lo via linha de comando:

1. Na raiz do projeto, faça as etapas 1, 2 e 3 da instalação local acima

2. caminhe para pasta do projeto ```cd django_crawler\crawler\imdb_selenium```

3. execute o comando ```python main.py csv``` para gerar arquivos .csv ou ```python main.py json``` para gerar arquivos json

Apesar do crawler com selenium não ser executado com o Django, as coletas feitas por ele também são salvas no banco de dados e podem ser visualizadas na página de histórico do Django

OBS: algumas linhas de código foram mantidas como comentário, caso encontre uma solução para incluir o crawler do selenium para ser executado com o Django



