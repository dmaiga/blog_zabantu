# 🌍 Zabantu – Plateforme Éditoriale Collaborative

**Zabantu** est une plateforme éditoriale collaborative dédiée à la publication de travaux, d’analyses, de comptes rendus de séminaires et d’actualités en lien avec les dynamiques sociales, politiques et culturelles contemporaines.

---

## ✨ Fonctionnalités principales

- 📝 **Articles & Analyses** : rédaction, édition et publication d’articles (avec éditeur WYSIWYG et prévisualisation).
- 🎓 **Séminaires Guelekan** : espace dédié aux comptes rendus et discussions académiques.
- 📅 **Événements** : création, gestion et mise en avant des événements.
- 🖼️ **Galeries & Photos** : bibliothèque multimédia intégrée.
- 👥 **Membres & Partenaires** : gestion des profils, affichage public et espace privé.
- 🔒 **Espace sécurisé** : authentification, gestion des rôles (membres, administrateurs).
- ⏳ **Publication programmée** : planification automatique des mises en ligne.

---

## 🛠️ Stack technique

- **Backend** : [Django](https://www.djangoproject.com/) (Python 3)
- **Base de données** : SQLite (dev) – PostgreSQL/MySQL (prod possible)
- **Frontend** : Templates Django + Bootstrap 5 (responsive, épuré)
- **Containerisation** : Docker & Docker Compose
- **Gestion des utilisateurs** : Django Auth
- **Éditeur de texte** : TinyMCE (intégré)
- **Hébergement cible** : LWS / Railway / Render

---

## 📂 Structure du projet
projet_zabantu/
├── src/
│ ├── articles/ # Gestion des articles & séminaires Guelekan
│ ├── events/ # Module événements
│ ├── gallery/ # Galeries et bibliothèque multimédia
│ ├── site_web/ # Pages publiques (accueil, contact, about, etc.)
│ ├── users/ # Authentification, profils et gestion des membres
│ └── zabantu/ # Fichiers principaux Django (settings, urls, wsgi)
├── docker-compose.yml # Orchestration multi-services
├── Dockerfile # Image de base pour Django
├── requirements.txt # Dépendances Python
└── README.md # Documentation projet


