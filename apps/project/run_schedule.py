from django.core.management.base import BaseCommand
from apps.project.models import schedule_update

class Command(BaseCommand):
    help = 'Exécute une mise à jour planifiée'

    def handle(self, *args, **options):
        schedule_update()
        self.stdout.write(self.style.SUCCESS('Mise à jour planifiée effectuée avec succès.'))
