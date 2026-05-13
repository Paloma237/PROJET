
from typing import ClassVar
from django.db import models

from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from campusnest.global_data.enums import ROLE_CHOICES
from campusnest.core.models import BaseModel

from .managers import UserManager

class User(AbstractUser, BaseModel):
    """
    Custom user model with additional fields for CampusNest.
    """
    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES.choices,
        default=ROLE_CHOICES.CLIENT,
        verbose_name="Rôle",
        help_text="Rôle de l'utilisateur dans l'application"
    )
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=20, blank=True, null=True)
    first_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200, blank=True, null=True)
    photo_profil = models.ImageField(upload_to='profils/', blank=True, null=True)
    
    objects: ClassVar[UserManager] = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return f"{self.email} ({self.get_role_display()})"

    def est_client(self):
        return self.role == ROLE_CHOICES.CLIENT

    def est_proprietaire(self):
        return self.role == ROLE_CHOICES.PROPRIETAIRE
    
    def save(self, *args, **kwargs):
        # Les superusers sont toujours admin
        if self.is_superuser:
            self.role = 'admin'
            self.is_staff = True
        super().save(*args, **kwargs)
    
    @property
    def is_admin(self):
        """Propriété pour vérifier si l'utilisateur est admin"""
        return self.role == 'admin' or self.is_superuser
    
    def has_admin_access(self):
        """Vérifie l'accès à l'interface admin Django"""
        return self.is_superuser or self.role == 'admin'


class Client(BaseModel):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_client')
    filiere = models.CharField(max_length=100, blank=True, null=True)
    niveau = models.CharField(max_length=20, blank=True, null=True)
    universite = models.CharField(max_length=150, default='IUT-FV Bandjoun')

    def __str__(self):
        return f"Étudiant : {self.User.email}"


class Proprietaire(BaseModel):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil_proprietaire')
    piece_identite = models.FileField(upload_to='pieces_identite/', blank=True, null=True)
    verifie = models.BooleanField(default=False)

    def __str__(self):
        return f"Propriétaire : {self.User.get_full_name()}"
