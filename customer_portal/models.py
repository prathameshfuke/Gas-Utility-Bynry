from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class CustomerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    account_number = models.CharField(max_length=50, unique=True, blank=True)  # Optional field
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set when created

    # Add a 'service_type' field with choices
    SERVICE_TYPE_CHOICES = [
        ('basic', 'Basic'),
        ('premium', 'Premium'),
        ('luxury', 'Luxury'),
    ]
    service_type = models.CharField(
        max_length=10,
        choices=SERVICE_TYPE_CHOICES,
        default='basic',
    )

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.user.username}"


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
        ('CLOSED', 'Closed'),
    ]

    SERVICE_TYPES = [
        ('GAS_LEAK', 'Gas Leak'),
        ('CONNECTION', 'New Connection'),
        ('DISCONNECTION', 'Disconnection'),
        ('BILLING', 'Billing Issue'),
        ('MAINTENANCE', 'Maintenance'),
        ('OTHER', 'Other'),
    ]

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    priority = models.IntegerField(default=3)  # 1 (highest) to 5 (lowest)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    assigned_to = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_requests'
    )

    def __str__(self):
        return f"{self.get_service_type_display()} - {self.customer.account_number}"

    def resolve(self):
        self.status = 'RESOLVED'
        self.resolved_at = timezone.now()
        self.save()

class Attachment(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='attachments')
    file = models.FileField(upload_to='service_requests/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Attachment for {self.service_request} - {self.description or 'No description'}"

class ServiceRequestComment(models.Model):
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_internal = models.BooleanField(default=False)  # For staff-only comments

    def __str__(self):
        return f"Comment on {self.service_request} by {self.author.get_full_name()}"
