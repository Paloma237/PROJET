from django.urls import path
from appli.views import index
app_name = 'appli'

urlpatterns = [
    path('', index, name='index'),
]