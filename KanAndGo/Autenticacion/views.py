from django.shortcuts import render

# Create your views here.
def access(request):
    return render(request, 'login_register.html')