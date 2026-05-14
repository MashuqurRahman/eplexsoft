from django.core.management.base import BaseCommand
from admin_app.recommendation.similarity import build_similarity_matrix

class Command(BaseCommand):
    help = "Build or update product similarity matrix"

    def handle(self, *args, **kwargs):
        count = build_similarity_matrix()
        self.stdout.write(
            self.style.SUCCESS(f"✅ Matrix updated for {count} products")
        )
