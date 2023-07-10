# Crawler - IMDb

Este é um projeto desenvolvido em Python, para coletar os dados dos 250 top filmes do IMDb e os armazenar em um banco de dados.

## Instalação

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

4. Configurações iniciais:
Antes de iniciar, é necessário criar um arquivo de .env e incluir as configurações do seu banco de dados:
O arquivo .env deve conter:

```
DB_NAME = 'nome_do_banco_de_dados'
DB_USER = 'usuario_banco_de_dados'
DB_PASSWORD = 'senha_banco_de_dados'
DB_HOST = 'host_banco_de_dados'
DB_PORT = 'porta_banco_de_dados'
```











