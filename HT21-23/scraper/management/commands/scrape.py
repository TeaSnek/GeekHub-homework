from django.core.management.base import (
    BaseCommand,
    CommandParser,
    CommandError,
)

from scraper.tasks import scrape_prod as scrape


class Command(BaseCommand):
    help = 'Release spider'

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument('products', nargs="+", type=str)

    def handle(self, *args, **options):
        try:
            scrape(options['products'][0].split())
        except ValueError:
            raise CommandError('Invalid product')
