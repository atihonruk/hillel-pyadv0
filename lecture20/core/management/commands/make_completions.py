from django.core.management.base import BaseCommand


from core.models import Book
from core.autocomplete import model_completions



class Command(BaseCommand):
    help = 'Make completions'

    # def add_argument(self, parser):
    #    pass
    
    def handle(self, *args, **options):
        count = len(model_completions(Book, 'title'))
        self.stdout.write(f'{count} completions added')
