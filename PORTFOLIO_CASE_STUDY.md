# Portfolio Case Study — Northstar Home Co. AI Support Dashboard

## Project Name

Northstar Home Co. AI Support Dashboard

---

## Project Type

Client-ready practice project for a small ecommerce business.

---

## Client Background

Northstar Home Co. is a mock ecommerce brand that sells home organization and lifestyle products such as storage baskets, pantry containers, wall shelves, and laundry room storage products.

The business receives repeated customer questions about:

- Shipping
- Returns
- Order changes
- Product information
- Discounts
- Damaged items
- Customer support

---

## Problem

The business needed a better way to handle common customer support questions and track support activity.

Without a system like this, the business owner would have difficulty knowing:

- What customers are asking
- Which questions are answered automatically
- Which questions the chatbot cannot answer
- Which customers need follow-up
- Which FAQs need to be improved
- Which leads came from chatbot conversations

---

## Solution

I built a Django-based AI Support Dashboard with a customer-facing chatbot and a protected admin dashboard.

The chatbot answers customer questions using an admin-managed FAQ knowledge base. If the chatbot cannot answer a question, it saves the question as unanswered and allows the customer to submit follow-up details.

The admin dashboard gives the business owner visibility into chats, leads, unanswered questions, FAQs, and support analytics.

---

## Main Features

### Customer Chatbot

- Customer can ask a support question
- Bot answers using active FAQ records
- Bot shows fallback when no answer is found
- Customer can submit follow-up details after the bot response

### Admin Dashboard

- Login-protected dashboard
- Total chats
- Answered chats
- Unanswered chats
- Total leads
- New leads
- Active FAQs
- Answer rate
- Fallback rate

### Lead Management

- Captures customer name, email, phone, product interest, and original question
- Admin can update lead status
- Admin can add lead notes

### Unanswered Question Tracking

- Saves questions the chatbot cannot answer
- Admin can review and update unanswered question status
- Helps the business improve FAQ coverage over time

### FAQ Management

- Admin can add FAQs
- Admin can edit FAQs
- Admin can delete FAQs
- Admin can activate or deactivate FAQs
- Chatbot uses active FAQs only

### CSV Export

- Export leads
- Export chat history
- Export unanswered questions

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
- CSV export

---

## How It Works

1. Customer opens the chatbot page.
2. Customer asks a question.
3. The chatbot checks active FAQ records.
4. If a match is found, the chatbot returns the FAQ answer.
5. If no match is found, the chatbot shows a fallback response.
6. The unanswered question is saved.
7. Customer can submit follow-up details.
8. Admin can review chats, leads, unanswered questions, and FAQs from the dashboard.

---

## Admin Workflow

The business owner can:

1. Log in to the dashboard.
2. Review recent support activity.
3. Check unanswered questions.
4. Follow up with captured leads.
5. Add new FAQs based on unanswered questions.
6. Update or deactivate outdated FAQs.
7. Export support data as CSV.

---

## Testing Completed

Manual testing was completed for:

- Admin login
- Admin logout
- Protected dashboard access
- Known FAQ response
- Unknown question fallback
- Lead capture
- Chat history
- Lead update
- Unanswered question update
- FAQ add/edit/delete
- FAQ active/inactive behavior
- CSV exports
- UI styling

Automated Django tests were also added.

Test command:

```bash
python manage.py test