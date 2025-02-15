from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.core.exceptions import ValidationError
from datetime import datetime
# Create your views here.
def error404(request):
    return render(request, 'map.html')

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
            disaster = Disaster.objects.create(
                name=name,
                location=location,
                severity=severity,
                description=description,
                status=status,
                reported_at=reported_at
            )
            disaster.save()

            # Create a notification for the new disaster
            Notification.objects.create(
                user=request.user,  # Assuming the user is logged in
                message=f"New Disaster '{name}' reported at {location} with severity {severity}.",
                notification_type='disaster'
            )

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

            # Create a notification
            Notification.objects.create(
            message=f"New Relief Center '{name}' has been added at {location}."
            )

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

def create_logistics(request):
    if request.method == 'POST':
        try:
            # Fetch data from the form
            vehicle_number = request.POST.get('vehicle_number')
            driver_name = request.POST.get('driver_name')
            departure_time_str = request.POST.get('departure_time')
            estimated_arrival_str = request.POST.get('estimated_arrival')
            status = request.POST.get('status', 'en_route')
            start_lat = request.POST.get('start_lat')
            start_lng = request.POST.get('start_lng')
            end_lat = request.POST.get('end_lat')
            end_lng = request.POST.get('end_lng')

            # Validate required fields
            if not all([vehicle_number, driver_name, departure_time_str, estimated_arrival_str, start_lat, start_lng, end_lat, end_lng]):
                raise ValidationError("All fields are required.")

            # Convert datetime strings to timezone-aware datetime objects
            departure_time = timezone.make_aware(datetime.fromisoformat(departure_time_str))
            estimated_arrival = timezone.make_aware(datetime.fromisoformat(estimated_arrival_str))

            # Convert latitude and longitude to float
            start_lat = float(start_lat)
            start_lng = float(start_lng)
            end_lat = float(end_lat)
            end_lng = float(end_lng)

            # Create and save the Logistics object
            logistics = Logistics.objects.create(
                vehicle_number=vehicle_number,
                driver_name=driver_name,
                departure_time=departure_time,
                estimated_arrival=estimated_arrival,
                status=status,
                start_lat=start_lat,
                start_lng=start_lng,
                end_lat=end_lat,
                end_lng=end_lng
            )

            # Create a notification for the new logistics entry
            Notification.objects.create(
                user=request.user,  # Assuming the user is logged in
                message=f"New Logistics entry for vehicle '{vehicle_number}' has been created.",
                notification_type='logistics'
            )

            # Redirect to a success page or home page
            return redirect('index')

        except ValidationError as e:
            # Handle validation errors
            return render(request, 'logistics.html', {'error': str(e)})

        except Exception as e:
            # Handle other exceptions
            return render(request, 'logistics.html', {'error': 'An error occurred. Please try again.'})

    else:
        # Render the form for GET requests
        return render(request, 'logistics.html')

def notifications(request):
    # Fetch all notifications for the logged-in user
    notifications = Notification.objects.filter(user=request.user, is_read=False).order_by('-timestamp')
    return render(request, 'notifications.html', {'notifications': notifications})

from django.http import JsonResponse

def mark_notification_as_read(request, notification_id):
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        return JsonResponse({'status': 'success'})
    except Notification.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Notification not found'}, status=404)

