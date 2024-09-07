from django.shortcuts import render
from .models import Student
from django.contrib import messages
from django.db.models import Q


# Create your views here.
def index(request):
    students = Student.objects.all()
    
    print(type(request.POST))

    if request.method == "POST":
        if "ajouter" in request.POST:
            nomEtudiant = request.POST.get("nomEtudiant")
            emailEtudiant = request.POST.get("emailEtudiant")
            Student.objects.create(
                name = nomEtudiant,
                email = emailEtudiant
            )
            messages.success(request, "La création de l'Etudiant s'est effectuée avec succes !")

        elif "modifier" in request.POST:
            ide = request.POST.get("id")
            nomEtudiant = request.POST.get("nomEtudiant")
            emailEtudiant = request.POST.get("emailEtudiant")
            etudiantModifier = Student.objects.get(id=ide)     
            etudiantModifier.name = nomEtudiant
            etudiantModifier.email = emailEtudiant
            etudiantModifier.save()
            messages.success(request, "La modication de l'Etudiant s'est effectuée avec succes !")

        elif "supprimer" in request.POST:
            ide = request.POST.get("id")
            Student.objects.get(id=ide).delete()
            messages.success(request, "La suppression de l'Etudiant s'est effectuée avec succes !")

        elif "search"  in request.POST:
            query = request.POST.get("searchquery")
            students = Student.objects.filter(Q(name__icontains = query) | Q(email__icontains = query))

    contexte = {"students": students}
    return render(request, "index.html", context = contexte)