from django.core.management.base import BaseCommand
from support.models import FAQ, ChatMessage


class Command(BaseCommand):
    help = "Load sample chat history data for Northstar Home Co."

    def handle(self, *args, **kwargs):
        sample_chats = [
            {
                "customer_question": "How long does shipping take?",
                "bot_answer": "Standard shipping usually takes 3–6 business days within the United States. Orders are normally processed within 1–2 business days before shipping.",
                "was_answered": True,
                "matched_faq_question": "How long does shipping take?",
            },
            {
                "customer_question": "Do you offer free shipping?",
                "bot_answer": "Free standard shipping is available on US orders over $75. Orders below $75 are charged a flat shipping rate at checkout.",
                "was_answered": True,
                "matched_faq_question": "Do you offer free shipping?",
            },
            {
                "customer_question": "Can I return an item?",
                "bot_answer": "Customers can request a return within 30 days of delivery. Items must be unused, in original condition, and in original packaging.",
                "was_answered": True,
                "matched_faq_question": "What is your return policy?",
            },
            {
                "customer_question": "Can I customize the size of a wall shelf?",
                "bot_answer": "Sorry, I don’t have the exact answer to that yet. Please leave your name and email, and our team will follow up.",
                "was_answered": False,
                "matched_faq_question": None,
            },
            {
                "customer_question": "My item arrived broken.",
                "bot_answer": "Please contact support within 7 days of delivery with your order number and clear photos of the damaged item and packaging.",
                "was_answered": True,
                "matched_faq_question": "What should I do if my item arrived damaged?",
            },
            {
                "customer_question": "Do you offer wholesale pricing?",
                "bot_answer": "Sorry, I don’t have the exact answer to that yet. Please leave your name and email, and our team will follow up.",
                "was_answered": False,
                "matched_faq_question": None,
            },
            {
                "customer_question": "Are your containers BPA free?",
                "bot_answer": "Yes, our clear pantry containers are BPA-free and designed for dry food storage such as pasta, rice, snacks, and baking ingredients.",
                "was_answered": True,
                "matched_faq_question": "Are your pantry containers BPA-free?",
            },
            {
                "customer_question": "Can I change my shipping address?",
                "bot_answer": "If your order has not shipped yet, our team may be able to update it. Please contact support as soon as possible with your order number.",
                "was_answered": True,
                "matched_faq_question": "Can I change my order after placing it?",
            },
            {
                "customer_question": "Do you ship to Alaska?",
                "bot_answer": "Sorry, I don’t have the exact answer to that yet. Please leave your name and email, and our team will follow up.",
                "was_answered": False,
                "matched_faq_question": None,
            },
            {
                "customer_question": "How can I contact support?",
                "bot_answer": "You can contact our support team through the website contact form. Our typical response time is 1–2 business days.",
                "was_answered": True,
                "matched_faq_question": "How can I contact customer support?",
            },
        ]

        created_count = 0
        updated_count = 0

        for chat_data in sample_chats:
            matched_faq = None

            if chat_data["matched_faq_question"]:
                matched_faq = FAQ.objects.filter(
                    question=chat_data["matched_faq_question"]
                ).first()

            chat, created = ChatMessage.objects.update_or_create(
                customer_question=chat_data["customer_question"],
                defaults={
                    "bot_answer": chat_data["bot_answer"],
                    "was_answered": chat_data["was_answered"],
                    "matched_faq": matched_faq,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample chats loaded. Created: {created_count}, Updated: {updated_count}"
            )
        )