# customer_portal/admin.py
from django.contrib import admin
from .models import CustomerProfile, ServiceRequest, Attachment, ServiceRequestComment

@admin.register(CustomerProfile)
class CustomerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'first_name', 'last_name', 'phone_number']  # Updated to match model fields
    list_filter = ['user__date_joined']  # Use related field if filtering by date
    search_fields = ['user__username', 'first_name', 'last_name', 'phone_number']

@admin.register(ServiceRequest)
class ServiceRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'service_type', 'status', 'priority', 'created_at', 'assigned_to')
    list_filter = ('status', 'service_type', 'priority', 'created_at')
    search_fields = ('customer__account_number', 'customer__user__email', 'description')
    raw_id_fields = ('customer', 'assigned_to')
    date_hierarchy = 'created_at'
    list_editable = ('status', 'priority', 'assigned_to')

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('customer', 'customer__user', 'assigned_to')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'file', 'uploaded_at', 'description')
    search_fields = ('service_request__id', 'description')
    date_hierarchy = 'uploaded_at'

@admin.register(ServiceRequestComment)
class ServiceRequestCommentAdmin(admin.ModelAdmin):
    list_display = ('service_request', 'author', 'created_at', 'is_internal')
    list_filter = ('is_internal', 'created_at')
    search_fields = ('service_request__id', 'author__email', 'content')
    raw_id_fields = ('service_request', 'author')
    date_hierarchy = 'created_at'
