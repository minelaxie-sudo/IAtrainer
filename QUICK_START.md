# Tutoriel Pas à Pas - IAtrainer

## 📁 Structure des dossiers

Quand vous clonez IAtrainer, voici ce que vous avez :

```
IAtrainer/
├── base_models/              ← 🔴 C'EST ICI QUE VOUS METTEZ LES MODÈLES
│   ├── (dossier vide au départ)
│   └── (vous y mettrez vos modèles)
│
├── trained_models/           ← Les modèles après entraînement (créé auto)
│   ├── (vide au départ)
│   └── (rempli après entraînement)
│
├── model_manager.py          ← Gestionnaire de modèles
├── orchestrator.py           ← Entraîneur principal
├── model_api.py              ← API HTTP
├── scraper.py                ← Web scraper
├── multi_agent_system.py     ← Système multi-agents
├── training_visualizer.py    ← Visualiseur
├── trpc_client.py            ← Client tRPC
├── requirements.txt          ← Dépendances
├── README.md                 ← Vue d'ensemble
├── COMPLETE_GUIDE.md         ← Guide complet
├── MODELS_SETUP.md           ← Configuration modèles
└── QUICK_START.md            ← CE FICHIER
```

---

## 🎯 Étape 1 : Installation (5 minutes)

### Ouvrir le terminal/PowerShell

**Windows :**
- Appuyez sur `Win + R`
- Tapez `cmd` ou `powershell`
- Appuyez sur Entrée

**Mac/Linux :**
- Ouvrez Terminal

### Cloner le projet

```bash
git clone https://github.com/minelaxie-sudo/IAtrainer.git
cd IAtrainer
```

### Créer un environnement virtuel

**Windows :**
```bash
python -m venv venv
venv\Scripts\activate
```

**Mac/Linux :**
```bash
python -m venv venv
source venv/bin/activate
```

### Installer les dépendances

```bash
pip install -r requirements.txt
```

✅ **Vous êtes prêt !**

---

## 🤖 Étape 2 : Télécharger un modèle (5-10 minutes)

### Lancer le gestionnaire de modèles

```bash
python model_manager.py
```

Vous verrez :
```
================================================================================
GESTIONNAIRE DE MODÈLES
================================================================================

📦 MODÈLES DE BASE:
  Aucun modèle de base trouvé

✅ MODÈLES ENTRAÎNÉS:
  Aucun modèle entraîné trouvé

------------------------------------------------------------------------
OPTIONS:
1. Charger un modèle de base
2. Charger un modèle entraîné
3. Créer un template de modèle de base
4. Télécharger un modèle depuis Hugging Face
5. Télécharger un modèle depuis Ollama
6. Afficher les infos du modèle actuel
7. Quitter

Choisissez une option (1-7): 
```

### Taper "4" pour télécharger depuis Hugging Face

```
Choisissez une option (1-7): 4
```

Vous verrez :
```
ID du modèle Hugging Face: 
```

### Taper le modèle à télécharger

**Pour débutants (RECOMMANDÉ) :**
```
ID du modèle Hugging Face: gpt2
```

**Autres options :**
```
ID du modèle Hugging Face: facebook/opt-350m
ID du modèle Hugging Face: mistralai/Mistral-7B
```

### Taper le nom local

```
Nom local du modèle: mon-modele
```

### Attendre le téléchargement

```
Téléchargement depuis Hugging Face...
✓ Modèle téléchargé: base_models/mon-modele/
```

✅ **Le modèle est maintenant dans `base_models/mon-modele/`**

### Quitter le gestionnaire

```
Choisissez une option (1-7): 7
Au revoir!
```

---

## 🎓 Étape 3 : Lancer l'entraînement (10-30 minutes)

### Ouvrir un NOUVEAU terminal

⚠️ **Important :** Ouvrez un nouveau terminal/PowerShell (ne fermez pas l'ancien)

### Aller dans le dossier IAtrainer

```bash
cd IAtrainer
```

### Activer l'environnement virtuel

**Windows :**
```bash
venv\Scripts\activate
```

**Mac/Linux :**
```bash
source venv/bin/activate
```

### Lancer l'entraînement

**Commande simple (POUR DÉBUTER) :**
```bash
python orchestrator.py --topic "Python basics"
```

**Commande avec plus d'options :**
```bash
python orchestrator.py --topic "Python basics" --pages 5 --iterations 10
```

### Comprendre la commande

```
python orchestrator.py --topic "Python basics" --pages 5 --iterations 10
│      │              │     │                 │      │            │
│      │              │     │                 │      │            └─ Nombre d'itérations
│      │              │     │                 │      └─ Nombre de pages à scraper
│      │              │     │                 └─ Paramètre
│      │              │     └─ Valeur du paramètre
│      │              └─ Paramètre (REQUIS)
│      └─ Fichier Python à lancer
└─ Commande pour lancer Python
```

### Pendant l'entraînement

Vous verrez :
```
================================================================================
🤖 TABLEAU DE BORD D'ENTRAÎNEMENT - IAtrainer
================================================================================
Modèle: llama2-unity
Démarrage: 2024-01-15T10:30:45.123456
================================================================================

[Itération 1/10]
Progress: |█░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░| 10%

📊 Dernière itération:
  ✓ Coder A qualité: 78.50%
  ✓ Coder B qualité: 72.30%
  ✓ Arbitre qualité: 81.20%
  ✓ Tokens traités: 245
  ✓ Décision: Coder A

📈 Métriques moyennes:
  • Coder A: 75.40%
  • Coder B: 70.20%
  • Arbitre: 78.50%
  • Total tokens: 1245

💡 Commandes:
  [P] Pause/Reprendre  [S] Arrêter  [I] Infos détaillées
```

✅ **C'est normal ! Le modèle apprend !**

### Attendre la fin

À la fin, vous verrez :
```
================================================================================
📋 RÉSUMÉ DE L'ENTRAÎNEMENT
================================================================================

Modèle: llama2-unity
Itérations complétées: 10/10
Tokens traités: 5432

📊 Qualité moyenne:
  • Coder A: 75.40%
  • Coder B: 70.20%
  • Arbitre: 78.50%

✅ Modèle sauvegardé: trained_models/llama2-unity_20240115_103045.json
✅ Modèle exporté pour Ollama: trained_models/llama2-unity_20240115_103045.gguf.json
```

✅ **Entraînement terminé !**

---

## 📊 Étape 4 : Voir les résultats

### Fichiers créés

Allez dans le dossier `trained_models/` :

```
trained_models/
├── llama2-unity_20240115_103045.json       ← Données d'entraînement
└── llama2-unity_20240115_103045.gguf.json  ← Modèle pour Ollama
```

### Utiliser le modèle

**Avec Ollama :**
```bash
ollama create mon-modele -f Modelfile
ollama run mon-modele "Générer une fonction de tri"
```

**Avec l'API :**
```bash
python model_api.py
# Choisir le modèle entraîné
# Utiliser http://localhost:8000/docs
```

---

## 🎯 Résumé des commandes

### Terminal 1 : Télécharger un modèle

```bash
# 1. Aller dans le dossier
cd IAtrainer

# 2. Activer l'environnement
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 3. Lancer le gestionnaire
python model_manager.py

# 4. Choisir option 4 (Hugging Face)
# 5. Taper "gpt2"
# 6. Taper "mon-modele"
# 7. Attendre le téléchargement
# 8. Quitter (option 7)
```

### Terminal 2 : Lancer l'entraînement

```bash
# 1. Ouvrir un NOUVEAU terminal

# 2. Aller dans le dossier
cd IAtrainer

# 3. Activer l'environnement
venv\Scripts\activate          # Windows
source venv/bin/activate       # Mac/Linux

# 4. Lancer l'entraînement
python orchestrator.py --topic "Python basics"

# 5. Attendre la fin
```

---

## 🔧 Paramètres expliqués simplement

### --topic (REQUIS)

**Qu'est-ce que c'est ?** Le sujet sur lequel entraîner le modèle

**Exemples :**
```bash
--topic "Python"
--topic "Unity development"
--topic "Web development"
--topic "Machine learning"
```

**Impact :** Le modèle sera spécialisé dans ce domaine

---

### --pages (optionnel, défaut: 5)

**Qu'est-ce que c'est ?** Nombre de pages web à scraper

**Exemples :**
```bash
--pages 2     # Rapide (2-3 min)
--pages 5     # Normal (5-10 min)
--pages 20    # Complet (20-30 min)
```

**Impact :** Plus de pages = meilleur modèle = plus de temps

---

### --iterations (optionnel, défaut: 10)

**Qu'est-ce que c'est ?** Nombre de cycles d'entraînement

**Exemples :**
```bash
--iterations 3   # Rapide
--iterations 10  # Normal
--iterations 50  # Long
```

**Impact :** Plus d'itérations = modèle plus raffiné = plus de temps

---

### --code-only (optionnel)

**Qu'est-ce que c'est ?** Scraper UNIQUEMENT du code (pas de texte)

**Exemples :**
```bash
python orchestrator.py --topic "C#" --code-only
```

**Impact :** Modèle spécialisé en génération de code

---

### --no-dashboard (optionnel)

**Qu'est-ce que c'est ?** Désactiver l'envoi de données à UnityIAPro

**Exemples :**
```bash
python orchestrator.py --topic "Python" --no-dashboard
```

**Impact :** Entraînement plus rapide (pas de communication réseau)

---

## 💡 Exemples complets

### Exemple 1 : Entraînement rapide (POUR DÉBUTER)

```bash
python orchestrator.py --topic "Python basics" --pages 2 --iterations 3
```

**Durée :** ~2 minutes
**Résultat :** Modèle simple pour tester

---

### Exemple 2 : Entraînement normal (RECOMMANDÉ)

```bash
python orchestrator.py --topic "Unity development" --pages 5 --iterations 10
```

**Durée :** ~10 minutes
**Résultat :** Bon modèle équilibré

---

### Exemple 3 : Modèle full codage

```bash
python orchestrator.py --topic "C# optimization" --pages 10 --iterations 20 --code-only
```

**Durée :** ~20 minutes
**Résultat :** Modèle spécialisé en code C#

---

### Exemple 4 : Avec UnityIAPro

```bash
python orchestrator.py --topic "Web development" --pages 5 --iterations 10 --dashboard-url "http://localhost:3000/api/trpc"
```

**Durée :** ~10 minutes
**Résultat :** Modèle + visualisation en direct

---

## ❌ Erreurs courantes

### Erreur : "Modèle non trouvé"

**Cause :** Vous n'avez pas téléchargé de modèle

**Solution :**
```bash
python model_manager.py
# Choisir option 4
# Télécharger gpt2
```

---

### Erreur : "Commande non reconnue"

**Cause :** Vous n'êtes pas dans le bon dossier

**Solution :**
```bash
cd IAtrainer
python orchestrator.py --topic "Python"
```

---

### Erreur : "Python non trouvé"

**Cause :** Python n'est pas installé ou pas dans PATH

**Solution :**
- Installer Python depuis python.org
- Redémarrer le terminal

---

### Erreur : "Pas assez de RAM"

**Cause :** Le modèle est trop gros

**Solution :**
```bash
# Utiliser un modèle plus petit
python model_manager.py
# Choisir gpt2 au lieu de Llama
```

---

## 📚 Prochaines étapes

1. **Lancer l'API :** `python model_api.py`
2. **Utiliser le modèle :** http://localhost:8000/docs
3. **Intégrer avec UnityIAPro :** Voir COMPLETE_GUIDE.md
4. **Améliorer le modèle :** Entraîner avec plus de données

---

## ❓ Questions fréquentes

**Q : Où mettre les modèles ?**
A : Dans le dossier `base_models/` (créé automatiquement)

**Q : Où trouver les modèles entraînés ?**
A : Dans le dossier `trained_models/` (créé automatiquement)

**Q : Combien de temps ça prend ?**
A : 2-30 minutes selon les paramètres

**Q : Puis-je arrêter l'entraînement ?**
A : Oui, appuyez sur CTRL+C (les données sont sauvegardées)

**Q : Puis-je continuer un entraînement ?**
A : Oui, charger le modèle entraîné avec le gestionnaire

---

## 🎉 Vous êtes prêt !

Vous avez maintenant tout ce qu'il faut pour :
1. ✅ Télécharger un modèle
2. ✅ Entraîner le modèle
3. ✅ Voir les résultats
4. ✅ Utiliser le modèle

Commencez par l'Étape 1 ! 🚀
