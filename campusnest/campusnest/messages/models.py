from django.db import models
from users.models import User
from core.models import Chambre
from core.models import BaseModel

class Message(BaseModel):
    """
    Message envoyé par un utilisateur à un autre
    """
    expediteur   = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_envoyes')
    destinataire = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages_recus')
    chambre      = models.ForeignKey(Chambre, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    contenu      = models.TextField()
    lu           = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']

    def __str__(self):
        return f"De {self.expediteur.email} à {self.destinataire.email}"
    
