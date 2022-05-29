from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Note

admin.site.register(Note)             # Ajouter la table Note au site d'administration
admin.site.register(User, UserAdmin)  # Ajouter l'utilisateur modifié...