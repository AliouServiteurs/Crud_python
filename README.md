# Crud_python
Les opérations CRUD avec python dans la gestions des étudiants. Le projet assure l'ajout, la suppression, la modification et la lecture des données dans la base.


# Django mise en place de gestionnaire d'etudiant avec les actions CRUD(Create, Read, Update, Delete)

J'ai d'abord appris les bases de python afin de maitriser la programmation avec python.
Ainsi après des jours d'apprentissage, je maitrise les bases de programmation python.
En ce sens, je me suis dans la maitrise des opérations CRUD qui sont pour moi neccessaire dans le developpement de logiciel et la programmation.

# Creation d'environnement virtuel
La création de l'environnement de virtuel permet d'empêcher le conflit ou probléme entre différent projet de developpement.
Ainsi, l'environnement virtuel concerne un seule projet de developpement avec tout ses dépendances sans affecter rien.
Le dossier sur lequel je crée mon environnement s'appelle : 'Docblog_django_startprojet_crud_operation'
COMMANDE : 
	python -m venv env --> python -m venv : permet la création de l'environnement virtuel avec comme nom {env}
	.\env\Scripts\activate : permet l'exécution de l'environnement virtuel dans windows
   l'environnement n'est pas inclue dans le projet car il contient des milliers de fichiers. Alors créer votre environnement et suivre la suite.
   
# Création de projet django dans l'environnement virtuel
Après l'exécution de l'environnement, je dois créer un projet django pour avoir un ensemble de fichier et dossier bien structuré.
Toujours dans mon dossier 'Docblog_django_startprojet_crud_operation'
COMMANDE :
	pip install django : il faudrait d'abord installer le framework django avec la commande pip de python
	django-admin startproject LeProjet : permet la création de projet django 'LeProjet' que j'ai renommé en 'LeProjetSource'
Ainsi, j'ai créé une application dans le 'LeProjet' pour bien structuré et assurer la maintenance mais je pourrais bien se limiter au projet django
Dans le dossier 'LeProjetSource', je crée l'application
COMMANDE :
	django-admin startapp 'LeAppProjet' : permet la création de l'application 'LeAppProjet' pour dire l'application du projet
Dans le dossier 'LeProjetSource', il existe un fichier python 'manage.py' qui permet de démarrer le projet et générer un url.
L'url permet de tester la fonctionnalité du projet ainsi que les modifications apportés; pour démarrer
COMMANDE : 
	python manage.py runserver : permet le démarrage ou l'eécution du projet (url par défaut : http://127.0.0.1:8000/)

# La création d'éléments de l'application 

J'ai commencé par créer un dossier nommé 'templates' dans l'application('LeProjetSource'). Ensuite, je crée un fichier 'index.html' dans le dossier 'templates'.
Dans l'application, il existe un fichier 'models.py' où j'ai défini mon model Student(Etudiant).
Le model Student représente une classe avec deux attributs qui sont : 'name' : le nom de l'étudiant et 'email' : le couriel de l'étudiant
code source 'models.py' : 

	from django.db import models

	class Student(models.Model):
    		name = models.CharField(max_length=100, verbose_name="Student Name")
    		email = models.EmailField(max_length=227, verbose_name="Student Email")

    		def __str__(self):
        		return str(self.id)

J'ai créé dans le fichier 'admin.py' une class 'StudeAdmin' pour pouvoir créer un admintrateur de la base de donnée.
Le code source 'admin.py' :

	from django.contrib import admin
	from .models import Student

	@admin.register(Student)
	class StudentAdmin(admin.ModelAdmin):
    		list_display = ["id", "name", "email"]

Après la création du model et d'admintrateur, il faudrait faire les commandes :
	python manage.py makemigrations : pour la création de models dans la base de donnée sqlite intégrer par défaut avec es modules python
	python manage.py migrate : pour pouvoir intégrer tout les dépendances
	python manage.py createsuperuser : pour créer un administrateur(login, password, ...)
 
J'ai créé aussi un fichier 'urls.py' dans l'application pour définir l'url d'accés au page 'index.html' de 'templates'.
code source urls.py :
	from django.urls import path
	from .import views

	urlpatterns = [
    		path('', views.index, name="index")
	]

Il existe un fichier 'views.py' dans l'application qui définit les fonctions pour accéder aux différent page.
Dans notre, nous avons qu'une seule page 'index.html' alors j'ai créé une fonction 'index' qui était dans le chemin d'url (path) du code ci-dessus.
La fonction renvoie la page index.html avec la liste des étudiants déjà inscrit sous forme de tableau.
La fonction permet aussi de faire les opérations CRUD selon des conditions. 
L'utilisation de méthode 'post' et l'appuie sur les buttons(avec un attribut 'name' dans 'index.html') qui correspondent à 'ajouter', 'modifier', 'supprimer' permettent d'assure les opérations CRUD.
La requête(request.method) est vérifiée pour savoir ainsi la correspondance de la requête dans la class <class 'django.http.request.QueryDict'>; et la correspondance est vérifiée.
J'ai créée une contexte pour requipérer la liste des étudiants que j'ai utiliser dans le fichier 'index.html'.
code source 'views.py':

from django.shortcuts import render
from .models import Student
from django.contrib import messages
from django.db.models import Q


def index(request):
    students = Student.objects.all()

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



![accueile](https://github.com/user-attachments/assets/3ba4b94d-6a36-4e83-bf3d-2cc0dfedb4a9)

