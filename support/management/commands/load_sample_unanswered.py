from django.core.management.base import BaseCommand
from support.models import UnansweredQuestion


class Command(BaseCommand):
    help = "Load sample unanswered question data for Northstar Home Co."

    def handle(self, *args, **kwargs):
        sample_unanswered_questions = [
            {
                "question": "Can you recommend a full pantry setup for a family of six?",
                "status": "New",
                "notes": "Could become future product recommendation FAQ.",
            },
            {
                "question": "Do you ship to Alaska and Hawaii?",
                "status": "New",
                "notes": "Need owner confirmation.",
            },
            {
                "question": "Can I pay in installments?",
                "status": "Reviewed",
                "notes": "Payment plan not currently supported.",
            },
            {
                "question": "Do you offer wholesale pricing?",
                "status": "New",
                "notes": "Potential B2B opportunity.",
            },
            {
                "question": "Can I customize the size of a wall shelf?",
                "status": "Reviewed",
                "notes": "Custom products not currently offered.",
            },
            {
                "question": "Are your baskets made in the USA?",
                "status": "New",
                "notes": "Need supplier/material information.",
            },
            {
                "question": "Can I schedule delivery for a specific date?",
                "status": "New",
                "notes": "Need shipping provider confirmation.",
            },
            {
                "question": "Do you have a designer consultation service?",
                "status": "Ignored",
                "notes": "Out of current service scope.",
            },
        ]

        created_count = 0
        updated_count = 0

        for unanswered_data in sample_unanswered_questions:
            unanswered_question, created = UnansweredQuestion.objects.update_or_create(
                question=unanswered_data["question"],
                defaults={
                    "status": unanswered_data["status"],
                    "notes": unanswered_data["notes"],
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample unanswered questions loaded. Created: {created_count}, Updated: {updated_count}"
            )
        )