# customer_portal/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from .models import ServiceRequest, CustomerProfile, Attachment, ServiceRequestComment
from .forms import (
    ServiceRequestForm, CustomerProfileForm, ServiceRequestCommentForm,
    ServiceRequestUpdateForm, AttachmentForm
)

class StaffDashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'customer_portal/staff_dashboard.html'

    model = ServiceRequest
    context_object_name = 'service_requests'
    paginate_by = 10

    def get_queryset(self):
        # Customize the queryset to show all service requests or those relevant to staff
        return ServiceRequest.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add any additional context required for staff
        return context

class CustomerDashboardView(LoginRequiredMixin, ListView):
    model = ServiceRequest
    template_name = 'customer_portal/dashboard.html'
    context_object_name = 'service_requests'
    paginate_by = 10

    def get_queryset(self):
        return ServiceRequest.objects.filter(
            customer__user=self.request.user
        ).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            context['profile'] = CustomerProfile.objects.get(user=self.request.user)
        except CustomerProfile.DoesNotExist:
            # Create the profile if it doesn't exist
            profile = CustomerProfile.objects.create(user=self.request.user)
            context['profile'] = profile
            messages.info(self.request, "Your profile has been created.")
        return context

@login_required
def service_request_create(request):
    if request.method == 'POST':
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.customer = request.user.customerprofile
            service_request.save()

            # Handle file upload
            if request.FILES.get('attachments'):
                Attachment.objects.create(
                    service_request=service_request,
                    file=request.FILES['attachments']
                )

            messages.success(request, 'Service request created successfully!')
            return redirect('service-request-detail', pk=service_request.pk)
    else:
        form = ServiceRequestForm()

    return render(request, 'customer_portal/service_request_form.html', {'form': form})

class ServiceRequestDetailView(LoginRequiredMixin, DetailView):
    model = ServiceRequest
    template_name = 'customer_portal/service_request_detail.html'
    context_object_name = 'service_request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = ServiceRequestCommentForm()
        context['comments'] = self.object.servicerequestcomment_set.all().order_by('-created_at')
        context['attachment_form'] = AttachmentForm()
        return context

@login_required
def add_attachment(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        form = AttachmentForm(request.POST, request.FILES)
        if form.is_valid():
            attachment = form.save(commit=False)
            attachment.service_request = service_request
            attachment.save()
            messages.success(request, 'File uploaded successfully!')
    return redirect('service-request-detail', pk=pk)

# ... rest of the views remain the same ...

@login_required
def profile_view(request):
    try:
        # Fetch the user's profile, or create a new one if it doesn't exist
        profile = CustomerProfile.objects.get(user=request.user)
    except CustomerProfile.DoesNotExist:
        profile = CustomerProfile(user=request.user)

    if request.method == 'POST':
        form = CustomerProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')  # Redirect back to the profile page
    else:
        form = CustomerProfileForm(instance=profile)

    return render(request, 'customer_portal/profile.html', {'form': form})

def add_comment(request, pk):
    service_request = get_object_or_404(ServiceRequest, pk=pk)
    if request.method == 'POST':
        form = ServiceRequestCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.service_request = service_request
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
        else:
            messages.error(request, 'There was an error adding your comment.')
    return redirect('service-request-detail', pk=pk)
