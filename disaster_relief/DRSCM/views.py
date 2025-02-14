from django.shortcuts import render
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect
from django.core.exceptions import ValidationError
# Create your views here.
def error404(request):
    return render(request,'pagenotfound.html')

def about(request):
    return render(request,'about.html')

def report(request):
    return render(request,'report.html')
def login(request):
    return render(request,'login.html')

def our_services(request):
    return render(request,'our_services.html')

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

def contact_us(request):
    return render(request,'contact_us.html')


from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Disaster

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

            # If the user is an admin, allow them to modify the status
            if request.user.is_staff or request.user.is_superuser:
                status = request.POST.get('status', 'active')

            # Validate required fields
            if not all([name, location, severity, description, reported_at]):
                raise ValidationError("All fields are required.")

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

            # Redirect to a success page or home page
            return redirect('index')  # Replace 'index' with the name of your home URL

        except ValidationError as e:
            # Handle validation errors
            return render(request, 'report.html', {'error': str(e)})

        except Exception as e:
            # Handle other exceptions
            return render(request, 'report.html', {'error': 'An error occurred. Please try again.'})

    else:
        # Render the form for GET requests
        return render(request, 'report.html')