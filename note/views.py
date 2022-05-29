
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils import timezone

from .models import Note, User

def index(request):

    if request.POST:

        if request.POST['submit']=='Connexion' :                              # Si l'utilisateur s'est connecté
            user = User.objects.filter(email=request.POST['email']).first()
            if user is not None:                                              # On verifie s'il existe
                if user.check_password(request.POST['password']):             # Et si le mot de pass est bon
                    request.session['user_id']=user.id                        # On enregistre son id dans la session
                    return HttpResponseRedirect(reverse('note:notes'))        # on le connecte
            return HttpResponseRedirect(reverse('note:index'))                # si non reconnu, on on redirige vers la page de connexion
            
        elif request.POST['submit']=='Inscription' :                                       # Si l'utilisateur s'inscrit
            new = User(last_name=request.POST['nom'], first_name=request.POST['prenom'],   # On le crée
                    email=request.POST['email'], date=request.POST['naissance'])
            new.set_password(request.POST['password'])
            new.save()                                                                     # On le sauvegarde
            request.session['user_id']=user.id                                             # On enregistre son id dans la session
            return HttpResponseRedirect(reverse('note:notes'))                             # et on le connecte

    return render(request, "note/index.html")                                       # Si aucun formulaire de validé, on charge juste la page

def detail(request, note_id):

    #On recupere la note
    note = get_object_or_404(Note, id=note_id)

    if request.method == "POST":                          

        # S'il s'agit d'une modification, on l'enregistre    
        if request.POST["submit"]=="Enregistrer":            
            note.Name = request.POST['name']
            note.Description = request.POST['note']
            note.modified_at = timezone.now()
            note.save()
            return HttpResponseRedirect(reverse('note:detail', args=(note.id,)))

        # si c'est une suppression, on supprime la note
        elif request.POST["submit"]=="Supprimer":
            note.delete()
            return HttpResponseRedirect(reverse('note:notes'))

    return render(request, "note/detail.html", {'note': note})

def notes(request):

    # On recuprer l'utilisateur à partir de session
    user_id = request.session['user_id']             
    user = User.objects.get(pk=user_id)

    # Si il a ajouté une nouvelle note, on enregistre et on recharge la page
    if request.method == "POST":
        user.note_set.create(Name=request.POST['name'], Description=request.POST['note'],
                    created_at=timezone.now(), modified_at=timezone.now())
        return HttpResponseRedirect(reverse('note:notes'))

    context = {
        'note_list': user.note_set.all(),
    }
    return render(request, "note/notes.html", context)      # On affiche la page avec la liste des notes de l'utilisateur