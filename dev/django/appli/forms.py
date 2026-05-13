#formulaire simple
from django import forms

class contactForm(forms.Form):
    name = forms.CharField(label='Votre nom', max_length=100)
    email = forms.EmailField(label='Votre adresse e-mail')
    message = forms.CharField(label='Votre message', widget=forms.Textarea)

#message form(lié au model message  pour créer un message à partir d'un formulaire)

from django import forms
from .models import Message

class messageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['text', 'color']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'created_at': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'text': 'Message',
            'color': 'Couleur',
            'created_at': 'Date de création',
        }