"""
Script d'initialisation des modèles réels.
Télécharge les vrais modèles depuis Hugging Face.
"""

import os
import json
import subprocess
import sys
from pathlib import Path


def install_huggingface_hub():
    """Installe huggingface_hub si nécessaire."""
    try:
        import huggingface_hub
        return True
    except ImportError:
        print("📦 Installation de huggingface_hub...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "huggingface_hub", "-q"])
            print("✓ huggingface_hub installé")
            return True
        except Exception as e:
            print(f"✗ Erreur lors de l'installation: {e}")
            return False


def download_model(model_id: str, local_name: str):
    """Télécharge un modèle depuis Hugging Face."""
    from huggingface_hub import snapshot_download
    
    base_models_dir = "base_models"
    if not os.path.exists(base_models_dir):
        os.makedirs(base_models_dir)
    
    model_path = os.path.join(base_models_dir, local_name)
    
    # Vérifier si le modèle existe déjà
    if os.path.exists(model_path) and len(os.listdir(model_path)) > 0:
        print(f"✓ {local_name} existe déjà")
        return model_path
    
    print(f"\n📥 Téléchargement de {model_id}...")
    print(f"   Destination: {model_path}")
    
    try:
        downloaded_path = snapshot_download(
            repo_id=model_id,
            local_dir=model_path,
            local_dir_use_symlinks=False,
        )
        print(f"✓ {local_name} téléchargé avec succès")
        
        # Afficher les infos du modèle
        config_path = os.path.join(downloaded_path, "config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                print(f"  📊 Architecture: {config.get('model_type', 'unknown')}")
                print(f"  🔤 Vocab size: {config.get('vocab_size', 'unknown'):,}")
                print(f"  📏 Hidden size: {config.get('hidden_size', 'unknown')}")
                print(f"  🔢 Num layers: {config.get('num_hidden_layers', 'unknown')}")
        
        return downloaded_path
    
    except Exception as e:
        print(f"✗ Erreur lors du téléchargement de {model_id}: {e}")
        return None


def get_model_size(model_path: str) -> str:
    """Calcule la taille totale du modèle."""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(model_path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            total_size += os.path.getsize(filepath)
    
    # Convertir en MB
    size_mb = total_size / (1024 * 1024)
    if size_mb > 1024:
        return f"{size_mb / 1024:.2f} GB"
    else:
        return f"{size_mb:.2f} MB"


def setup_models():
    """Télécharge et initialise tous les modèles."""
    
    print("\n" + "=" * 80)
    print("🤖 INITIALISATION DES MODÈLES RÉELS".center(80))
    print("=" * 80)
    
    # Vérifier huggingface_hub
    if not install_huggingface_hub():
        print("\n⚠️  Impossible d'installer huggingface_hub")
        print("   Installez manuellement: pip install huggingface_hub")
        return False
    
    # Modèles à télécharger
    models = [
        {
            "id": "gpt2",
            "name": "gpt2",
            "description": "GPT-2 (124M paramètres)",
        },
        {
            "id": "distilgpt2",
            "name": "distilgpt2",
            "description": "DistilGPT-2 (82M paramètres, plus rapide)",
        },
        {
            "id": "meta-llama/Llama-2-7b-hf",
            "name": "llama2-7b",
            "description": "Llama 2 7B (7B paramètres)",
            "requires_auth": True,
        },
    ]
    
    print("\n📦 MODÈLES DISPONIBLES:")
    print("=" * 80)
    
    for i, model in enumerate(models, 1):
        auth_note = " (nécessite authentification Hugging Face)" if model.get("requires_auth") else ""
        print(f"{i}. {model['description']}{auth_note}")
    
    print("\n" + "=" * 80)
    print("Téléchargement des modèles...")
    print("=" * 80)
    
    downloaded_models = []
    
    # Télécharger GPT-2 (toujours disponible)
    print("\n[1/3] GPT-2...")
    path = download_model("gpt2", "gpt2")
    if path:
        size = get_model_size(path)
        print(f"      Taille: {size}")
        downloaded_models.append(("gpt2", path))
    
    # Télécharger DistilGPT-2 (plus léger)
    print("\n[2/3] DistilGPT-2...")
    path = download_model("distilgpt2", "distilgpt2")
    if path:
        size = get_model_size(path)
        print(f"      Taille: {size}")
        downloaded_models.append(("distilgpt2", path))
    
    # Télécharger Llama-2 (optionnel, peut nécessiter authentification)
    print("\n[3/3] Llama-2 7B...")
    print("      ⚠️  Nécessite un token Hugging Face")
    print("      Voir: https://huggingface.co/meta-llama/Llama-2-7b-hf")
    try:
        path = download_model("meta-llama/Llama-2-7b-hf", "llama2-7b")
        if path:
            size = get_model_size(path)
            print(f"      Taille: {size}")
            downloaded_models.append(("llama2-7b", path))
    except Exception as e:
        print(f"      ⚠️  Llama-2 non disponible: {e}")
        print("      Vous pouvez le télécharger manuellement plus tard")
    
    # Résumé
    print("\n" + "=" * 80)
    print("✅ INITIALISATION TERMINÉE".center(80))
    print("=" * 80)
    
    if downloaded_models:
        print(f"\n✓ {len(downloaded_models)} modèle(s) téléchargé(s):")
        for name, path in downloaded_models:
            size = get_model_size(path)
            print(f"  • {name}: {size}")
    else:
        print("\n⚠️  Aucun modèle n'a pu être téléchargé")
        return False
    
    print("\n📚 Prochaines étapes:")
    print("  1. Lancer: python orchestrator.py --choose-model --topic 'Python'")
    print("  2. Choisir un modèle dans le menu")
    print("  3. L'entraînement commencera automatiquement")
    
    print("\n" + "=" * 80 + "\n")
    
    return True


if __name__ == "__main__":
    success = setup_models()
    sys.exit(0 if success else 1)
