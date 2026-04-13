#!/bin/bash

# Script pour lancer le serveur CenterCommunication sur le port 8000

cd /home/arthur/Documents/Projets_en_cour/CenterCommunication

echo "🚀 Démarrage de CenterCommunication..."
echo ""

# Activer l'environnement virtuel
source venv/bin/activate

# Vérifier les migrations
echo "📋 Vérification des migrations..."
python manage.py migrate --noinput

# Vérifier la configuration
echo "✓ Vérification de la configuration..."
python manage.py check

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "🎓 CenterCommunication démarre sur :"
echo "   http://127.0.0.1:8000/"
echo ""
echo "📚 Endpoints disponibles :"
echo "   - Admin:   http://127.0.0.1:8000/admin/"
echo "   - API:     http://127.0.0.1:8000/api/v1/"
echo ""
echo "🔐 Utilisateurs test :"
echo "   - admin (admin123)"
echo "   - prof_jean (prof123)"
echo "   - etudiant_alice (etudiant123)"
echo "   - etudiant_bob (etudiant123)"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Lancer le serveur
python manage.py runserver 0.0.0.0:8000
