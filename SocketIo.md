# Fonctionnement de Socket.IO dans CenterCommunication

Ce document explique comment le temps réel est implémenté dans l'application pour permettre les commentaires et notifications instantanés.

## 1. Architecture Générale

L'application utilise une architecture **hybride** permettant de combiner la robustesse de Django avec la réactivité de Socket.IO.

*   **Serveur ASGI (Uvicorn)** : Contrairement au serveur de développement classique, Uvicorn permet de gérer à la fois les requêtes HTTP (Django) et les connexions persistantes (WebSockets/Socket.IO).
*   **python-socketio** : La bibliothèque utilisée côté serveur pour gérer les événements et les "salons" (rooms).
*   **Socket.io Client** : Inclus dans `base.html` pour connecter le navigateur au serveur.

## 2. Le Système de "Salons" (Rooms)

Pour éviter de surcharger les clients avec des messages inutiles, Socket.IO utilise des **rooms**.

*   Lorsqu'un utilisateur ouvre une annonce (Post), le client émet l'événement `join_post` avec l'ID du post.
*   Le serveur place alors cette connexion dans un salon nommé `post_{id}`.
*   Cela garantit que seuls les utilisateurs consultant la **même annonce** reçoivent les nouveaux commentaires en temps réel.

## 3. Flux de Données d'un Commentaire

Voici ce qui se passe quand un commentaire est posté :

1.  **Envoi** : Le client envoie les données du commentaire via une requête `POST` standard à l'API Django.
2.  **Sauvegarde** : Django enregistre le commentaire en base de données.
3.  **Signal** : Un signal Django (`post_save`) se déclenche automatiquement dans `apps/comments/signals.py`.
4.  **Émission** : Le signal appelle la fonction `emit_new_comment()` qui transmet les données au serveur Socket.IO.
5.  **Diffusion** : Socket.IO diffuse l'événement `new_comment` uniquement au salon `post_{id}` correspondant.
6.  **Réception** : Les navigateurs des autres utilisateurs reçoivent l'événement et ajoutent le commentaire à la liste dynamiquement (sans recharger la page).

## 4. Événements Disponibles

| Événement | Direction | Description |
| :--- | :--- | :--- |
| `connect` | Client → Serveur | Initialise la connexion temps réel. |
| `join_post` | Client → Serveur | Rejoint le salon d'une annonce spécifique. |
| `new_comment` | Serveur → Client | Envoie les données d'un nouveau commentaire ou d'une réponse. |
| `connection_success` | Serveur → Client | Confirme que la connexion Socket.IO est active. |

## 5. Comment lancer le temps réel ?

Pour que Socket.IO fonctionne, vous **devez** lancer l'application avec la commande suivante :

```bash
./venv/bin/python -m uvicorn config.asgi:application --host 0.0.0.0 --port 8000
```

> [!IMPORTANT]
> Si vous utilisez `python manage.py runserver`, l'application fonctionnera pour les pages classiques, mais les fonctionnalités **temps réel** (Socket.IO) seront désactivées.
