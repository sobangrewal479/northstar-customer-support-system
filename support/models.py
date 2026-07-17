from django.db import models


class FAQ(models.Model):
    CATEGORY_CHOICES = [
        ("Shipping", "Shipping"),
        ("Returns", "Returns"),
        ("Orders", "Orders"),
        ("Product Info", "Product Info"),
        ("Discounts", "Discounts"),
        ("Damaged Items", "Damaged Items"),
        ("Store Policy", "Store Policy"),
        ("Contact", "Contact"),
    ]

    question = models.CharField(max_length=255)
    answer = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    keywords = models.TextField(
        help_text="Add comma-separated keywords. Example: shipping, delivery, arrive"
    )
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["category", "question"]

    def __str__(self):
        return self.question


class ChatMessage(models.Model):
    customer_question = models.TextField()
    bot_answer = models.TextField()
    was_answered = models.BooleanField(default=False)
    matched_faq = models.ForeignKey(
        FAQ,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="matched_chats",
    )
    customer_name = models.CharField(max_length=100, blank=True)
    customer_email = models.EmailField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.customer_question[:80]


class Lead(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Contacted", "Contacted"),
        ("Qualified", "Qualified"),
        ("Not Interested", "Not Interested"),
        ("Closed", "Closed"),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    product_interest = models.CharField(max_length=150, blank=True)
    original_question = models.TextField(blank=True)
    source = models.CharField(max_length=50, default="Chatbot")
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="New")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"


class UnansweredQuestion(models.Model):
    STATUS_CHOICES = [
        ("New", "New"),
        ("Reviewed", "Reviewed"),
        ("Added to FAQ", "Added to FAQ"),
        ("Ignored", "Ignored"),
    ]

    question = models.TextField()
    customer_email = models.EmailField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="New")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    created_faq = models.ForeignKey(
        FAQ,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="created_from_unanswered",
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.question[:80]