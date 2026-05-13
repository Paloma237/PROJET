from django.shortcuts import redirect, render
from datetime import datetime
from .forms import contactForm
from .models import Message

# Create your views here.
def index(request):
    context = {
        'messages': [
            {
                'text': 'Hello World',
                'color': 'red',
                'created_at': datetime.now(),
            },
            {
                'text': 'Hello World',
                'color': 'red',
                'created_at': datetime.now(),
            },
            {
                'text': 'Hello World',
                'color': 'red',
                'created_at': datetime.now(),
            }
        ]
    }
    return render(request, template_name='index.html', context=context)
#utiliser un formulaire dasn une vue
def contact(request):
    if request.method == 'POST':
        form = contactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            message = form.cleaned_data['message']
            return redirect('index')
            # Traitez les données du formulaire (par exemple, envoyez un e-mail)
    else:
        form = contactForm()
    return render(request, 'contact.html', {'form': form})