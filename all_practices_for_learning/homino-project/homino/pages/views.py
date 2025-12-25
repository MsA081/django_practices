# FBV -> Function Base Views
# from django.shortcuts import render
# from django.http import HttpResponse

# # Create your views here.


# def home(request):
#     return render(request, "home.html")


# def about(request):
#     return render(request, "about.html")


# def contact(request):
#     return render(request, "contact.html")

# CBV -> Class Based Views
from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = "home.html"
    

class AboutView(TemplateView):
    template_name = "about.html"
    


class ContactView(TemplateView):
    template_name = "contact.html"
    
