# Configuration des Modèles - IAtrainer

## 📁 Structure des dossiers

```
IAtrainer/
├── base_models/          ← Modèles de base à entraîner
│   ├── llama2-unity.bin
│   ├── mistral-7b.gguf
│   └── custom-model.json
│
├── trained_models/       ← Modèles après entraînement
│   ├── llama2-unity_20240115_103045.json
│   └── llama2-unity_20240115_103045.gguf.json
│
└── model_manager.py      ← Gestionnaire de modèles
```

## 🚀 Mettre un modèle de base

### Option 1 : Utiliser le gestionnaire interactif (RECOMMANDÉ)

```bash
python model_manager.py
```

Menu interactif :
```
OPTIONS:
1. Charger un modèle de base
2. Charger un modèle entraîné
3. Créer un template de modèle de base
4. Télécharger un modèle depuis Hugging Face
5. Télécharger un modèle depuis Ollama
6. Afficher les infos du modèle actuel
7. Quitter
```

### Option 2 : Télécharger depuis Hugging Face

```bash
python model_manager.py
# Choisir l'option 4
# Entrer: meta-llama/Llama-2-7b
# Entrer: llama2-7b
```

**Modèles populaires :**
- `meta-llama/Llama-2-7b` - Llama 2 (7B)
- `mistralai/Mistral-7B` - Mistral (7B)
- `gpt2` - GPT-2 (petit, rapide)
- `facebook/opt-350m` - OPT (350M)

### Option 3 : Télécharger depuis Ollama

```bash
python model_manager.py
# Choisir l'option 5
# Entrer: llama2
# Entrer: llama2-local
```

**Modèles disponibles :**
- `llama2` - Llama 2
- `mistral` - Mistral
- `neural-chat` - Neural Chat
- `orca-mini` - Orca Mini

### Option 4 : Copier manuellement

1. Téléchargez le modèle depuis [Hugging Face](https://huggingface.co/models)
2. Placez-le dans le dossier `base_models/`
3. Renommez-le avec une extension claire (`.gguf`, `.bin`, `.json`)

Exemple :
```bash
# Télécharger depuis Hugging Face
git clone https://huggingface.co/meta-llama/Llama-2-7b

# Copier dans IAtrainer
cp -r Llama-2-7b/* IAtrainer/base_models/llama2-7b/
```

## 📝 Créer un template de modèle

Si vous avez un modèle personnalisé :

```bash
python model_manager.py
# Choisir l'option 3
# Entrer: mon-modele-custom
```

Cela crée `base_models/mon-modele-custom.json` :
```json
{
  "name": "mon-modele-custom",
  "type": "base_model",
  "created_at": "2024-01-15T10:30:45",
  "version": "1.0.0",
  "architecture": "transformer",
  "parameters": {
    "vocab_size": 32000,
    "hidden_size": 768,
    "num_layers": 12,
    "num_heads": 12
  }
}
```

## 🔍 Lister les modèles disponibles

```bash
python model_manager.py
# Affiche automatiquement les modèles de base et entraînés
```

Ou en Python :
```python
from model_manager import ModelManager

manager = ModelManager()

# Lister les modèles de base
base_models = manager.list_base_models()
for model in base_models:
    print(f"{model['name']} - {model['size_mb']} MB")

# Lister les modèles entraînés
trained_models = manager.list_trained_models()
for model in trained_models:
    print(f"{model['name']} - {model['size_mb']} MB")
```

## 🎯 Utiliser un modèle pour l'entraînement

### Dans orchestrator.py

```python
from model_manager import ModelManager

manager = ModelManager()

# Charger un modèle de base
manager.load_base_model("llama2-7b.bin")

# Récupérer le modèle actuel
current_model = manager.get_current_model()
print(f"Modèle chargé: {current_model['name']}")

# Utiliser pour l'entraînement
orchestrator = IAtrainerOrchestrator(model_name=current_model['name'])
result = orchestrator.train(topic="Unity development", num_iterations=10)
```

## 💾 Format des modèles supportés

| Format | Extension | Source | Notes |
|--------|-----------|--------|-------|
| GGUF | `.gguf` | Ollama, llama.cpp | Optimisé, recommandé |
| PyTorch | `.bin` | Hugging Face | Format standard |
| JSON | `.json` | Custom | Template ou metadata |
| SafeTensors | `.safetensors` | Hugging Face | Format sécurisé |

## ⚙️ Configuration du modèle

Chaque modèle peut avoir une configuration personnalisée :

```json
{
  "name": "llama2-7b",
  "training_config": {
    "learning_rate": 1e-4,
    "batch_size": 32,
    "epochs": 3,
    "optimizer": "adam",
    "warmup_steps": 500,
    "max_grad_norm": 1.0
  },
  "inference_config": {
    "max_tokens": 512,
    "temperature": 0.7,
    "top_p": 0.9,
    "top_k": 40
  }
}
```

## 🚨 Dépannage

### "Modèle non trouvé"
- Vérifiez que le fichier est dans `base_models/`
- Vérifiez l'extension du fichier (`.gguf`, `.bin`, `.json`)

### "Erreur lors du téléchargement"
- Vérifiez votre connexion internet
- Vérifiez que le modèle existe sur Hugging Face
- Essayez avec un modèle plus petit d'abord

### "Pas assez d'espace disque"
- Les modèles peuvent faire plusieurs GB
- Vérifiez l'espace disponible : `df -h`
- Supprimez les anciens modèles si nécessaire

## 📚 Ressources

- [Hugging Face Models](https://huggingface.co/models)
- [Ollama Models](https://ollama.ai/library)
- [GGUF Format](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
- [Llama 2 Paper](https://arxiv.org/abs/2307.09288)
