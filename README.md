# IAtrainer - Système d'Entraînement Multi-Agents

Un système complet d'entraînement d'un modèle LLM spécialisé dans la génération de code Unity/Unreal, utilisant un système multi-agents (Coder A, Coder B, Arbitre) qui scrape automatiquement internet pour les données d'entraînement.

## 🎯 Fonctionnalités

### 🕷️ Web Scraping Gratuit
- **Scrape automatique** depuis DuckDuckGo, GitHub et Stack Overflow
- **Sans API payante** - utilise BeautifulSoup et requests
- **Extraction intelligente** de contenu et d'exemples de code
- **Respecte les serveurs** avec délais entre les requêtes

### 🤖 Système Multi-Agents
- **Coder A** : Génère une première solution
- **Coder B** : Génère une solution alternative
- **Arbitre** : Compare et choisit la meilleure approche
- **Feedback** : Les agents apprennent de chaque itération

### 📊 Entraînement du Modèle
- **Fine-tuning** automatique avec les données scrapées
- **Métriques** de performance en temps réel
- **Persistance** des décisions et apprentissages
- **Export** du modèle entraîné

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
- **Export** du modèle

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

## 🚀 Utilisation

### 1. Lancer l'API du modèle (optionnel)
```bash
python model_api.py
# L'API démarre sur http://localhost:8000
# Documentation: http://localhost:8000/docs
```

### 2. Lancer une session d'entraînement

#### Avec intégration UnityIAPro
```bash
python orchestrator.py \
  --topic "Unity game development" \
  --pages 5 \
  --iterations 10 \
  --dashboard-url "http://localhost:3000/api/trpc"
```

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

## 🔄 Flux de Travail

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
- **Modèle** : Modèle entraîné prêt à l'emploi

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
- Les délais entre requêtes sont intentionnels (respect des serveurs)

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
- Web scraping gratuit sans API payante
- Systèmes multi-agents collaboratifs
- Fine-tuning de modèles LLM
- Intégration temps réel avec dashboards
- Architecture modulaire et extensible
