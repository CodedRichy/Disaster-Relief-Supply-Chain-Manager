from django.shortcuts import render

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