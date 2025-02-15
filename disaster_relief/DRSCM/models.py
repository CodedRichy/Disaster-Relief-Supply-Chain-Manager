from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from .models import *

# Create your models here.
class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Relief Center Staff'),
        ('volunteer', 'Volunteer'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Link to Django's built-in User model
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='volunteer')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

class Disaster(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    severity = models.IntegerField()  # Scale from 1-10
    description = models.CharField(max_length=1000)
    reported_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('active', 'Active'),
        ('resolved', 'Resolved')
    ], default='active')

    def __str__(self):
        return f"{self.name} - {self.location}"


class ReliefCenter(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=255)
    capacity = models.IntegerField()  # Maximum people it can support
    available_resources = models.TextField()  # List of available supplies

    def __str__(self):
        return self.name


class SupplyRequest(models.Model):
    disaster = models.ForeignKey(Disaster, on_delete=models.CASCADE)
    relief_center = models.ForeignKey(ReliefCenter, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=200)
    quantity_needed = models.IntegerField()
    status = models.CharField(max_length=50, choices=[
        ('pending', 'Pending'),
        ('fulfilled', 'Fulfilled'),
        ('in_progress', 'In Progress')
    ], default='pending')

    requested_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.item_name} - {self.relief_center.name} ({self.status})"


from django.db import models
from django.utils import timezone

class Logistics(models.Model):
    driver_name = models.CharField(max_length=200)
    vehicle_number = models.CharField(max_length=50)
    departure_time = models.DateTimeField(default=timezone.now)
    estimated_arrival = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=50,
        choices=[
            ('en_route', 'En Route'),
            ('delivered', 'Delivered'),
            ('delayed', 'Delayed')
        ],
        default='en_route'
    )
    start_lat = models.FloatField()  # Starting latitude
    start_lng = models.FloatField()  # Starting longitude
    end_lat = models.FloatField()    # Ending latitude
    end_lng = models.FloatField()    # Ending longitude

    def save(self, *args, **kwargs):
        """Ensure estimated_arrival is timezone-aware before saving."""
        if self.estimated_arrival and timezone.is_naive(self.estimated_arrival):
            self.estimated_arrival = timezone.make_aware(self.estimated_arrival)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Logistics for {self.vehicle_number} by {self.driver_name}"



class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField()
    notification_type = models.CharField(max_length=20, choices=[
        ('disaster', 'Disaster Alert'),
        ('supply', 'Supply Request'),
        ('logistics', 'Logistics Update'),
    ])
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.notification_type} - {self.status}"
