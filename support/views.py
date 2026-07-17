import csv
import re

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    ChatbotForm,
    FAQForm,
    LeadCaptureForm,
    LeadUpdateForm,
    UnansweredQuestionUpdateForm,
)
from .models import FAQ, ChatMessage, Lead, UnansweredQuestion


FALLBACK_RESPONSE = (
    "Sorry, I don't have the exact answer to that yet. "
    "Please leave your name and email, and our team will follow up."
)


COMMON_WORDS = {
    "the", "a", "an", "and", "or", "to", "of", "in", "on", "for", "with",
    "is", "are", "do", "does", "did", "you", "your", "i", "my", "we", "our",
    "can", "could", "would", "should", "what", "how", "when", "where", "why",
    "after", "about", "it", "this", "that", "have", "has", "had", "offer",
    "offers", "available", "need", "want", "please",
}


def normalize_text(text):
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def get_meaningful_words(text):
    normalized_text = normalize_text(text)
    words = normalized_text.split()

    return [
        word
        for word in words
        if word not in COMMON_WORDS and len(word) > 2
    ]


def find_best_matching_faq(customer_question):
    """
    Finds the best active FAQ match for a customer question.

    MVP rule:
    - Multi-word keywords are strongest.
    - Specific single-word keywords can match.
    - Broad single words like "shipping" are weak alone.
    """

    ambiguous_single_keywords = {
        "shipping",
        "delivery",
        "order",
        "orders",
        "item",
        "items",
        "product",
        "products",
        "support",
        "help",
        "customer",
        "customers",
    }

    question_text = normalize_text(customer_question)
    question_words = set(get_meaningful_words(customer_question))
    active_faqs = FAQ.objects.filter(is_active=True)

    best_faq = None
    best_score = 0

    for faq in active_faqs:
        score = 0

        keywords = [
            normalize_text(keyword)
            for keyword in faq.keywords.split(",")
            if keyword.strip()
        ]

        for keyword in keywords:
            keyword_words = get_meaningful_words(keyword)

            if not keyword_words:
                continue

            if len(keyword_words) == 1:
                keyword_word = keyword_words[0]

                if keyword_word in question_words:
                    if keyword_word in ambiguous_single_keywords:
                        score += 2
                    else:
                        score += 5

                continue

            if keyword in question_text:
                score += 10 + len(keyword_words)
                continue

            if all(word in question_words for word in keyword_words):
                score += 6 + len(keyword_words)
                continue

            shared_words = set(keyword_words).intersection(question_words)
            distinctive_shared_words = [
                word
                for word in shared_words
                if word not in ambiguous_single_keywords
            ]

            if distinctive_shared_words:
                score += len(distinctive_shared_words) * 4

        if score > best_score:
            best_score = score
            best_faq = faq

    if best_score >= 5:
        return best_faq

    return None


def chat_view(request):
    bot_answer = None
    was_answered = False
    matched_faq = None
    lead_saved = False
    submitted_question = None
    show_lead_form = False

    question_form = ChatbotForm()
    lead_form = LeadCaptureForm()

    if request.method == "POST":
        action = request.POST.get("action")

        if action == "ask_question":
            question_form = ChatbotForm(request.POST)

            if question_form.is_valid():
                question = question_form.cleaned_data["question"]
                submitted_question = question

                matched_faq = find_best_matching_faq(question)

                if matched_faq:
                    bot_answer = matched_faq.answer
                    was_answered = True
                else:
                    bot_answer = FALLBACK_RESPONSE
                    was_answered = False

                    UnansweredQuestion.objects.create(
                        question=question,
                        status="New",
                    )

                ChatMessage.objects.create(
                    customer_question=question,
                    bot_answer=bot_answer,
                    was_answered=was_answered,
                    matched_faq=matched_faq,
                )

                lead_form = LeadCaptureForm(
                    initial={
                        "original_question": question,
                    }
                )
                show_lead_form = True
                question_form = ChatbotForm()

        elif action == "save_lead":
            lead_form = LeadCaptureForm(request.POST)

            if lead_form.is_valid():
                original_question = lead_form.cleaned_data["original_question"]
                name = lead_form.cleaned_data["name"]
                email = lead_form.cleaned_data["email"]
                phone = lead_form.cleaned_data.get("phone", "")
                product_interest = lead_form.cleaned_data.get("product_interest", "")

                Lead.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    product_interest=product_interest,
                    original_question=original_question,
                    source="Chatbot",
                    status="New",
                )

                related_chat = ChatMessage.objects.filter(
                    customer_question=original_question
                ).order_by("-created_at").first()

                if related_chat:
                    related_chat.customer_name = name
                    related_chat.customer_email = email
                    related_chat.save()

                related_unanswered = UnansweredQuestion.objects.filter(
                    question=original_question
                ).order_by("-created_at").first()

                if related_unanswered:
                    related_unanswered.customer_email = email
                    related_unanswered.save()

                lead_saved = True
                submitted_question = original_question
                show_lead_form = False
                lead_form = LeadCaptureForm(
                    initial={
                        "original_question": original_question,
                    }
                )
            else:
                submitted_question = request.POST.get("original_question", "")
                show_lead_form = True

    context = {
        "form": question_form,
        "lead_form": lead_form,
        "bot_answer": bot_answer,
        "was_answered": was_answered,
        "matched_faq": matched_faq,
        "lead_saved": lead_saved,
        "submitted_question": submitted_question,
        "show_lead_form": show_lead_form,
    }

    return render(request, "support/chat.html", context)


@login_required
def dashboard_view(request):
    total_chats = ChatMessage.objects.count()
    answered_chats = ChatMessage.objects.filter(was_answered=True).count()
    unanswered_chats = ChatMessage.objects.filter(was_answered=False).count()
    total_leads = Lead.objects.count()
    new_leads = Lead.objects.filter(status="New").count()
    active_faqs = FAQ.objects.filter(is_active=True).count()

    if total_chats > 0:
        answer_rate = round((answered_chats / total_chats) * 100, 1)
        fallback_rate = round((unanswered_chats / total_chats) * 100, 1)
    else:
        answer_rate = 0
        fallback_rate = 0

    recent_chats = ChatMessage.objects.all()[:5]
    recent_leads = Lead.objects.all()[:5]
    recent_unanswered = UnansweredQuestion.objects.all()[:5]

    context = {
        "total_chats": total_chats,
        "answered_chats": answered_chats,
        "unanswered_chats": unanswered_chats,
        "total_leads": total_leads,
        "new_leads": new_leads,
        "active_faqs": active_faqs,
        "answer_rate": answer_rate,
        "fallback_rate": fallback_rate,
        "recent_chats": recent_chats,
        "recent_leads": recent_leads,
        "recent_unanswered": recent_unanswered,
    }

    return render(request, "support/dashboard.html", context)


@login_required
def chat_history_view(request):
    chats = ChatMessage.objects.all()

    context = {
        "chats": chats,
    }

    return render(request, "support/chat_history.html", context)


@login_required
def leads_view(request):
    leads = Lead.objects.all()

    context = {
        "leads": leads,
    }

    return render(request, "support/leads.html", context)


@login_required
def lead_update_view(request, lead_id):
    lead = get_object_or_404(Lead, id=lead_id)

    if request.method == "POST":
        form = LeadUpdateForm(request.POST, instance=lead)

        if form.is_valid():
            form.save()
            return redirect("leads")
    else:
        form = LeadUpdateForm(instance=lead)

    context = {
        "form": form,
        "lead": lead,
    }

    return render(request, "support/lead_update.html", context)


@login_required
def unanswered_questions_view(request):
    unanswered_questions = UnansweredQuestion.objects.all()

    context = {
        "unanswered_questions": unanswered_questions,
    }

    return render(request, "support/unanswered.html", context)


@login_required
def unanswered_update_view(request, unanswered_id):
    unanswered_question = get_object_or_404(UnansweredQuestion, id=unanswered_id)

    if request.method == "POST":
        form = UnansweredQuestionUpdateForm(
            request.POST,
            instance=unanswered_question,
        )

        if form.is_valid():
            form.save()
            return redirect("unanswered_questions")
    else:
        form = UnansweredQuestionUpdateForm(instance=unanswered_question)

    context = {
        "form": form,
        "unanswered_question": unanswered_question,
    }

    return render(request, "support/unanswered_update.html", context)


@login_required
def faq_list_view(request):
    faqs = FAQ.objects.all()

    context = {
        "faqs": faqs,
    }

    return render(request, "support/faq_list.html", context)


@login_required
def faq_create_view(request):
    if request.method == "POST":
        form = FAQForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("faq_list")
    else:
        form = FAQForm()

    context = {
        "form": form,
        "page_title": "Add FAQ",
        "button_text": "Save FAQ",
    }

    return render(request, "support/faq_form.html", context)


@login_required
def faq_update_view(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)

    if request.method == "POST":
        form = FAQForm(request.POST, instance=faq)

        if form.is_valid():
            form.save()
            return redirect("faq_list")
    else:
        form = FAQForm(instance=faq)

    context = {
        "form": form,
        "faq": faq,
        "page_title": "Edit FAQ",
        "button_text": "Save FAQ Changes",
    }

    return render(request, "support/faq_form.html", context)


@login_required
def faq_delete_view(request, faq_id):
    faq = get_object_or_404(FAQ, id=faq_id)

    if request.method == "POST":
        faq.delete()
        return redirect("faq_list")

    context = {
        "faq": faq,
    }

    return render(request, "support/faq_confirm_delete.html", context)


@login_required
def export_leads_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="northstar_leads.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Name",
        "Email",
        "Phone",
        "Product Interest",
        "Original Question",
        "Source",
        "Status",
        "Notes",
        "Created At",
        "Updated At",
    ])

    leads = Lead.objects.all()

    for lead in leads:
        writer.writerow([
            lead.name,
            lead.email,
            lead.phone,
            lead.product_interest,
            lead.original_question,
            lead.source,
            lead.status,
            lead.notes,
            lead.created_at,
            lead.updated_at,
        ])

    return response


@login_required
def export_chats_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="northstar_chat_history.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Customer Question",
        "Bot Answer",
        "Was Answered",
        "Matched FAQ",
        "Customer Name",
        "Customer Email",
        "Created At",
    ])

    chats = ChatMessage.objects.all()

    for chat in chats:
        matched_faq_question = ""

        if chat.matched_faq:
            matched_faq_question = chat.matched_faq.question

        writer.writerow([
            chat.customer_question,
            chat.bot_answer,
            "Yes" if chat.was_answered else "No",
            matched_faq_question,
            chat.customer_name,
            chat.customer_email,
            chat.created_at,
        ])

    return response


@login_required
def export_unanswered_csv(request):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="northstar_unanswered_questions.csv"'

    writer = csv.writer(response)
    writer.writerow([
        "Question",
        "Customer Email",
        "Status",
        "Notes",
        "Created At",
        "Resolved At",
        "Created FAQ",
    ])

    unanswered_questions = UnansweredQuestion.objects.all()

    for item in unanswered_questions:
        created_faq_question = ""

        if item.created_faq:
            created_faq_question = item.created_faq.question

        writer.writerow([
            item.question,
            item.customer_email,
            item.status,
            item.notes,
            item.created_at,
            item.resolved_at,
            created_faq_question,
        ])

    return response