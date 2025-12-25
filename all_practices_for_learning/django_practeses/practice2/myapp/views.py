from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def hello(request):
    return HttpResponse("Hello World")

# def home(request):
#     return render(request, "home.html")

# def about(request):
#     return render(request, "about.html")

from django.views.generic import TemplateView

class HomeView(TemplateView):
    template_name = 'home.html'
    
class AboutView(TemplateView):
    template_name = 'about.html'

def contact(request):
    return render(request, "contact.html")

def product(request):
    return render(request, "product.html")

def user(request):
    return render(request, "user.html")

def user_details(request, user_id):
    return render(request, "user_details.html", {"user_id": user_id})