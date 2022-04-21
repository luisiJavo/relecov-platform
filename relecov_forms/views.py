import re
from django.shortcuts import render

# Create your views here.
def relecov_form(request):
    return render(request,"relecov_forms/relecov_form.html",{})