
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

# Table utilisateur recréé pour ajouter la date
class User(AbstractUser):
    
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    date = models.DateField('birth date', default=None, blank=True, null=True)
    
    USERNAME_FIELD = 'email'            # Se connecter avec l'email
    REQUIRED_FIELDS = ['username']      # pour demander le champ lors de la creation du super utilisateur et eviter une erruer

    def __str__(self):
        return self.first_name+" "+self.last_name

class Base(models.Model):
    id= models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)   # id de type uuid
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField()
    modified_at = models.DateTimeField()

    class Meta:
        abstract = True           # class abstraite pour pouvoir en heriter


class Note(Base):
    Name = models.CharField(max_length=100)
    Description = models.CharField(max_length=500)

    def __str__(self):           # Definir le format sous lequel representer la note
        return "["+self.created_by.first_name+" "+self.created_by.last_name+"] "+self.Name