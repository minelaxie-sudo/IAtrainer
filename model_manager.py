"""
Gestionnaire de modèles pour IAtrainer.
Gère le chargement, la sauvegarde et l'entraînement des modèles.
"""

import os
import json
import logging
from typing import Optional, Dict, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ModelManager:
    """Gère les modèles de base et entraînés."""

    def __init__(self):
        self.base_models_dir = "base_models"
        self.trained_models_dir = "trained_models"
        self.current_model = None
        self.current_model_path = None

        # Créer les répertoires s'ils n'existent pas
        os.makedirs(self.base_models_dir, exist_ok=True)
        os.makedirs(self.trained_models_dir, exist_ok=True)

    def list_base_models(self) -> List[Dict]:
        """Liste tous les modèles de base disponibles."""
        models = []

        if not os.path.exists(self.base_models_dir):
            return models

        for filename in os.listdir(self.base_models_dir):
            if filename.endswith((".gguf", ".bin", ".json")):
                filepath = os.path.join(self.base_models_dir, filename)
                size = os.path.getsize(filepath)
                models.append({
                    "name": filename,
                    "path": filepath,
                    "size_mb": round(size / (1024 * 1024), 2),
                    "type": "base",
                })

        return models

    def list_trained_models(self) -> List[Dict]:
        """Liste tous les modèles entraînés disponibles."""
        models = []

        if not os.path.exists(self.trained_models_dir):
            return models

        for filename in os.listdir(self.trained_models_dir):
            if filename.endswith((".gguf", ".json")):
                filepath = os.path.join(self.trained_models_dir, filename)
                size = os.path.getsize(filepath)
                models.append({
                    "name": filename,
                    "path": filepath,
                    "size_mb": round(size / (1024 * 1024), 2),
                    "type": "trained",
                })

        return models

    def load_base_model(self, model_name: str) -> bool:
        """Charge un modèle de base."""
        model_path = os.path.join(self.base_models_dir, model_name)

        if not os.path.exists(model_path):
            logger.error(f"Modèle de base non trouvé: {model_path}")
            return False

        try:
            self.current_model_path = model_path
            self.current_model = {
                "name": model_name,
                "path": model_path,
                "loaded_at": datetime.utcnow().isoformat(),
                "type": "base",
            }
            logger.info(f"✓ Modèle de base chargé: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            return False

    def load_trained_model(self, model_name: str) -> bool:
        """Charge un modèle entraîné."""
        model_path = os.path.join(self.trained_models_dir, model_name)

        if not os.path.exists(model_path):
            logger.error(f"Modèle entraîné non trouvé: {model_path}")
            return False

        try:
            self.current_model_path = model_path
            self.current_model = {
                "name": model_name,
                "path": model_path,
                "loaded_at": datetime.utcnow().isoformat(),
                "type": "trained",
            }
            logger.info(f"✓ Modèle entraîné chargé: {model_name}")
            return True
        except Exception as e:
            logger.error(f"Erreur lors du chargement du modèle: {e}")
            return False

    def get_current_model(self) -> Optional[Dict]:
        """Retourne le modèle actuellement chargé."""
        return self.current_model

    def create_base_model_template(self, model_name: str) -> str:
        """Crée un template de modèle de base."""
        template = {
            "name": model_name,
            "type": "base_model",
            "created_at": datetime.utcnow().isoformat(),
            "version": "1.0.0",
            "architecture": "transformer",
            "parameters": {
                "vocab_size": 32000,
                "hidden_size": 768,
                "num_layers": 12,
                "num_heads": 12,
            },
            "training_config": {
                "learning_rate": 1e-4,
                "batch_size": 32,
                "epochs": 3,
                "optimizer": "adam",
            },
            "description": f"Modèle de base pour {model_name}",
        }

        filepath = os.path.join(self.base_models_dir, f"{model_name}.json")

        with open(filepath, "w") as f:
            json.dump(template, f, indent=2)

        logger.info(f"✓ Template créé: {filepath}")
        return filepath

    def download_base_model(self, model_id: str, model_name: str) -> bool:
        """
        Télécharge un modèle de base depuis Hugging Face ou Ollama.
        Exemples: "meta-llama/Llama-2-7b", "mistralai/Mistral-7B", etc.
        """
        logger.info(f"Téléchargement du modèle: {model_id}")
        logger.info(f"Destination: {self.base_models_dir}/{model_name}")

        try:
            # Essayer avec transformers (Hugging Face)
            try:
                from transformers import AutoModel, AutoTokenizer

                logger.info("Téléchargement depuis Hugging Face...")
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = AutoModel.from_pretrained(model_id)

                # Sauvegarder
                model_path = os.path.join(self.base_models_dir, model_name)
                os.makedirs(model_path, exist_ok=True)
                model.save_pretrained(model_path)
                tokenizer.save_pretrained(model_path)

                logger.info(f"✓ Modèle téléchargé: {model_path}")
                return True

            except ImportError:
                logger.warning("transformers non installé, essai avec Ollama...")

                # Essayer avec Ollama
                import subprocess

                result = subprocess.run(
                    ["ollama", "pull", model_id],
                    capture_output=True,
                    text=True,
                )

                if result.returncode == 0:
                    logger.info(f"✓ Modèle téléchargé avec Ollama: {model_id}")
                    # Créer un fichier de référence
                    ref_file = os.path.join(self.base_models_dir, f"{model_name}.ollama")
                    with open(ref_file, "w") as f:
                        f.write(model_id)
                    return True
                else:
                    logger.error(f"Erreur Ollama: {result.stderr}")
                    return False

        except Exception as e:
            logger.error(f"Erreur lors du téléchargement: {e}")
            return False

    def get_model_info(self, model_path: str) -> Optional[Dict]:
        """Récupère les infos d'un modèle."""
        if not os.path.exists(model_path):
            return None

        try:
            if model_path.endswith(".json"):
                with open(model_path, "r") as f:
                    return json.load(f)
            else:
                return {
                    "name": os.path.basename(model_path),
                    "path": model_path,
                    "size_mb": round(os.path.getsize(model_path) / (1024 * 1024), 2),
                }
        except Exception as e:
            logger.error(f"Erreur lors de la lecture du modèle: {e}")
            return None

    def display_model_menu(self):
        """Affiche un menu interactif pour gérer les modèles."""
        while True:
            print("\n" + "=" * 70)
            print("GESTIONNAIRE DE MODÈLES".center(70))
            print("=" * 70)

            print("\n📦 MODÈLES DE BASE:")
            base_models = self.list_base_models()
            if base_models:
                for idx, model in enumerate(base_models, 1):
                    print(f"  {idx}. {model['name']} ({model['size_mb']} MB)")
            else:
                print("  Aucun modèle de base trouvé")

            print("\n✅ MODÈLES ENTRAÎNÉS:")
            trained_models = self.list_trained_models()
            if trained_models:
                for idx, model in enumerate(trained_models, 1):
                    print(f"  {idx}. {model['name']} ({model['size_mb']} MB)")
            else:
                print("  Aucun modèle entraîné trouvé")

            print("\n" + "-" * 70)
            print("OPTIONS:")
            print("1. Charger un modèle de base")
            print("2. Charger un modèle entraîné")
            print("3. Créer un template de modèle de base")
            print("4. Télécharger un modèle depuis Hugging Face")
            print("5. Télécharger un modèle depuis Ollama")
            print("6. Afficher les infos du modèle actuel")
            print("7. Quitter")

            choice = input("\nChoisissez une option (1-7): ").strip()

            if choice == "1":
                base_models = self.list_base_models()
                if base_models:
                    for idx, model in enumerate(base_models, 1):
                        print(f"{idx}. {model['name']}")
                    try:
                        model_idx = int(input("Choisissez un modèle: ")) - 1
                        if 0 <= model_idx < len(base_models):
                            self.load_base_model(base_models[model_idx]["name"])
                        else:
                            print("Index invalide")
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                else:
                    print("Aucun modèle de base disponible")

            elif choice == "2":
                trained_models = self.list_trained_models()
                if trained_models:
                    for idx, model in enumerate(trained_models, 1):
                        print(f"{idx}. {model['name']}")
                    try:
                        model_idx = int(input("Choisissez un modèle: ")) - 1
                        if 0 <= model_idx < len(trained_models):
                            self.load_trained_model(trained_models[model_idx]["name"])
                        else:
                            print("Index invalide")
                    except ValueError:
                        print("Veuillez entrer un nombre valide")
                else:
                    print("Aucun modèle entraîné disponible")

            elif choice == "3":
                model_name = input("Nom du modèle de base: ").strip()
                if model_name:
                    self.create_base_model_template(model_name)
                else:
                    print("Nom invalide")

            elif choice == "4":
                model_id = input("ID du modèle Hugging Face (ex: meta-llama/Llama-2-7b): ").strip()
                model_name = input("Nom local du modèle: ").strip()
                if model_id and model_name:
                    self.download_base_model(model_id, model_name)
                else:
                    print("Paramètres invalides")

            elif choice == "5":
                model_id = input("ID du modèle Ollama (ex: llama2, mistral): ").strip()
                model_name = input("Nom local du modèle: ").strip()
                if model_id and model_name:
                    self.download_base_model(model_id, model_name)
                else:
                    print("Paramètres invalides")

            elif choice == "6":
                if self.current_model:
                    print("\n📋 Modèle actuel:")
                    for key, value in self.current_model.items():
                        print(f"  {key}: {value}")
                else:
                    print("Aucun modèle chargé")

            elif choice == "7":
                print("Au revoir!")
                break

            else:
                print("Option invalide")


def main():
    """Point d'entrée principal."""
    manager = ModelManager()
    manager.display_model_menu()


if __name__ == "__main__":
    main()
