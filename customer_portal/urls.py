# customer_portal/urls.py
from django.urls import path
from . import views  # This imports everything from views.py

from .views import CustomerDashboardView  # Import the view here

urlpatterns = [
    path('dashboard/', CustomerDashboardView.as_view(), name='customer_dashboard'),
    path('service-requests/<int:pk>/add-comment/', views.add_comment, name='add-comment'),
    path('', CustomerDashboardView.as_view(), name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('service-request/new/',
         views.service_request_create,
         name='service-request-create'),
    path('service-request/<int:pk>/',
         views.ServiceRequestDetailView.as_view(),
         name='service-request-detail'),
    path('service-request/<int:pk>/comment/',
         views.add_comment,
         name='add-comment'),
    path('service-request/<int:pk>/attachment/',
         views.add_attachment,
         name='add-attachment'),
    path('staff-dashboard/', views.StaffDashboardView.as_view(), name='staff-dashboard'),

]
