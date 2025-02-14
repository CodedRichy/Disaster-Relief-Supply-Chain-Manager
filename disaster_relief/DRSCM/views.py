from django.shortcuts import render
from .models import *

from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
from datetime import datetime
# Create your views here.
def error404(request):
    return render(request,'pagenotfound.html')

def about(request):
    return render(request,'about.html')

def report(request):
    return render(request,'report.html')

def index(request):
    return render(request,'index.html')

def admin_dashboard(request):
    return render(request,'admin_dashboard.html')

def relief_centers(request):
    return render(request,'relief_centers.html')

def notifications(request):
    return render(request,'notifications.html')

def logistics(request):
    return render(request,'logistics.html')

def add_disaster_details(request):
    if request.method == 'POST':
        try:
            # Fetch data from the form
            name = request.POST.get('name')
            location = request.POST.get('location')
            severity = request.POST.get('severity')
            description = request.POST.get('description')
            reported_at = request.POST.get('reported_at')

            # Set default status to 'active'
            status = 'active'
            if request.user.is_staff or request.user.is_superuser:
                status = request.POST.get('status', 'active')

            # Validate required fields
            if not all([name, location, severity, description, reported_at]):
                raise ValidationError("All fields are required.")

            # Convert reported_at to datetime format
            try:
                reported_at = datetime.strptime(reported_at, '%Y-%m-%dT%H:%M')
            except ValueError:
                return render(request, 'report.html', {'error': 'Invalid date format. Please select a valid date & time.'})

            # Debugging: Print received data in terminal
            print(f"Saving Disaster Report: {name}, {location}, {severity}, {description}, {reported_at}, {status}")

            # Create and save the Disaster object
            data = Disaster.objects.create(
                name=name,
                location=location,
                severity=severity,
                description=description,
                status=status,
                reported_at=reported_at
            )
            data.save()

            # Redirect to home page after successful submission
            return redirect('index')  # Make sure 'index' exists in urls.py

        except ValidationError as e:
            # Handle validation errors
            return render(request, 'report.html', {'error': str(e)})

        except Exception as e:
            # Handle other exceptions
            print(f"Error: {e}")  # Print the error in console for debugging
            return render(request, 'report.html', {'error': 'An error occurred. Please try again.'})

    else:
        # Render the form for GET requests
        return render(request, 'report.html')