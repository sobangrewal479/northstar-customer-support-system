from django.contrib import admin
from .models import FAQ, ChatMessage, Lead, UnansweredQuestion


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "category", "is_active", "created_at", "updated_at")
    list_filter = ("category", "is_active")
    search_fields = ("question", "answer", "keywords")


@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ("customer_question", "was_answered", "matched_faq", "customer_email", "created_at")
    list_filter = ("was_answered", "created_at")
    search_fields = ("customer_question", "bot_answer", "customer_email")


@admin.register(Lead)
class LeadAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "product_interest", "status", "source", "created_at")
    list_filter = ("status", "source", "created_at")
    search_fields = ("name", "email", "phone", "product_interest", "original_question")


@admin.register(UnansweredQuestion)
class UnansweredQuestionAdmin(admin.ModelAdmin):
    list_display = ("question", "status", "customer_email", "created_at", "resolved_at")
    list_filter = ("status", "created_at")
    search_fields = ("question", "customer_email", "notes")