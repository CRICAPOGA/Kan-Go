from django.shortcuts import render

def acceso(request):
    return render(request, 'acceso.html')