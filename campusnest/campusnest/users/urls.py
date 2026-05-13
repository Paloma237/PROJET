from django.urls import path

from campusnest.users.views.pageAcceuil_views import AccueilView

app_name = "users"
urlpatterns = [
    path('', AccueilView.as_view(), name='accueil'),
]
