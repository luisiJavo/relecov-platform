from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def dashboard(request):
    #return HttpResponse("Here's the dashboard.")
    context ={}
    return render(request, 'dashboard/index.html', context)