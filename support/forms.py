from django import forms
from .models import FAQ, Lead, UnansweredQuestion


class ChatbotForm(forms.Form):
    question = forms.CharField(
        label="Your question",
        widget=forms.Textarea(
            attrs={
                "rows": 3,
                "placeholder": "Ask about shipping, returns, products, discounts, or order issues...",
            }
        ),
        required=True,
    )


class LeadCaptureForm(forms.Form):
    original_question = forms.CharField(
        widget=forms.HiddenInput(),
        required=True,
    )

    name = forms.CharField(
        label="Name",
        max_length=100,
        required=True,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Your name",
            }
        ),
    )

    email = forms.EmailField(
        label="Email",
        required=True,
        widget=forms.EmailInput(
            attrs={
                "placeholder": "your@email.com",
            }
        ),
    )

    phone = forms.CharField(
        label="Phone",
        max_length=30,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Optional phone number",
            }
        ),
    )

    product_interest = forms.CharField(
        label="Product interest",
        max_length=150,
        required=False,
        widget=forms.TextInput(
            attrs={
                "placeholder": "Example: pantry containers, wall shelves, baskets",
            }
        ),
    )


class LeadUpdateForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = ["status", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 5}),
        }


class UnansweredQuestionUpdateForm(forms.ModelForm):
    class Meta:
        model = UnansweredQuestion
        fields = ["status", "notes"]
        widgets = {
            "notes": forms.Textarea(attrs={"rows": 5}),
        }


class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ["question", "answer", "category", "keywords", "is_active"]
        widgets = {
            "question": forms.TextInput(
                attrs={
                    "placeholder": "Example: Do you offer free shipping?",
                }
            ),
            "answer": forms.Textarea(
                attrs={
                    "rows": 5,
                    "placeholder": "Write the answer customers should receive.",
                }
            ),
            "keywords": forms.Textarea(
                attrs={
                    "rows": 3,
                    "placeholder": "Example: free shipping, shipping cost, delivery fee",
                }
            ),
        }