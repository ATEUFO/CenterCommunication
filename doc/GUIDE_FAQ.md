# 🎓 GUIDE COMPLET - FAQ CouCou

## ❓ Pourquoi l'URL `http://127.0.0.1:8000/` renvoie un 404 ?

### ✅ **Réponse**: C'est normal au départ !

Avant la modif, il n'y had pas d'endpoint sur la racine `/`. Maintenant, **c'est fixé** !

### Les changements effectués:
1. ✅ Créé `config/views.py` avec une page d'accueil
2. ✅ Modifié `config/urls.py` pour ajouter la racine
3. ✅ Ajouté `permission_classes = [AllowAny]` pour accès sans login

### **Résultat**:
```bash
curl http://127.0.0.1:8001/
```
Retourne:
```json
{
  "message": "🎓 Bienvenue sur CouCou",
  "description": "Babillard intelligent d'établissement scolaire",
  "endpoints": {...}
}
```

---

## 👤 Comment créer un utilisateur admin dans Django

### **3 Méthodes:**

### **Méthode 1: Commande Django personnalisée (RECOMMANDÉE)** ✅

```bash
source venv/bin/activate
python manage.py create_admin
```

**Résultat**:
- ✅ Admin créé (ou existe déjà)
- ✅ 3 utilisateurs de test créés
- ✅ Établissement et classes créés
- ✅ Données de test prêtes

---

### **Méthode 2: Django Shell**

```bash
source venv/bin/activate
python manage.py shell
```

```python
from accounts.models import User

# Créer un super utilisateur
User.objects.create_superuser(
    username='admin',
    email='admin@example.com',
    password='admin123',
    role='ADMIN'
)

# Ou créer un utilisateur simple
User.objects.create_user(
    username='john',
    email='john@example.com',
    password='john123',
    role='STUDENT'
)

exit()
```

---

### **Méthode 3: Ligne de commande Django (Quick)**

```bash
python manage.py createsuperuser
# Puis répondre aux questions
```

⚠️ **Limitation**: Ne définit pas le rôle. Faut le faire après en shell.

---

## 📝 Configuration du .env pour les tests

### **Fichier `.env` configuré pour DÉVELOPPEMENT/TESTS**:

```env
# 🔧 Configuration CouCou - DÉVELOPPEMENT
DEBUG=True
SECRET_KEY=django-insecure-u@c(ph)1$^5-8-7aouear75=(t^31348h#_)99#9=u$3oj*ufo
ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0

# DATABASE - SQLite pour les tests
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# SECURITY - Désactivé pour développement
SECURE_SSL_REDIRECT=False
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False

# EMAIL - Console pour logs
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend

# ADMIN
ADMIN_USERNAME=admin
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=admin123

# API
API_VERSION=v1
REST_FRAMEWORK_PAGE_SIZE=20
```

✅ **Tous les tests vont fonctionner maintenant !**

---

## 🚀 Démarrage du Projet

### **1. Activation de l'environnement**
```bash
cd /home/arthur/Documents/Projets_en_cour/CouCou
source venv/bin/activate
```

### **2. Création des utilisateurs (IMPORTANT!)**
```bash
python manage.py create_admin
```

### **3. Lancer le serveur**
```bash
python manage.py runserver 0.0.0.0:8001
```

### **4. Accès**

| URL | Description | User | Pass |
|-----|-------------|------|------|
| http://127.0.0.1:8001/ | 🏠 Page d'accueil | - | - |
| http://127.0.0.1:8001/admin/ | 👑 Admin | admin | admin123 |
| http://127.0.0.1:8001/api/v1/ | 📚 API REST | - | - |

---

## 👨‍💼 Utilisateurs de Test Créés

Après `python manage.py create_admin`:

```
• etudiant_bob         (Étudiant)      - bob.bernard@school.com
• etudiant_alice       (Étudiant)      - alice.martin@school.com
• prof_jean            (Enseignant)    - jean.dupont@school.com
• admin                (Admin)         - admin@example.com
```

**Tous les mots de passe**: 
- Admin: `admin123`
- Profs: `prof123`
- Étudiants: `etudiant123`

---

## 🧪 Tests de l'API

### **1. Page d'accueil (Sans authentification)**
```bash
curl http://127.0.0.1:8001/

# Résultat:
# {
#   "message": "🎓 Bienvenue sur CouCou",
#   ...
# }
```

### **2. Tester les endpoints (Avec authentification)**

**Méthode 1: Via le navigateur**
1. Aller sur http://127.0.0.1:8001/admin/
2. Se connecter (admin/admin123)
3. Puis visiter http://127.0.0.1:8001/api/v1/auth/users/

**Méthode 2: Via curl (Session)**
```bash
# 1. Login
curl -c cookies.txt -d "username=admin&password=admin123" \
  http://127.0.0.1:8001/api-auth/login/

# 2. Accéder à l'API
curl -b cookies.txt http://127.0.0.1:8001/api/v1/auth/users/
```

**Méthode 3: Via curl (Token BasAuth)**
```bash
curl -u admin:admin123 http://127.0.0.1:8001/api/v1/auth/users/
```

---

## 📊 Vérifications après Configuration

### **Vérifier le serveur**
```bash
python manage.py check
# ✓ System check identified no issues (0 silenced).
```

### **Vérifier les migrations**
```bash
python manage.py showmigrations
# ✓ [X] pour tous les apps
```

### **Vérifier les utilisateurs**
```bash
python manage.py shell
>>> from accounts.models import User
>>> User.objects.all().count()
# Devrait retourner: 4 (admin + 3 tests)
```

### **Test du projet**
```bash
python test_project.py
# ✓ Tous les tests PASSÉS
```

---

## 💡 Commandes Utiles

```bash
# Créer les utilisateurs
python manage.py create_admin

# Accéder au shell Django
python manage.py shell

# Faire les migrations
python manage.py makemigrations

# Appliquer les migrations
python manage.py migrate

# Vider la base de données
python manage.py flush

# Créer un nouveau superuser
python manage.py createsuperuser

# Collecter les fichiers statiques
python manage.py collectstatic

# Runserver sur un port différent
python manage.py runserver 0.0.0.0:8002

# Vérifier la configuration
python manage.py check --deploy
```

---

## 🐛 Problèmes Courants & Solutions

### **Problème: Port 8000 déjà utilisé**
```bash
# Solution: Utiliser un port différent
python manage.py runserver 0.0.0.0:8001
```

### **Problème: Utilisateurs non trouvés**
```bash
# Solution: Exécuter la commande de création
python manage.py create_admin
```

### **Problème: Migrations non appliquées**
```bash
# Solution: Appliquer les migrations
python manage.py migrate
```

### **Problème: "No such table" dans la BD**
```bash
# Solution: Supprimer db.sqlite3 et refaire les migrations
rm db.sqlite3
python manage.py migrate
python manage.py create_admin
```

---

## ✅ Résumé Final

| Élément | Status | Details |
|---------|--------|---------|
| **Page d'accueil (/)** | ✅ | Fonctionne maintenant |
| **Admin (/admin/)** | ✅ | Fonctionnel |
| **Utilisateurs** | ✅ | 4 créés (admin + 3 test) |
| **BD** | ✅ | Configuration de développement |
| **API** | ✅ | Prête à tester |
| **.env** | ✅ | Configuré pour tests |

---

**Vous êtes prêt ! Tout fonctionne maintenant ! 🎉**
