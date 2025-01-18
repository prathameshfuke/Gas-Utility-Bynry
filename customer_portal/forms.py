# customer_portal/forms.py
from django import forms
from .models import ServiceRequest, CustomerProfile, ServiceRequestComment, Attachment
class CustomerProfileForm(forms.ModelForm):
    class Meta:
        model = CustomerProfile
        fields = ['first_name', 'last_name', 'phone_number', 'address']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'service_address': forms.Textarea(attrs={'rows': 3}),
        }

class ServiceRequestForm(forms.ModelForm):
    attachments = forms.FileField(
        required=False,
        widget=forms.FileInput(attrs={'accept': 'image/*,.pdf'}),
        help_text='Select a file to upload'
    )

    class Meta:
        model = ServiceRequest
        fields = ['service_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': 'Please provide detailed information about your request...'
            })
        }

class ServiceRequestCommentForm(forms.ModelForm):
    class Meta:
        model = ServiceRequestComment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }

class ServiceRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ['status', 'priority', 'assigned_to']

class AttachmentForm(forms.ModelForm):
    class Meta:
        model = Attachment
        fields = ['file', 'description']
