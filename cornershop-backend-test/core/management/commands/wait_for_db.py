import time

from django.core.management.base import BaseCommand
from django.db import connections
from django.db.utils import OperationalError


class Command(BaseCommand):
    """Django command to pause excecution until database is available"""

    def handle(self, *args, **kwargs):
        self.stdout.write("Waiting for database...")
        db_connection = None
        while not db_connection:
            try:
                db_connection = connections["default"]
            except OperationalError:
                self.stdout.write("Database unavailable, waiting 1 second")
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS("Database available!"))
