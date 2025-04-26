from django.shortcuts import render

# Create your views here.
def home(request):
    return render(request, 'home.html')

def reportes(request):
    return render(request, 'reportes.html')
