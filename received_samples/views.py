from django.shortcuts import render

# Create your views here.
def received_samples(request):
    context = {}
    return render(request, 'received_samples/received_samples.html', context)