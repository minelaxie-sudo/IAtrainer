# IAtrainer - Système d'Entraînement Multi-Agents

Un système complet pour entraîner un modèle LLM libre (Llama, Mistral, etc.) spécialisé dans la génération de code, utilisant un système multi-agents (Coder A, Coder B, Arbitre) qui scrape automatiquement internet. Le modèle entraîné est directement utilisable avec **Ollama** et s'intègre parfaitement avec **UnityIAPro** pour générer automatiquement du code Unity/Unreal.

## 🎯 Fonctionnalités

### 🕷️ Web Scraping Gratuit
- **Scrape automatique** depuis DuckDuckGo, GitHub et Stack Overflow
- **Sans API payante** - utilise BeautifulSoup et requests
- **Au plus rapide** - pas de délais inutiles
- **Option code-only** - scrape uniquement du code pour un modèle full codage

### 🤖 Système Multi-Agents
- **Coder A** : Génère une première solution
- **Coder B** : Génère une solution alternative
- **Arbitre** : Compare et choisit la meilleure approche
- **Feedback** : Les agents apprennent de chaque itération

### 📊 Entraînement du Modèle
- **Fine-tuning** automatique avec les données scrapées
- **Métriques** de performance en temps réel
- **Persistance** des décisions et apprentissages
- **Export au format Ollama** (GGUF) pour utilisation directe

### 🔗 Intégration UnityIAPro
- **Synchronisation en temps réel** avec le dashboard
- **Visualisation** des conversations et décisions
- **Alertes** automatiques en cas d'erreur
- **Logs** complets de toutes les interactions

### 🚀 API HTTP Locale
- **Génération de code** indépendante
- **Analyse de code** (qualité, sécurité, performance)
- **Comparaison** de solutions
- **Entraînement** du modèle
- **Export au format Ollama** (GGUF) pour utilisation directe

## 📦 Installation

### Prérequis
- Python 3.8+
- pip ou conda

### Setup
```bash
# Cloner le repository
git clone https://github.com/minelaxie-sudo/IAtrainer.git
cd IAtrainer

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# Installer les dépendances
pip install -r requirements.txt
```

### Dépendances optionnelles

Pour le fine-tuning réel avec PyTorch (optionnel) :
```bash
# CPU uniquement
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Transformers pour fine-tuning
pip install transformers scikit-learn pydantic
```

Pour Selenium avec navigateur (scraping avancé, optionnel) :
```bash
pip install selenium
```

**Note** : Les dépendances principales (scraping, API, multi-agents) fonctionnent sans ces packages optionnels.

## 🚀 Utilisation

### 1. Lancer l'API du modèle (optionnel)

**L'API sert à :**
- Générer du code basé sur des prompts
- Analyser du code (qualité, sécurité, performance)
- Comparer deux solutions de code
- Entraîner le modèle avec de nouvelles données
- Exporter le modèle au format Ollama (GGUF)

**Lancer l'API avec configuration interactive :**
```bash
python model_api.py
```

Un menu interactif s'affichera pour configurer :
- Nom du modèle
- Nombre de tokens par défaut
- Température
- Top-P
- Host et port

Après configuration, l'API démarre sur `http://localhost:8000`

**Accéder à l'API :**
- Documentation interactive: http://localhost:8000/docs
- Vérifier l'état: http://localhost:8000/health
- Configuration: http://localhost:8000/config

### 2. Lancer une session d'entraînement

**Paramètres :**

- `--topic` (requis) - Sujet d'entraînement (ex: "Unity development")
- `--pages` (optionnel, défaut: 5) - Nombre de pages à scraper
- `--iterations` (optionnel, défaut: 10) - Nombre d'itérations d'entraînement
- `--code-only` (optionnel) - Scraper uniquement du code
- `--dashboard-url` (optionnel) - URL du dashboard UnityIAPro
- `--no-dashboard` (optionnel) - Désactiver le dashboard

**Pour la liste complète des paramètres, voir `COMPLETE_GUIDE.md`**

#### Avec intégration UnityIAPro
```bash
python orchestrator.py \
  --topic "Unity game development" \
  --pages 5 \
  --iterations 10 \
  --dashboard-url "http://localhost:3000/api/trpc"
```

**Pendant l'entraînement, vous verrez :**
- 📊 Barre de progression en temps réel
- 📈 Métriques de qualité (Coder A, Coder B, Arbitre)
- 💾 Tokens traités
- 🏆 Décisions de l'arbitre
- ✅ Sauvegarde automatique du modèle
- 📄 Export au format Ollama (GGUF)

**Commandes pendant l'entraînement :**
- `[P]` - Pause/Reprendre
- `[S]` - Arrêter proprement
- `[I]` - Afficher les infos détaillées

#### Mode full codage (scrape uniquement du code)
```bash
python orchestrator.py \
  --topic "C# optimization" \
  --pages 5 \
  --iterations 10 \
  --code-only
```

Le visualiseur affichera le progrès en direct avec les métriques d'apprentissage.

#### Entraînement rapide (test)
```bash
python orchestrator.py \
  --topic "Python basics" \
  --pages 2 \
  --iterations 3 \
  --no-dashboard
```

Durée : ~2 minutes

#### Sans intégration (mode standalone)
```bash
python orchestrator.py \
  --topic "Python optimization techniques" \
  --pages 3 \
  --iterations 5 \
  --no-dashboard
```

### 3. Options de ligne de commande
```
--topic TEXT              Sujet à scraper et entraîner (défaut: Unity game development)
--pages INT               Nombre de pages à scraper (défaut: 3)
--iterations INT          Nombre d'itérations d'entraînement (défaut: 3)
--dashboard-url TEXT      URL du dashboard UnityIAPro (défaut: http://localhost:3000/api/trpc)
--no-dashboard           Désactiver l'intégration avec le dashboard
--code-only              Scraper uniquement du code (GitHub, etc.) pour un modèle full codage
```

## 📚 Architecture

```
IAtrainer/
├── scraper.py                 # Web scraper gratuit
├── multi_agent_system.py      # Système multi-agents
├── trpc_client.py             # Client tRPC pour UnityIAPro
├── model_api.py               # API HTTP locale
├── orchestrator.py            # Orchestrateur principal
├── requirements.txt           # Dépendances Python
└── README.md                  # Cette documentation
```

## 📊 Mettre un modèle de base

**Avant de commencer l'entraînement, vous devez avoir un modèle de base.**

### Méthode 1 : Gestionnaire interactif (RECOMMANDÉ)

```bash
python model_manager.py
```

**Options disponibles :**

1. **Charger un modèle de base** - Charge un modèle existant dans `base_models/`
2. **Charger un modèle entraîné** - Charge un modèle que vous avez entraîné
3. **Créer un template** - Crée un fichier JSON pour un modèle personnalisé
4. **Télécharger Hugging Face** - Télécharge depuis Hugging Face
5. **Télécharger Ollama** - Télécharge depuis Ollama
6. **Afficher les infos** - Affiche les détails du modèle actuel

**Pour plus de détails, voir `COMPLETE_GUIDE.md`**

### Méthode 2 : Copier manuellement

Placez votre modèle dans le dossier `base_models/` :

```
base_models/
├── llama2-7b.gguf
├── mistral-7b.bin
└── custom-model.json
```

**Voir `MODELS_SETUP.md` pour les détails complets.**

## 📊 Visualisation en temps réel

Pendant l'entraînement, le système affiche un tableau de bord en direct avec :
- Barre de progression en pourcentage
- Métriques de qualité pour chaque agent
- Tokens traités
- Décisions de l'arbitre
- Commandes pour pause/arrêt

### Sauvegarder et arrêter l'entraînement

L'entraînement sauvegarde automatiquement :
1. Les données d'entraînement (JSON)
2. Le modèle au format Ollama (GGUF)
3. Les métriques et apprentissages

Fichiers générés dans le dossier `trained_models/`

## 📊 Documentation complète

**Voir `COMPLETE_GUIDE.md` pour :**
- Tutoriels détaillés
- Explication de chaque option
- Explication de chaque paramètre
- Exemples pratiques
- Dépannage

## 📊 Flux de Travail

### 1. Scraping
```
Topic → DuckDuckGo/GitHub/StackOverflow → Contenu + Exemples
```

### 2. Entraînement Multi-Agents
```
Tâche → Coder A (solution 1)
     → Coder B (solution 2)
     → Arbitre (comparaison)
     → Feedback (apprentissage)
```

### 3. Intégration Dashboard
```
Résultats → UnityIAPro Dashboard
         → Visualisation temps réel
         → Alertes automatiques
         → Historique complet
```

## 📡 API HTTP

### Mettre à jour la configuration
```bash
curl -X POST "http://localhost:8000/config/update?model_name=mistral&max_tokens=1024&temperature=0.8"
```

### Générer du code
```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Créer une fonction de tri optimisée",
    "max_tokens": 512,
    "temperature": 0.7
  }'
```

### Analyser du code
```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def my_function(): pass",
    "analysis_type": "quality"
  }'
```

### Comparer deux solutions
```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "code_a": "def solution_a(): pass",
    "code_b": "def solution_b(): pass"
  }'
```

### Entraîner le modèle
```bash
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Unity optimization",
    "content": "...",
    "code_examples": ["..."]
  }'
```

### Exporter le modèle pour Ollama
```bash
curl -X POST http://localhost:8000/export?format=gguf
```

Le modèle est exporté au format GGUF, directement utilisable avec Ollama :
```bash
# Charger le modèle dans Ollama
ollama create mon-modele -f Modelfile
ollama run mon-modele "Générer du code Unity"
```

## 🔗 Intégration avec UnityIAPro

### Prérequis
- UnityIAPro doit être en cours d'exécution sur `http://localhost:3000`

### Flux d'intégration
1. IAtrainer scrape les données
2. IAtrainer crée une session dans UnityIAPro
3. Chaque itération envoie les résultats au dashboard
4. Le dashboard affiche les conversations et décisions en temps réel
5. Les alertes sont créées automatiquement en cas d'erreur

### Exemple
```bash
# Terminal 1: Lancer UnityIAPro
cd ../UnityIAPro
pnpm dev

# Terminal 2: Lancer IAtrainer
cd ../IAtrainer
python orchestrator.py --topic "Advanced Python patterns"
```

Puis ouvrez le dashboard sur `http://localhost:3000` pour voir les résultats en temps réel.

## 📊 Résultats

Après une session d'entraînement, vous obtenez :

- **Conversations** : Tous les messages entre agents
- **Décisions** : Choix de l'arbitre avec justifications
- **Métriques** : Performance de chaque agent
- **Logs** : Historique complet des interactions
- **Modèle** : Modèle entraîné prêt à l'emploi avec Ollama

## 🛠️ Développement

### Ajouter un nouveau scraper
```python
def scrape_custom_source(self, query: str) -> List[Dict]:
    # Implémenter le scraping
    pass
```

### Améliorer les agents
```python
class CoderAgent:
    def generate_solution(self, task: str) -> Message:
        # Améliorer la génération
        pass
```

### Ajouter une nouvelle endpoint API
```python
@app.post("/custom-endpoint")
async def custom_endpoint(request: CustomRequest):
    # Implémenter la logique
    pass
```

## 📝 Logs

Les logs sont affichés en console avec timestamps et niveaux (INFO, WARNING, ERROR).

Exemple :
```
2024-01-15 10:30:45 - IAtrainer - INFO - SCRAPING: Unity game development
2024-01-15 10:30:46 - IAtrainer - INFO - Trouvé 5 résultats
2024-01-15 10:30:47 - IAtrainer - INFO - Itération 1: Coder A génère une solution
```

## 🚨 Dépannage

### Le dashboard ne reçoit pas les données
- Vérifier que UnityIAPro est en cours d'exécution sur `http://localhost:3000`
- Vérifier les logs pour les erreurs de connexion
- Utiliser `--no-dashboard` pour tester en mode standalone

### Le scraping est lent
- Réduire le nombre de pages avec `--pages 1`
- Les délais ont été supprimés pour aller au plus rapide

### L'API HTTP ne démarre pas
- Vérifier que le port 8000 est disponible
- Utiliser `--port 8001` pour changer le port

## 📄 License

MIT

## 🤝 Support

Pour toute question ou problème :
1. Vérifier la documentation
2. Consulter les logs
3. Ouvrir une issue sur GitHub

## 🎓 Apprentissage

Ce projet démontre :
- Web scraping gratuit sans API payante, au plus rapide
- Systèmes multi-agents collaboratifs
- Fine-tuning de modèles LLM libres
- Export au format Ollama (GGUF)
- Intégration temps réel avec dashboards
- Architecture modulaire et extensible
