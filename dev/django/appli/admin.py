from email.message import Message
from .models import Message

from django.contrib import admin

# Register your models here.
#creer un super utilisateur pour acceder a l'admin
#python manage.py createsuperuser

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('text', 'color', 'created_at')
    list_filter = ('color', 'created_at')
    search_fields = ('text',)
    ordering = ('-created_at',)
    list_editable = ('color',)
    readonly_fields = ('created_at',)
    fieldsets = [(
        'Message Information',
        {
            'fields': ('text', 'color', 'created_at'),
            'description': 'Information about the message',
        }
    )]