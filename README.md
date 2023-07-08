
# Criar banco de dados:

- mysql -u seu_usuario_do_mysql -p

- CREATE DATABASE beemon

- Em `settings.py`:

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'nome_do_seu_banco_de_dados',
        'USER': 'seu_usuario_do_mysql',
        'PASSWORD': 'sua_senha_do_mysql',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```







