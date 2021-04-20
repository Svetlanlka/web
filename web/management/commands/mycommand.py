from django.core.management.base import BaseCommand

class Command(BaseCommand):
    def add_arguments(self, parser):
        parser.add_argument('first')
        parser.add_argument('--option1')
    def handle(self, *args, **options):
        print('Command: mycommand')
        print('Second line')
        print(f'First: {options["first"]}')
        print(f'Option1: {options["option1"]}')
