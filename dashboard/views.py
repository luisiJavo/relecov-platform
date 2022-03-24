from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def index(request):
    context = {}
    return render(request, 'dashboard/index.html', context)

def link_to_dashboard(request):
    context = {}
    return render(request, 'dashboard/dashboard.html', context)
    
    