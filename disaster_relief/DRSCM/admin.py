from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(ReliefCenter)
admin.site.register(Disaster)
admin.site.register(SupplyRequest)
admin.site.register(Logistics)
admin.site.register(Notification)