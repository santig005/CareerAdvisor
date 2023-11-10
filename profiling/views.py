from django.shortcuts import render
from . import views

# Create your views here.
def profiling_form(request):
    return render(request,'profiling_form.html')

def results(request):
    estudios = request.POST.get("estudios", "")
    pregrado = request.POST.get("pregrado", "")
    cursos = request.POST.get("cursos", "")

    print("Estudios:", estudios)
    print("Pregrado:", pregrado)
    print("Cursos:", cursos)
    print(type(cursos))

    # ... tu lógica adicional aquí ...

    return render(request, "results.html")