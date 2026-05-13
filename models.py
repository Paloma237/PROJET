import uuid

from django.db import models

class BaseModel(models.Model):
    """Modèle de base avec les champs communs à tous les modèles"""
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    id = models.UUIDField(
        default=uuid.uuid4,
        null=False,
        blank=False,
        unique=True,
        primary_key=True,
        help_text="Unique identifier for the model instance.",
    )

    class Meta:
        abstract = True

# ──────────────────────────────────────────
# CITÉ / RÉSIDENCE
# ──────────────────────────────────────────

class Cite(BaseModel):
    proprietaire = models.ForeignKey('users.Utilisateur', on_delete=models.CASCADE, related_name='cites')
    nom          = models.CharField(max_length=200, verbose_name="Nom de la résidence")
    adresse      = models.TextField(null=True, blank=True, verbose_name="Adresse")
    quartier     = models.CharField(max_length=100 verbose_name="Quartier", help_text="Nom du quartier")
    ville        = models.CharField(max_length=100, verbose_name="Ville", help_text="Nom de la ville")
    description  = models.TextField(blank=True, null=True, verbose_name="Description", help_text="Description de la résidence")

    def __str__(self):
        return f"{self.nom} — {self.quartier}"
    
    class Meta:
        verbose_name = "city"
        verbose_name_plural = "cities"


# ──────────────────────────────────────────
# CHAMBRE
# ──────────────────────────────────────────

class Chambre(BaseModel):

    #TODO : Creer un fichier enums.py et ajoute les champs choices
    TYPE_CHOICES = [
        ('simple',      'Chambre simple'),
        ('double',      'Chambre double'),
        ('studio',      'Studio'),
        ('appartement', 'Appartement'),
    ]
    STATUT_CHOICES = [
        ('disponible', 'Disponible'),
        ('occupee',    'Occupée'),
        ('suspendue',  'Suspendue'),
    ]

    cite          = models.ForeignKey(Cite, on_delete=models.CASCADE, related_name='chambres')
    titre         = models.CharField(max_length=200)
    type_chambre  = models.CharField(max_length=20, choices=TYPE_CHOICES)
    description   = models.TextField(blank=True, null=True)
    prix_mensuel  = models.DecimalField(max_digits=10, decimal_places=2)
    superficie    = models.FloatField(blank=True, null=True)
    statut        = models.CharField(max_length=20, choices=STATUT_CHOICES, default='disponible')
    wifi          = models.BooleanField(default=False)
    electricite   = models.BooleanField(default=True)
    eau_courante  = models.BooleanField(default=True)
    cuisine       = models.BooleanField(default=False)
    salle_de_bain = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.titre} — {self.cite.nom}"

    def est_disponible(self):
        return self.statut == 'disponible'


# ──────────────────────────────────────────
# PHOTO CHAMBRE
# ──────────────────────────────────────────

class PhotoChambre(BaseModel):
    chambre     = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='photos')
    image       = models.ImageField(upload_to='chambres/')
    principale  = models.BooleanField(default=False)

    def __str__(self):
        return f"Photo de {self.chambre.titre}"


# ──────────────────────────────────────────
# RÉSERVATION
# ──────────────────────────────────────────

class Reservation(BaseModel):
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('confirmee',  'Confirmée'),
        ('annulee',    'Annulée'),
        ('terminee',   'Terminée'),
    ]

    etudiant   = models.ForeignKey('users.Utilisateur', on_delete=models.CASCADE, related_name='reservations')
    chambre    = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='reservations')
    date_debut = models.DateField()
    date_fin   = models.DateField()
    statut     = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    message    = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.etudiant.email} → {self.chambre.titre}"

    def duree_mois(self):
        return round((self.date_fin - self.date_debut).days / 30)

    def montant_total(self):
        return self.chambre.prix_mensuel * self.duree_mois()


# ──────────────────────────────────────────
# PAIEMENT
# ──────────────────────────────────────────

class Paiement(BaseModel):
    METHODE_CHOICES = [
        ('mtn_momo',     'MTN Mobile Money'),
        ('orange_money', 'Orange Money'),
        ('especes',      'Espèces'),
    ]
    STATUT_CHOICES = [
        ('en_attente', 'En attente'),
        ('reussi',     'Réussi'),
        ('echoue',     'Échoué'),
    ]

    reservation   = models.ForeignKey(Reservation, on_delete=models.CASCADE, related_name='paiements')
    montant       = models.DecimalField(max_digits=10, decimal_places=2)
    methode       = models.CharField(max_length=20, choices=METHODE_CHOICES)
    statut        = models.CharField(max_length=20, choices=STATUT_CHOICES, default='en_attente')
    reference     = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.montant} FCFA — {self.get_statut_display()}"


# ──────────────────────────────────────────
# AVIS
# ──────────────────────────────────────────

class Avis(BaseModel):
    etudiant    = models.ForeignKey('users.Utilisateur', on_delete=models.CASCADE, related_name='avis')
    chambre     = models.ForeignKey(Chambre, on_delete=models.CASCADE, related_name='avis')
    note        = models.IntegerField(choices=[(i, i) for i in range(1, 6)])
    commentaire = models.TextField(blank=True, null=True)

    class Meta:
        unique_together = ('etudiant', 'chambre')

    def __str__(self):
        return f"{self.note}★ — {self.etudiant.email} sur {self.chambre.titre}"