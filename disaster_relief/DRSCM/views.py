from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError

# Create your views here.
def error404(request):
    return render(request, 'pagenotfound.html')

def about(request):
    return render(request, 'about.html')

def report(request):
    return render(request, 'report.html')

def login_view(request):  # Renamed to avoid conflict with Django's login function
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'login.html')

def index(request):
    return render(request, 'index.html')

def admin_dashboard(request):
    return render(request, 'admin_dashboard.html')

def relief_centers(request):
    # Fetch all relief centers from the database
    relief_centers = ReliefCenter.objects.all()

    # Pass the relief centers to the template
    return render(request, 'relief_centers.html', {'relief_centers': relief_centers})

def notifications(request):
    return render(request, 'notifications.html')

def logistics(request):
    return render(request, 'logistics.html')

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
            return redirect('index.html')  # Replace 'index' with the name of your home URL

        except ValidationError as e:
            # Handle validation errors
            return render(request, 'report.html', {'error': str(e)})

        except Exception as e:
            # Handle other exceptions
            return render(request, 'report.html', {'error': 'An error occurred. Please try again.'})

    else:
        # Render the form for GET requests
        return render(request, 'report.html')

# New Functions

def register_user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Default user type is 'volunteer'
        user_type = 'volunteer'

        # If the user is an admin, allow them to set the user type
        if request.user.is_staff or request.user.is_superuser:
            user_type = request.POST.get('user_type', 'volunteer')  # Default to 'volunteer' if not provided

        # Validate required fields
        if not all([username, password]):
            return render(request, 'register.html', {'error': 'Username and password are required.'})

        try:
            # Create the user
            user = User.objects.create_user(username=username, password=password)
            user.save()

            # Assign user type (default is 'volunteer')
            user_profile = UserProfile.objects.create(user=user, user_type=user_type)
            user_profile.save()

            # Log the user in (optional, depending on your flow)
            login(request, user)

            # Redirect to a success page or home page
            return redirect('index')  # Replace 'index' with the name of your home URL

        except Exception as e:
            # Handle other exceptions
            return render(request, 'register.html', {'error': 'An error occurred. Please try again.'})

    else:
        # Render the form for GET requests
        return render(request, 'register.html')

def add_relief_center(request):
    if request.method == 'POST':
        try:
            # Fetch data from the form
            name = request.POST.get('name')
            location = request.POST.get('location')
            capacity = request.POST.get('capacity')
            available_resources = request.POST.get('available_resources')

            # Validate required fields
            if not all([name, location, capacity, available_resources]):
                raise ValidationError("All fields are required.")

            # Create and save the ReliefCenter object
            relief_center = ReliefCenter.objects.create(
                name=name,
                location=location,
                capacity=capacity,
                available_resources=available_resources
            )
            relief_center.save()

            # Redirect to a success page or home page
            return redirect('index')  # Replace 'index' with the name of your home URL

        except ValidationError as e:
            # Handle validation errors
            return render(request, 'add_relief_center.html', {'error': str(e)})

        except Exception as e:
            # Handle other exceptions
            return render(request, 'add_relief_center.html', {'error': 'An error occurred. Please try again.'})

    else:
        # Render the form for GET requests
        return render(request, 'add_relief_center.html')

def create_supply_request(request):
    if request.method == 'POST':
        try:
            # Fetch data from the form
            disaster = request.POST.get('disaster')
            relief_center = request.POST.get('relief_center')
            item_name = request.POST.get('item_name')
            quantity_needed = request.POST.get('quantity_needed')
            status = request.POST.get('status', 'pending')  # Default status is 'pending'

            # Validate required fields
            if not all([disaster, relief_center, item_name, quantity_needed]):
                raise ValidationError("All fields are required.")

            # Create and save the SupplyRequest object
            supply_request = SupplyRequest.objects.create(
                disaster=disaster,
                relief_center=relief_center,
                item_name=item_name,
                quantity_needed=quantity_needed,
                status=status
            )
            supply_request.save()

            # Redirect to a success page or home page
            return redirect('index')  # Replace 'index' with the name of your home URL

        except ValidationError as e:
            # Handle validation errors
            return render(request, 'create_supply_request.html', {'error': str(e)})

        except Exception as e:
            # Handle other exceptions
            return render(request, 'create_supply_request.html', {'error': 'An error occurred. Please try again.'})

    else:
        # Render the form for GET requests
        return render(request, 'create_supply_request.html')