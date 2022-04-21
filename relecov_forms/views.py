import re
from django.shortcuts import render

# Create your views here.
def relecov_form(request):
    csv_file = "relecov_core/docs/jspreadsheet.csv"
    return render(request,"relecov_forms/relecov_form.html",{"csv_file":csv_file})