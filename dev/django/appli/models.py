from django.db import models


#creer des modèles 
class Message(models.Model):
    text=models.CharField(max_length=100)
    color=models.CharField(max_length=50)
    created_at=models.DateTimeField(auto_now_add=True)
