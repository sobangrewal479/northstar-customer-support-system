from django.urls import path
from . import views

urlpatterns = [
    path("chat/", views.chat_view, name="chat"),
    path("dashboard/", views.dashboard_view, name="dashboard"),

    path("dashboard/chats/", views.chat_history_view, name="chat_history"),
    path("dashboard/chats/export/", views.export_chats_csv, name="export_chats_csv"),

    path("dashboard/leads/", views.leads_view, name="leads"),
    path("dashboard/leads/export/", views.export_leads_csv, name="export_leads_csv"),
    path("dashboard/leads/<int:lead_id>/update/", views.lead_update_view, name="lead_update"),

    path("dashboard/unanswered/", views.unanswered_questions_view, name="unanswered_questions"),
    path("dashboard/unanswered/export/", views.export_unanswered_csv, name="export_unanswered_csv"),
    path(
        "dashboard/unanswered/<int:unanswered_id>/update/",
        views.unanswered_update_view,
        name="unanswered_update",
    ),

    path("dashboard/faqs/", views.faq_list_view, name="faq_list"),
    path("dashboard/faqs/add/", views.faq_create_view, name="faq_create"),
    path("dashboard/faqs/<int:faq_id>/edit/", views.faq_update_view, name="faq_update"),
    path("dashboard/faqs/<int:faq_id>/delete/", views.faq_delete_view, name="faq_delete"),
]