# Guide Complet IAtrainer - Tutoriels et Paramètres

## 📚 Table des matières

1. [Démarrage rapide](#démarrage-rapide)
2. [Gestionnaire de modèles](#gestionnaire-de-modèles)
3. [Orchestrateur d'entraînement](#orchestrateur-dentraînement)
4. [API HTTP locale](#api-http-locale)
5. [Intégration UnityIAPro](#intégration-unityiapro)
6. [Paramètres détaillés](#paramètres-détaillés)
7. [Exemples pratiques](#exemples-pratiques)
8. [Dépannage](#dépannage)

---

## 🚀 Démarrage rapide

### Installation

```bash
# Cloner le repository
git clone https://github.com/minelaxie-sudo/IAtrainer.git
cd IAtrainer

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Première utilisation (5 minutes)

```bash
# 1. Télécharger un modèle de base
python model_manager.py
# Choisir option 4 → Hugging Face
# Entrer: gpt2
# Entrer: gpt2-base

# 2. Lancer l'entraînement
python orchestrator.py --topic "Python basics" --iterations 5

# 3. Voir le tableau de bord en temps réel
# (Les métriques s'affichent automatiquement)

# 4. Modèle entraîné sauvegardé dans trained_models/
```

---

## 🤖 Gestionnaire de modèles

### Commande

```bash
python model_manager.py
```

### Options expliquées

#### **Option 1 : Charger un modèle de base**

**À quoi ça sert :** Charge un modèle de base existant pour l'utiliser comme point de départ de l'entraînement.

**Quand l'utiliser :**
- Vous avez déjà un modèle téléchargé dans `base_models/`
- Vous voulez continuer l'entraînement d'un modèle existant

**Exemple :**
```
Choisir: 1
Affichage des modèles disponibles:
  1. llama2-7b.gguf (3500 MB)
  2. mistral-7b.bin (4200 MB)
Choisir: 1
✓ Modèle de base chargé: llama2-7b.gguf
```

---

#### **Option 2 : Charger un modèle entraîné**

**À quoi ça sert :** Charge un modèle que vous avez déjà entraîné pour continuer l'entraînement ou l'utiliser.

**Quand l'utiliser :**
- Vous avez un modèle dans `trained_models/`
- Vous voulez affiner un modèle existant
- Vous voulez utiliser un modèle entraîné avec l'API

**Exemple :**
```
Choisir: 2
Affichage des modèles entraînés:
  1. llama2-unity_20240115_103045.json (250 KB)
Choisir: 1
✓ Modèle entraîné chargé: llama2-unity_20240115_103045.json
```

---

#### **Option 3 : Créer un template de modèle de base**

**À quoi ça sert :** Crée un fichier JSON template pour définir un modèle personnalisé sans le télécharger.

**Quand l'utiliser :**
- Vous avez un modèle personnalisé avec une architecture spéciale
- Vous voulez définir les paramètres d'entraînement avant de commencer
- Vous voulez documenter votre modèle

**Paramètres du template :**
```json
{
  "name": "mon-modele",
  "type": "base_model",
  "version": "1.0.0",
  "architecture": "transformer",
  "parameters": {
    "vocab_size": 32000,        // Taille du vocabulaire
    "hidden_size": 768,         // Taille des couches cachées
    "num_layers": 12,           // Nombre de couches
    "num_heads": 12             // Nombre de têtes d'attention
  },
  "training_config": {
    "learning_rate": 1e-4,      // Vitesse d'apprentissage
    "batch_size": 32,           // Taille des batches
    "epochs": 3,                // Nombre d'épochs
    "optimizer": "adam"         // Optimiseur
  }
}
```

**Exemple :**
```
Choisir: 3
Nom du modèle: mon-modele-custom
✓ Template créé: base_models/mon-modele-custom.json
```

---

#### **Option 4 : Télécharger depuis Hugging Face**

**À quoi ça sert :** Télécharge automatiquement un modèle depuis Hugging Face (la plus grande plateforme de modèles open-source).

**Quand l'utiliser :**
- Vous voulez un modèle de base populaire
- Vous voulez un modèle spécialisé (codage, chat, etc.)
- Vous n'avez pas le modèle localement

**Modèles recommandés :**
```
Petits (rapides, peu de RAM):
- gpt2                          (124M, 500MB)
- facebook/opt-350m             (350M, 1.3GB)
- distilbert-base-uncased       (66M, 250MB)

Moyens (équilibrés):
- meta-llama/Llama-2-7b         (7B, 3.5GB)
- mistralai/Mistral-7B          (7B, 4.2GB)
- EleutherAI/pythia-6.9b        (6.9B, 3.2GB)

Grands (puissants, beaucoup de RAM):
- meta-llama/Llama-2-13b        (13B, 7GB)
- bigcode/starcoder             (15B, 8GB)
```

**Exemple :**
```
Choisir: 4
ID du modèle Hugging Face: gpt2
Nom local: gpt2-base
Téléchargement depuis Hugging Face...
✓ Modèle téléchargé: base_models/gpt2-base/
```

---

#### **Option 5 : Télécharger depuis Ollama**

**À quoi ça sert :** Télécharge un modèle depuis Ollama (plateforme locale optimisée pour les modèles GGUF).

**Quand l'utiliser :**
- Vous avez Ollama installé
- Vous voulez des modèles optimisés et compressés
- Vous voulez des modèles spécialisés (code, chat)

**Modèles disponibles :**
```
Populaires:
- llama2                        (7B, optimisé)
- mistral                       (7B, rapide)
- neural-chat                   (7B, chat)
- orca-mini                     (3B, petit)

Spécialisés:
- codellama                     (Code)
- dolphin-mixtral               (Chat amélioré)
- starling-lm                   (Instruction-following)
```

**Exemple :**
```
Choisir: 5
ID du modèle Ollama: llama2
Nom local: llama2-local
Téléchargement avec Ollama...
✓ Modèle téléchargé avec Ollama: llama2
```

---

#### **Option 6 : Afficher les infos du modèle actuel**

**À quoi ça sert :** Affiche les détails du modèle actuellement chargé.

**Informations affichées :**
- Nom du modèle
- Chemin du fichier
- Type (base ou entraîné)
- Heure de chargement
- Taille du fichier

**Exemple :**
```
Choisir: 6
📋 Modèle actuel:
  name: llama2-7b.gguf
  path: base_models/llama2-7b.gguf
  loaded_at: 2024-01-15T10:30:45
  type: base
  size_mb: 3500
```

---

## 🎓 Orchestrateur d'entraînement

### Commande

```bash
python orchestrator.py [OPTIONS]
```

### Paramètres expliqués

#### **--topic** (Requis)

**À quoi ça sert :** Définit le sujet sur lequel le modèle sera entraîné.

**Format :** Texte libre, n'importe quel sujet

**Exemples :**
```bash
--topic "Python optimization"
--topic "C# game development"
--topic "Web development with React"
--topic "Machine learning basics"
```

**Impact :**
- Le scraper cherchera du contenu sur ce sujet
- Les agents généreront du code lié à ce sujet
- Le modèle sera spécialisé dans ce domaine

---

#### **--pages** (Optionnel, défaut: 5)

**À quoi ça sert :** Nombre de pages web à scraper pour collecter les données d'entraînement.

**Valeurs recommandées :**
```
1-3 pages   → Entraînement rapide (5-10 min), données limitées
5-10 pages  → Équilibre qualité/temps (15-30 min)
10+ pages   → Données riches (30+ min), meilleure qualité
```

**Exemples :**
```bash
--pages 3    # Entraînement rapide
--pages 5    # Recommandé
--pages 20   # Entraînement complet
```

**Impact :**
- Plus de pages = plus de données = meilleur modèle
- Plus de pages = plus de temps d'entraînement

---

#### **--iterations** (Optionnel, défaut: 10)

**À quoi ça sert :** Nombre d'itérations d'entraînement (cycles Coder A/B + Arbitre).

**Valeurs recommandées :**
```
1-3 itérations    → Test rapide (1-2 min)
5-10 itérations   → Entraînement normal (5-15 min)
20+ itérations    → Entraînement approfondi (30+ min)
```

**Exemples :**
```bash
--iterations 3    # Test rapide
--iterations 10   # Recommandé
--iterations 50   # Entraînement long
```

**Impact :**
- Plus d'itérations = modèle plus raffiné
- Plus d'itérations = plus de temps
- Chaque itération améliore le modèle

---

#### **--code-only** (Optionnel, défaut: False)

**À quoi ça sert :** Scrape UNIQUEMENT du code (pas de texte), crée un modèle spécialisé en génération de code.

**Quand l'utiliser :**
- Vous voulez un modèle pour générer du code
- Vous ne voulez pas de texte explicatif
- Vous voulez un modèle "full codage"

**Exemples :**
```bash
--code-only              # Active le mode code-only
# Sans ce flag, scrape du texte ET du code
```

**Impact :**
- Données : uniquement du code
- Modèle spécialisé en codage
- Meilleure qualité pour la génération de code

---

#### **--dashboard-url** (Optionnel, défaut: http://localhost:3000/api/trpc)

**À quoi ça sert :** URL du dashboard UnityIAPro pour envoyer les données en temps réel.

**Quand l'utiliser :**
- Vous avez UnityIAPro en cours d'exécution
- Vous voulez visualiser l'entraînement en direct
- Vous voulez enregistrer les données dans la base de données

**Exemples :**
```bash
--dashboard-url "http://localhost:3000/api/trpc"    # Local
--dashboard-url "http://192.168.1.100:3000/api/trpc" # Réseau
```

**Impact :**
- Avec URL : données envoyées au dashboard
- Sans URL : entraînement local uniquement

---

#### **--no-dashboard** (Optionnel, défaut: False)

**À quoi ça sert :** Désactive l'envoi des données au dashboard (mode standalone).

**Quand l'utiliser :**
- UnityIAPro n'est pas lancé
- Vous voulez un entraînement rapide sans overhead
- Vous voulez tester localement

**Exemples :**
```bash
--no-dashboard           # Mode standalone
```

**Impact :**
- Pas d'envoi de données au dashboard
- Entraînement plus rapide
- Données sauvegardées localement uniquement

---

### Exemples d'utilisation

#### **Exemple 1 : Entraînement rapide (test)**
```bash
python orchestrator.py \
  --topic "Python basics" \
  --pages 3 \
  --iterations 5 \
  --no-dashboard
```
**Résultat :** Entraînement en ~5 minutes, données limitées

---

#### **Exemple 2 : Entraînement standard (recommandé)**
```bash
python orchestrator.py \
  --topic "Unity game development" \
  --pages 5 \
  --iterations 10 \
  --dashboard-url "http://localhost:3000/api/trpc"
```
**Résultat :** Entraînement en ~15 minutes, données équilibrées, visualisation en direct

---

#### **Exemple 3 : Modèle full codage**
```bash
python orchestrator.py \
  --topic "C# optimization" \
  --pages 10 \
  --iterations 20 \
  --code-only
```
**Résultat :** Modèle spécialisé en code C#, entraînement complet

---

#### **Exemple 4 : Entraînement approfondi**
```bash
python orchestrator.py \
  --topic "Web development" \
  --pages 20 \
  --iterations 50 \
  --dashboard-url "http://localhost:3000/api/trpc"
```
**Résultat :** Modèle très raffiné, entraînement long (~1 heure)

---

## 🌐 API HTTP locale

### Commande

```bash
python model_api.py
```

### Configuration interactive

Menu interactif :
```
OPTIONS DISPONIBLES:
1. Voir la configuration actuelle
2. Changer le nom du modèle
3. Changer le nombre de tokens par défaut
4. Changer la température par défaut
5. Changer le Top-P par défaut
6. Changer le host
7. Changer le port
8. Démarrer l'API
9. Quitter
```

### Paramètres expliqués

#### **Nom du modèle**

**À quoi ça sert :** Identifie le modèle utilisé par l'API.

**Exemples :**
```
llama2-unity
mistral-7b
gpt2-base
custom-model
```

---

#### **Tokens par défaut**

**À quoi ça sert :** Nombre maximum de tokens générés par défaut.

**Valeurs recommandées :**
```
256    → Réponses courtes
512    → Réponses moyennes (défaut)
1024   → Réponses longues
2048   → Réponses très longues
```

**Impact :**
- Plus de tokens = réponses plus longues
- Plus de tokens = plus de temps de génération

---

#### **Température**

**À quoi ça sert :** Contrôle la créativité du modèle.

**Valeurs :**
```
0.0    → Déterministe (toujours la même réponse)
0.5    → Équilibré
0.7    → Recommandé (créatif mais cohérent)
1.0    → Très créatif
2.0    → Très aléatoire
```

**Impact :**
- Basse température = réponses prévisibles
- Haute température = réponses variées

---

#### **Top-P**

**À quoi ça sert :** Contrôle la diversité des tokens générés.

**Valeurs :**
```
0.5    → Réponses conservatrices
0.9    → Recommandé (équilibré)
1.0    → Toute la distribution
```

**Impact :**
- Bas Top-P = réponses plus cohérentes
- Haut Top-P = réponses plus variées

---

#### **Host**

**À quoi ça sert :** Adresse IP où l'API écoute.

**Valeurs :**
```
127.0.0.1    → Localhost uniquement (sécurisé)
0.0.0.0      → Toutes les interfaces (réseau)
192.168.1.x  → IP spécifique
```

---

#### **Port**

**À quoi ça sert :** Port TCP pour accéder à l'API.

**Valeurs recommandées :**
```
8000   → Défaut
8001   → Alternative
5000   → Flask standard
3000   → Node.js standard
```

---

### Endpoints API

#### **GET /health**

Vérifier l'état de l'API.

```bash
curl http://localhost:8000/health
```

Réponse :
```json
{
  "status": "healthy",
  "model_loaded": true,
  "model": "llama2-unity",
  "training_iterations": 10
}
```

---

#### **POST /generate**

Générer du code.

```bash
curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Créer une fonction de tri",
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9
  }'
```

Paramètres :
- `prompt` : Texte d'entrée
- `max_tokens` : Nombre max de tokens
- `temperature` : Créativité (0-2)
- `top_p` : Diversité (0-1)

---

#### **POST /analyze**

Analyser du code.

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{
    "code": "def hello(): print(\"Hello\")",
    "analysis_type": "quality"
  }'
```

Types d'analyse :
- `quality` : Qualité générale
- `security` : Sécurité
- `performance` : Performance
- `style` : Style de code

---

#### **POST /compare**

Comparer deux solutions.

```bash
curl -X POST http://localhost:8000/compare \
  -H "Content-Type: application/json" \
  -d '{
    "code_a": "def sort1(arr): return sorted(arr)",
    "code_b": "def sort2(arr): ...",
  }'
```

Résultat :
- `winner` : "a", "b", ou "tie"
- `score_a` : Score de la solution A
- `score_b` : Score de la solution B

---

#### **POST /train**

Entraîner le modèle.

```bash
curl -X POST http://localhost:8000/train \
  -H "Content-Type: application/json" \
  -d '{
    "topic": "Python optimization",
    "content": "...",
    "code_examples": ["def func1(): ...", "def func2(): ..."]
  }'
```

---

#### **POST /export**

Exporter le modèle.

```bash
curl -X POST http://localhost:8000/export?format=gguf
```

Formats :
- `json` : Format JSON
- `gguf` : Format Ollama (GGUF)

---

## 🔗 Intégration UnityIAPro

### Démarrage

1. **Lancer UnityIAPro**
```bash
cd ../UnityIAPro
pnpm dev
```

2. **Lancer IAtrainer avec dashboard**
```bash
python orchestrator.py \
  --topic "Unity development" \
  --pages 5 \
  --iterations 10 \
  --dashboard-url "http://localhost:3000/api/trpc"
```

3. **Voir les données en direct**
- Ouvrir http://localhost:3000
- Aller à "Conversations" pour voir les messages
- Aller à "Code Comparison" pour comparer les solutions
- Aller à "Dashboard" pour voir les métriques

---

## 📊 Paramètres détaillés

### Scraper

| Paramètre | Valeur | Impact |
|-----------|--------|--------|
| `--pages` | 1-50 | Nombre de pages à scraper |
| `--code-only` | True/False | Scraper uniquement du code |

### Entraînement

| Paramètre | Valeur | Impact |
|-----------|--------|--------|
| `--iterations` | 1-100 | Nombre d'itérations |
| `--topic` | Texte | Sujet d'entraînement |

### API

| Paramètre | Valeur | Impact |
|-----------|--------|--------|
| `max_tokens` | 256-2048 | Longueur des réponses |
| `temperature` | 0.0-2.0 | Créativité |
| `top_p` | 0.0-1.0 | Diversité |

---

## 💡 Exemples pratiques

### Cas 1 : Créer un modèle pour Unity

```bash
# 1. Télécharger un modèle
python model_manager.py
# Option 4 → mistralai/Mistral-7B → mistral-unity

# 2. Entraîner sur Unity
python orchestrator.py \
  --topic "Unity C# scripting" \
  --pages 10 \
  --iterations 20 \
  --code-only

# 3. Résultat
# trained_models/mistral-unity_*.json
# trained_models/mistral-unity_*.gguf.json
```

---

### Cas 2 : Entraînement rapide pour tester

```bash
python orchestrator.py \
  --topic "Python basics" \
  --pages 2 \
  --iterations 3 \
  --no-dashboard
```

**Durée :** ~2 minutes

---

### Cas 3 : Modèle full codage

```bash
python orchestrator.py \
  --topic "Web development" \
  --pages 15 \
  --iterations 30 \
  --code-only
```

**Résultat :** Modèle spécialisé en code web

---

## 🐛 Dépannage

### "Modèle non trouvé"

```
Solution:
1. Vérifier que le fichier est dans base_models/
2. Vérifier l'extension (.gguf, .bin, .json)
3. Utiliser model_manager.py pour télécharger
```

### "Erreur de scraping"

```
Solution:
1. Vérifier la connexion internet
2. Essayer avec --pages 2
3. Vérifier que le sujet existe
```

### "Pas assez de RAM"

```
Solution:
1. Utiliser un modèle plus petit (gpt2, opt-350m)
2. Réduire --pages et --iterations
3. Fermer les autres applications
```

### "API ne démarre pas"

```
Solution:
1. Vérifier le port (8000 par défaut)
2. Vérifier que rien n'occupe le port
3. Changer le port dans model_api.py
```

---

## 📚 Ressources

- [Hugging Face Models](https://huggingface.co/models)
- [Ollama](https://ollama.ai)
- [Transformers Documentation](https://huggingface.co/docs/transformers)
- [GGUF Format](https://github.com/ggerganov/ggml)
