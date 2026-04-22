# News Digest API

Une API robuste et asynchrone conçue pour agréger, stocker et gérer des flux d'actualités technologiques, avec un système complet de gestion des interactions utilisateurs.

## 🚀 Fonctionnalités
* **Agrégation Automatisée** : Scraping de news en arrière-plan via GNews API (scheduler intégré).
* **Architecture Orientée Service** : Séparation claire entre les modèles, les repositories et les endpoints.
* **Gestion des Interactions** : Système complet de likes, de notes et de suivi de lecture.
* **Validation Stricte** : Utilisation de Pydantic v2 pour des données typées et sécurisées.
* **Résilience** : Gestion des timeouts et stratégies de "retry" pour les appels API externes.
* **Non-bloquant** : Scheduler asynchrone pour ne pas ralentir le démarrage du serveur.

## 🛠 Stack Technique
* **Framework** : [FastAPI](https://fastapi.tiangolo.com/)
* **ORM** : [SQLAlchemy](https://www.sqlalchemy.org/) avec SQLite
* **Validation** : [Pydantic v2](https://docs.pydantic.dev/)
* **Background Tasks** : [APScheduler](https://apscheduler.readthedocs.io/)
* **HTTP Client** : [Requests](https://requests.readthedocs.io/) avec `HTTPAdapter`

## 📦 Installation

1. Cloner le projet :
   ```bash
   git clone https://github.com/Jovialngandu/news_digest_api.git
   cd news_digest_api
Créer l'environnement virtuel :
```bash
python -m venv env
source env/bin/activate  # Sur Linux/Mac
```
Installer les dépendances :
```bash
pip install -r requirements.txt
```
⚙️ Configuration

Crée un fichier .env à la racine du projet en vous basant sur .env.example :

Extrait de code

```bash
DATABASE_URL=sqlite:///./app_data.db
GNEWS_API_KEY=ta_cle_api_ici
GNEWS_BASE_URL=[https://gnews.io/api/v4/top-headlines](https://gnews.io/api/v4/top-headlines)
```
🚀 Démarrage
Lancer le serveur de développement :

```bash
uvicorn main:app --reload
```
📚 Documentation API

Une fois le serveur lancé, accède à la documentation interactive (Swagger UI) pour tester tes endpoints :
http://127.0.0.1:8000/docs

🏗 Structure du Projet

```Plaintext
app/
├── api/v1/         # Endpoints (articles, interactions, sources)
├── core/           # Configuration, DB, Settings
├── models/         # Modèles SQLAlchemy
├── repositories/   # Logique d'accès aux données
├── schemas/        # Modèles Pydantic (validation)
└── services/       # Logique métier (scraping)
```