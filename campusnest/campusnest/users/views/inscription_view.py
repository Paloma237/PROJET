from django.shortcuts import render, redirect
from django.views                              import View
from django.contrib                            import messages
from django.contrib.auth.password_validation  import validate_password
from django.core.exceptions                   import ValidationError
from django.core.validators                   import validate_email

from users.models import Utilisateur, ProfilClient, ProfilProprietaire


# ══════════════════════════════════════════════════════════════════
#  VUE D'INSCRIPTION UNIQUE  (étudiant + propriétaire)
#  Utilisation d'une Class-Based View  —  sans forms.py
# ══════════════════════════════════════════════════════════════════
class InscriptionView(View):
    """
    GET  → affiche le formulaire vide.
    POST → valide manuellement les données POST, crée Utilisateur
           + ProfilClient  ou ProfilProprietaire selon le rôle.
    """

    template_name = 'home/authentification/inscription.html'

    # ──────────────────────────────────────────────
    # GET
    # ──────────────────────────────────────────────
    def get(self, request):
        return render(request, self.template_name, {
            'role_initial': 'client',
        })

    # ──────────────────────────────────────────────
    # POST
    # ──────────────────────────────────────────────
    def post(self, request):
        data = request.POST

        # ── 1. Récupération des champs ───────────
        role        = data.get('role', 'client').strip()
        username    = data.get('username', '').strip()
        email       = data.get('email', '').strip()
        telephone   = data.get('telephone', '').strip()
        password1   = data.get('password1', '')
        password2   = data.get('password2', '')
        nom_complet = data.get('nom_complet', '').strip()   # propriétaire
        filiere     = data.get('filiere', '').strip()        # étudiant
        niveau      = data.get('niveau', '').strip()         # étudiant

        errors       = []
        field_errors = {}

        # ── 2. Validations communes ──────────────

        if role not in ('client', 'proprietaire'):
            errors.append("Rôle invalide.")

        # Nom d'utilisateur
        if not username:
            field_errors['username'] = "Le nom d'utilisateur est obligatoire."
        elif Utilisateur.objects.filter(username=username).exists():
            field_errors['username'] = "Ce nom d'utilisateur est déjà pris."

        # Email
        if not email:
            field_errors['email'] = "L'adresse e-mail est obligatoire."
        else:
            try:
                validate_email(email)
            except ValidationError:
                field_errors['email'] = "Adresse e-mail invalide."
            else:
                if Utilisateur.objects.filter(email=email).exists():
                    field_errors['email'] = "Un compte existe déjà avec cet e-mail."

        # Mots de passe
        if not password1:
            field_errors['password1'] = "Le mot de passe est obligatoire."
        elif password1 != password2:
            field_errors['password2'] = "Les mots de passe ne correspondent pas."
        else:
            try:
                validate_password(password1)
            except ValidationError as exc:
                field_errors['password1'] = exc.messages[0]

        # ── 3. Validations spécifiques au rôle ───

        if role == 'proprietaire' and not nom_complet:
            field_errors['nom_complet'] = "Le nom complet est obligatoire."

        # ── 4. Erreurs → ré-afficher le formulaire
        if errors or field_errors:
            return render(request, self.template_name, {
                'errors'      : errors,
                'field_errors': field_errors,
                'form_data'   : data,      # re-remplissage des champs
            })

        # ── 5. Création de l'utilisateur ─────────
        utilisateur = Utilisateur.objects.create_user(
            username  = username,
            email     = email,
            password  = password1,
            role      = role,
            telephone = telephone or None,
        )

        # ── 6. Création du profil selon le rôle ──
        if role == 'client':
            ProfilClient.objects.create(
                utilisateur = utilisateur,
                filiere     = filiere or None,
                niveau      = niveau  or None,
            )
        else:
            ProfilProprietaire.objects.create(
                utilisateur = utilisateur,
                nom_complet = nom_complet,
            )

        # ── 7. Succès → redirection ───────────────
        messages.success(
            request,
            f"Compte créé avec succès ! Bienvenue, {username}. "
            "Vous pouvez maintenant vous connecter."
        )
        return redirect('connexion')
    