from django.shortcuts import render
from .models import Proyecto

######################### CRUD PROYECTOS #########################
def proyectos(request):
    proyectos = Proyecto.objects.filter(usuario_id=request.user)
    return render(request, 'proyectos.html', {'proyectos': proyectos})

