from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import FAQ, ChatMessage, Lead, UnansweredQuestion
from .views import find_best_matching_faq


class SupportDashboardTests(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(
            username="testadmin",
            password="testpassword123",
        )

        self.free_shipping_faq = FAQ.objects.create(
            question="Do you offer free shipping?",
            answer="Free standard shipping is available on US orders over $75.",
            category="Shipping",
            keywords="free shipping, shipping cost, delivery fee",
            is_active=True,
        )

        self.shipping_time_faq = FAQ.objects.create(
            question="How long does shipping take?",
            answer="Standard shipping usually takes 3–6 business days.",
            category="Shipping",
            keywords="shipping, delivery, how long, arrive, ship time",
            is_active=True,
        )

        self.discount_faq = FAQ.objects.create(
            question="Do you offer discount codes?",
            answer="Discount codes may be available during seasonal promotions.",
            category="Discounts",
            keywords="discount, promo code, coupon, sale",
            is_active=True,
        )

    def test_dashboard_redirects_when_logged_out(self):
        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response.url)

    def test_dashboard_loads_for_logged_in_admin(self):
        self.client.login(
            username="testadmin",
            password="testpassword123",
        )

        response = self.client.get(reverse("dashboard"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Northstar Home Co. Support Dashboard")

    def test_known_question_returns_matching_faq(self):
        matched_faq = find_best_matching_faq("Do you offer free shipping?")

        self.assertEqual(matched_faq, self.free_shipping_faq)

    def test_unknown_question_returns_no_match(self):
        matched_faq = find_best_matching_faq("Do you offer wholesale pricing?")

        self.assertIsNone(matched_faq)

    def test_inactive_faq_is_not_used_by_chatbot(self):
        self.free_shipping_faq.is_active = False
        self.free_shipping_faq.save()

        matched_faq = find_best_matching_faq("Do you offer free shipping?")

        self.assertIsNone(matched_faq)

    def test_chatbot_saves_answered_chat(self):
        response = self.client.post(
            reverse("chat"),
            {
                "action": "ask_question",
                "question": "Do you offer free shipping?",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChatMessage.objects.count(), 1)

        chat = ChatMessage.objects.first()

        self.assertTrue(chat.was_answered)
        self.assertEqual(chat.matched_faq, self.free_shipping_faq)
        self.assertIn("Free standard shipping", chat.bot_answer)
        self.assertContains(response, "Need Follow-Up?")

    def test_chatbot_saves_unanswered_question(self):
        response = self.client.post(
            reverse("chat"),
            {
                "action": "ask_question",
                "question": "Do you offer wholesale pricing?",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ChatMessage.objects.count(), 1)
        self.assertEqual(UnansweredQuestion.objects.count(), 1)

        chat = ChatMessage.objects.first()
        unanswered = UnansweredQuestion.objects.first()

        self.assertFalse(chat.was_answered)
        self.assertIsNone(chat.matched_faq)
        self.assertEqual(unanswered.question, "Do you offer wholesale pricing?")
        self.assertContains(response, "Need Follow-Up?")

    def test_chatbot_creates_lead_from_follow_up_form(self):
        response = self.client.post(
            reverse("chat"),
            {
                "action": "save_lead",
                "original_question": "Can I customize the size of a wall shelf?",
                "name": "Test Lead",
                "email": "lead@example.com",
                "phone": "123456789",
                "product_interest": "Wall Shelves",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(Lead.objects.count(), 1)

        lead = Lead.objects.first()

        self.assertEqual(lead.name, "Test Lead")
        self.assertEqual(lead.email, "lead@example.com")
        self.assertEqual(lead.product_interest, "Wall Shelves")
        self.assertEqual(lead.original_question, "Can I customize the size of a wall shelf?")
        self.assertEqual(lead.status, "New")
        self.assertContains(response, "Follow-Up Details Saved")

    def test_leads_page_loads_for_logged_in_admin(self):
        Lead.objects.create(
            name="Sample Lead",
            email="sample@example.com",
            product_interest="Storage Baskets",
            original_question="Are your baskets washable?",
            source="Chatbot",
            status="New",
        )

        self.client.login(
            username="testadmin",
            password="testpassword123",
        )

        response = self.client.get(reverse("leads"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sample Lead")

    def test_lead_status_can_be_updated(self):
        lead = Lead.objects.create(
            name="Sample Lead",
            email="sample@example.com",
            product_interest="Storage Baskets",
            original_question="Are your baskets washable?",
            source="Chatbot",
            status="New",
        )

        self.client.login(
            username="testadmin",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("lead_update", args=[lead.id]),
            {
                "status": "Contacted",
                "notes": "Followed up with customer.",
            },
        )

        lead.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(lead.status, "Contacted")
        self.assertEqual(lead.notes, "Followed up with customer.")

    def test_unanswered_status_can_be_updated(self):
        unanswered = UnansweredQuestion.objects.create(
            question="Do you ship to Alaska?",
            status="New",
        )

        self.client.login(
            username="testadmin",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("unanswered_update", args=[unanswered.id]),
            {
                "status": "Reviewed",
                "notes": "Needs owner confirmation.",
            },
        )

        unanswered.refresh_from_db()

        self.assertEqual(response.status_code, 302)
        self.assertEqual(unanswered.status, "Reviewed")
        self.assertEqual(unanswered.notes, "Needs owner confirmation.")

    def test_faq_can_be_created(self):
        self.client.login(
            username="testadmin",
            password="testpassword123",
        )

        response = self.client.post(
            reverse("faq_create"),
            {
                "question": "Do you offer gift wrapping?",
                "answer": "Gift wrapping is not currently available.",
                "category": "Store Policy",
                "keywords": "gift wrapping, gift wrap, wrapping",
                "is_active": "on",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            FAQ.objects.filter(question="Do you offer gift wrapping?").exists()
        )

    def test_csv_export_leads_downloads(self):
        Lead.objects.create(
            name="CSV Lead",
            email="csv@example.com",
            product_interest="Pantry Storage",
            original_question="Can you recommend pantry storage?",
            source="Chatbot",
            status="New",
        )

        self.client.login(
            username="testadmin",
            password="testpassword123",
        )

        response = self.client.get(reverse("export_leads_csv"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response["Content-Type"], "text/csv")
        self.assertIn(
            'attachment; filename="northstar_leads.csv"',
            response["Content-Disposition"],
        )