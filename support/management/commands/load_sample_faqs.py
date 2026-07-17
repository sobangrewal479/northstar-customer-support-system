from django.core.management.base import BaseCommand
from support.models import FAQ


class Command(BaseCommand):
    help = "Load sample FAQ data for Northstar Home Co."

    def handle(self, *args, **kwargs):
        sample_faqs = [
            {
                "category": "Shipping",
                "question": "How long does shipping take?",
                "keywords": "shipping, delivery, how long, arrive, ship time",
                "answer": "Standard shipping usually takes 3–6 business days within the United States. Orders are normally processed within 1–2 business days before shipping.",
            },
            {
                "category": "Shipping",
                "question": "Do you offer free shipping?",
                "keywords": "free shipping, shipping cost, delivery fee",
                "answer": "Free standard shipping is available on US orders over $75. Orders below $75 are charged a flat shipping rate at checkout.",
            },
            {
                "category": "Returns",
                "question": "What is your return policy?",
                "keywords": "return, refund, exchange, return policy",
                "answer": "Customers can request a return within 30 days of delivery. Items must be unused, in original condition, and in original packaging.",
            },
            {
                "category": "Returns",
                "question": "How do I start a return?",
                "keywords": "start return, return item, refund request",
                "answer": "To start a return, contact support with your order number and reason for return. Our team will send return instructions if the item qualifies.",
            },
            {
                "category": "Orders",
                "question": "Can I change my order after placing it?",
                "keywords": "change order, edit order, update order, wrong address",
                "answer": "If your order has not shipped yet, our team may be able to update it. Please contact support as soon as possible with your order number.",
            },
            {
                "category": "Orders",
                "question": "Can I cancel my order?",
                "keywords": "cancel order, order cancellation",
                "answer": "Orders can only be canceled before they are processed for shipment. Once an order has shipped, it cannot be canceled, but it may qualify for return after delivery.",
            },
            {
                "category": "Product Info",
                "question": "Are your storage baskets washable?",
                "keywords": "storage basket, washable, clean basket",
                "answer": "Most storage baskets can be spot-cleaned with a damp cloth. We do not recommend machine washing unless the product page specifically says it is machine washable.",
            },
            {
                "category": "Product Info",
                "question": "Are your pantry containers BPA-free?",
                "keywords": "pantry containers, BPA, food safe, plastic",
                "answer": "Yes, our clear pantry containers are BPA-free and designed for dry food storage such as pasta, rice, snacks, and baking ingredients.",
            },
            {
                "category": "Product Info",
                "question": "Do your wall shelves include mounting hardware?",
                "keywords": "wall shelves, hardware, screws, mount",
                "answer": "Most wall shelves include basic mounting hardware. Please check the product description for exact details before purchase.",
            },
            {
                "category": "Damaged Items",
                "question": "What should I do if my item arrived damaged?",
                "keywords": "damaged, broken, defective, arrived damaged",
                "answer": "Please contact support within 7 days of delivery with your order number and clear photos of the damaged item and packaging.",
            },
            {
                "category": "Discounts",
                "question": "Do you offer discount codes?",
                "keywords": "discount, promo code, coupon, sale",
                "answer": "Discount codes may be available during seasonal promotions. Customers can also sign up for our newsletter to receive occasional offers.",
            },
            {
                "category": "Contact",
                "question": "How can I contact customer support?",
                "keywords": "support, contact, help, email",
                "answer": "You can contact our support team through the website contact form. Our typical response time is 1–2 business days.",
            },
        ]

        created_count = 0
        updated_count = 0

        for faq_data in sample_faqs:
            faq, created = FAQ.objects.update_or_create(
                question=faq_data["question"],
                defaults={
                    "category": faq_data["category"],
                    "keywords": faq_data["keywords"],
                    "answer": faq_data["answer"],
                    "is_active": True,
                },
            )

            if created:
                created_count += 1
            else:
                updated_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Sample FAQs loaded. Created: {created_count}, Updated: {updated_count}"
            )
        )