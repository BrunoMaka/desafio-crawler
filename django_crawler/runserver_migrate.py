import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_crawler.settings")
    
    from django.core.management import execute_from_command_line
    from django.core.management.commands import makemigrations, migrate
    
    # Executa as migrações pendentes
    execute_from_command_line([sys.argv[0], "makemigrations"])
    execute_from_command_line([sys.argv[0], "migrate"])

    # Inicia o servidor Django
    execute_from_command_line([sys.argv[0], "runserver"])
