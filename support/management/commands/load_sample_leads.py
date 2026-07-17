from django.core.management.base import BaseCommand
from support.models import Lead


class Command(BaseCommand):
    help = "Load sample lead data for Northstar Home Co."

    def handle(self, *args, **kwargs):
        sample_leads = [
            {
                "name": "Jessica Miller",
                "email": "jessica.miller@example.com",
                "phone": "303-555-0184",
                "product_interest": "Pantry Storage Set",
                "original_question": "Can you recommend a full pantry setup for a family of six?",
                "source": "Chatbot",
                "status": "New",
                "notes": "Interested in large pantry bundle.",
            },
            {
                "name": "Ryan Cooper",
                "email": "ryan.cooper@example.com",
                "phone": "720-555-0169",
                "product_interest": "Wall Shelves",
                "original_question": "Can I customize the size of a wall shelf?",
                "source": "Chatbot",
                "status": "New",
                "notes": "Wants custom sizing, not currently offered.",
            },
            {
                "name": "Amanda Brooks",
                "email": "amanda.brooks@example.com",
                "phone": "512-555-0112",
                "product_interest": "Storage Baskets",
                "original_question": "Are your baskets made in the USA?",
                "source": "Chatbot",
                "status": "Contacted",
                "notes": "Asked about product origin and materials.",
            },
            {
                "name": "Daniel Harris",
                "email": "daniel.harris@example.com",
                "phone": "214-555-0147",
                "product_interest": "Bulk Office Organization Order",
                "original_question": "Do you offer wholesale pricing?",
                "source": "Chatbot",
                "status": "Qualified",
                "notes": "Potential bulk order for office storage.",
            },
            {
                "name": "Rachel Evans",
                "email": "rachel.evans@example.com",
                "phone": "602-555-0191",
                "product_interest": "Laundry Room Storage",
                "original_question": "Can I schedule delivery for a specific date?",
                "source": "Chatbot",
                "status": "New",
                "notes": "Moving into a new home next month.",
            },
            {
                "name": "Olivia Parker",
                "email": "olivia.parker@example.com",
                "phone": "415-555-0155",
                "product_interest": "Designer Consultation",
                "original_question": "Do you have a designer consultation service?",
                "source": "Chatbot",
                "status": "Not Interested",
                "notes": "Service not offered at this stage.",
            },
        ]

        created_count = 0
        updated_count = 0

        for lead_data in sample_leads:
            lead, created = Lead.objects.update_or_create(
                email=lead_data["email"],
                defaults=lead_data,
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample leads loaded. Created: {created_count}, Updated: {updated_count}"
            )
        )