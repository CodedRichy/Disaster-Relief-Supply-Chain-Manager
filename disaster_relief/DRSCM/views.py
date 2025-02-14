from django.shortcuts import render

# Create your views here.
def error404(request):
    return render(request,'index.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')

def (request):
    return render(request,'index.html')