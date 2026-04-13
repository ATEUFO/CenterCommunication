# 🚀 QUICK START - CenterCommunication

## En 3 Commandes

```bash
# 1. Naviguer au projet
cd /home/arthur/Documents/Projets_en_cour/CenterCommunication

# 2. Activer l'environnement
source venv/bin/activate

# 3. Lancer le serveur
python manage.py runserver 0.0.0.0:8000
```

## Accès Immédiat

- **Accueil**: http://127.0.0.1:8000/
- **Admin**: http://127.0.0.1:8000/admin/
- **API**: http://127.0.0.1:8000/api/v1/

---

## 🔐 Identifiants

| Utilisateur    | Rôle          | Password    |
| -------------- | ------------- | ----------- |
| admin          | 👑 Admin      | admin123    |
| prof_jean      | 👨‍🏫 Enseignant | prof123     |
| etudiant_alice | 👨‍🎓 Étudiant   | etudiant123 |
| etudiant_bob   | 👨‍🎓 Étudiant   | etudiant123 |

---

## 📝 Configuration

**Port**: 8000 ✓  
**Host**: 0.0.0.0 ✓  
**DEBUG**: True (développement) ✓  
**Database**: SQLite ✓  
**Locale**: Français (FR) ✓

---

## 🎯 Points d'Accès

### Page d'Accueil API

```bash
curl http://127.0.0.1:8000/
```

Voir tous les endpoints disponibles en JSON

### Interface Admin Django

http://127.0.0.1:8000/admin/

- Login: admin / admin123
- Gérer tous les modèles

### API REST Endpoints

- `/api/auth/users/` - Users
- `/api/academic/establishments/` - Établissements
- `/api/academic/classrooms/` - Classes
- `/api/academic/students/` - Étudiants
- `/api/academic/teachers/` - Enseignants
- `/api/posts/posts/` - Publications
- `/api/comments/comments/` - Commentaires
- `/api/notifications/notifications/` - Notifications

---

## 🧪 Tester l'API

### Méthode 1: Navigateur

1. Aller sur http://127.0.0.1:8000/admin/
2. Se connecter (admin/admin123)
3. Visiter http://127.0.0.1:8000/api/v1/auth/users/

### Méthode 2: cURL

```bash
curl -u admin:admin123 http://127.0.0.1:8000/api/v1/auth/users/
```

### Méthode 3: Bruno/Postman

- Base URL: http://127.0.0.1:8000
- Auth: Basic Auth (admin/admin123)

---

## ⚙️ Commandes Utiles

```bash
# Créer/Réinitialiser les utilisateurs
python manage.py create_admin

# Vérifier la configuration
python manage.py check

# Accéder au shell Django
python manage.py shell

# Faire les migrations
python manage.py migrate

# Collecte les fichiers statiques
python manage.py collectstatic

# Vider la base de données
python manage.py flush
```

---

## 📊 Vérifications

- ✓ Port 8000 libre et écouté
- ✓ ALLOWED_HOSTS configuré
- ✓ Migrations appliquées
- ✓ Utilisateurs créés
- ✓ Admin accessible
- ✓ API fonctionnelle

---

## ❓ Aide

Voir les fichiers de documentation:

- `GUIDE_FAQ.md` - Questions fréquentes
- `DOCUMENTATION.md` - Documentation complète
- `CORRECTIONS_PORT_8000.md` - Corrections apportées

---

**L'application est prête! 🎉**
