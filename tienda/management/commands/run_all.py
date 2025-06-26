from django.core.management.base import BaseCommand
import subprocess
import threading

class Command(BaseCommand):
    help = "Corre servidor Django y proceso paralelo"

    def handle(self, *args, **kwargs):
        def run_django():
            subprocess.call(['python', 'manage.py', 'runserver'])

        def run_proceso_extra():
            # Cambiá esto por el proceso extra (por ejemplo, uno para login o admin)
            subprocess.call(['python', 'manage.py', 'correr_login_extra'])  # ejemplo ficticio

        # Lanzar ambos en paralelo
        threading.Thread(target=run_django).start()
        threading.Thread(target=run_proceso_extra).start()
