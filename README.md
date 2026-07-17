# Northstar Home Co. AI Support Dashboard

A client-ready practice project for a small ecommerce business that needs a customer-facing support chatbot and an owner/admin dashboard for support visibility.

This project was built for a mock ecommerce client, Northstar Home Co., a home organization and lifestyle product store. The system helps the business answer common customer questions, capture leads, track unanswered questions, manage FAQ content, and export support data.

---

## Project Purpose

Northstar Home Co. receives repeated customer questions about shipping, returns, orders, products, discounts, damaged items, and support policies.

The goal of this project is to provide:

- A customer-facing chatbot page
- A protected admin dashboard
- Chat history tracking
- Lead capture and lead management
- Unanswered question tracking
- FAQ / knowledge-base management
- Basic analytics
- CSV export
- Manual and automated testing
- Client-style documentation and handover notes

This is a mock client-ready portfolio project. It uses mock/local data and is not connected to a real ecommerce store.

---

## Tech Stack

- Python
- Django
- SQLite
- Django templates
- HTML
- CSS
- Django authentication
- Django automated tests
- CSV export using Django views

---

## Main Features

### Customer Chatbot

Customers can:

- Open the chatbot page
- Ask support questions
- Receive FAQ-based answers
- See a fallback message when the bot cannot answer
- Submit follow-up contact details if needed

The chatbot uses active FAQ records from the database. It does not use hardcoded answers inside the template.

---

### Admin Login

Admin dashboard pages are protected.

Logged-out users are redirected to the login page before they can access:

- Dashboard
- Chat history
- Leads
- Unanswered questions
- FAQ management pages
- CSV export URLs

---

### Admin Dashboard

The dashboard shows:

- Total chats
- Answered chats
- Unanswered chats
- Total leads
- New leads
- Active FAQs
- Answer rate
- Fallback rate
- Recent chats
- Recent leads
- Recent unanswered questions

---

### Chat History

The admin can review:

- Customer question
- Bot answer
- Answered/unanswered status
- Matched FAQ
- Customer name/email if provided
- Timestamp

---

### Lead Management

The admin can review captured leads with:

- Name
- Email
- Phone
- Product interest
- Original question
- Source
- Status
- Notes
- Created date

The admin can update:

- Lead status
- Lead notes

Supported lead statuses:

- New
- Contacted
- Qualified
- Not Interested
- Closed

---

### Unanswered Question Management

When the chatbot cannot answer a question, the question is saved as unanswered.

The admin can review:

- Question
- Customer email if provided
- Status
- Notes
- Created date
- Created FAQ reference if applicable

The admin can update:

- Status
- Notes

Supported unanswered question statuses:

- New
- Reviewed
- Added to FAQ
- Ignored

---

### FAQ / Knowledge Base Management

The admin can manage chatbot knowledge without editing code.

The admin can:

- Add FAQ records
- Edit FAQ records
- Delete FAQ records
- Activate/deactivate FAQs
- Add keywords for matching

FAQ fields:

- Question
- Answer
- Category
- Keywords
- Active/inactive status
- Created date
- Updated date

The chatbot only uses active FAQs.

---

### CSV Export

The admin can export:

- Leads
- Chat history
- Unanswered questions

CSV files include clear column names and can be opened in Excel or Google Sheets.

---

## Project Structure

```text
northstar_support_dashboard/
│
├── manage.py
├── requirements.txt
├── .gitignore
│
├── northstar_support_dashboard/
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── support/
│   ├── admin.py
│   ├── apps.py
│   ├── forms.py
│   ├── models.py
│   ├── tests.py
│   ├── urls.py
│   ├── views.py
│   └── management/
│       └── commands/
│           ├── load_sample_faqs.py
│           ├── load_sample_leads.py
│           ├── load_sample_chats.py
│           └── load_sample_unanswered.py
│
├── templates/
│   ├── registration/
│   │   └── login.html
│   └── support/
│       ├── chat.html
│       ├── dashboard.html
│       ├── chat_history.html
│       ├── leads.html
│       ├── lead_update.html
│       ├── unanswered.html
│       ├── unanswered_update.html
│       ├── faq_list.html
│       ├── faq_form.html
│       └── faq_confirm_delete.html
│
└── static/
    └── support/
        └── style.css