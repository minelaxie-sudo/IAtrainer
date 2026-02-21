"""
Analyseur de paramètres de modèle.
Calcule et affiche le nombre de paramètres avant/après entraînement.
"""

import json
import os
from datetime import datetime
from typing import Dict, Optional


class ModelAnalyzer:
    """Analyse les paramètres et statistiques du modèle."""

    def __init__(self, model_name: str):
        self.model_name = model_name
        self.stats_dir = "model_stats"
        self._create_stats_dir()

    def _create_stats_dir(self):
        """Crée le dossier de statistiques s'il n'existe pas."""
        if not os.path.exists(self.stats_dir):
            os.makedirs(self.stats_dir)

    def estimate_parameters(self, config: Optional[Dict] = None) -> int:
        """
        Estime le nombre de paramètres du modèle.
        Formule approximative pour un transformer:
        params ≈ 4 * hidden_size * num_layers * (3 * hidden_size + 4 * intermediate_size)
        """
        if config is None:
            config = self._get_default_config()

        hidden_size = config.get("hidden_size", 768)
        num_layers = config.get("num_layers", 12)
        vocab_size = config.get("vocab_size", 32000)
        intermediate_size = config.get("intermediate_size", hidden_size * 4)

        # Calcul approximatif des paramètres
        # Embeddings
        embedding_params = vocab_size * hidden_size

        # Attention + Feed-forward par layer
        per_layer_params = (
            3 * hidden_size * hidden_size  # Q, K, V projections
            + hidden_size * hidden_size  # Output projection
            + 2 * hidden_size  # Layer norms
            + hidden_size * intermediate_size  # Feed-forward first layer
            + intermediate_size * hidden_size  # Feed-forward second layer
            + 2 * intermediate_size  # Feed-forward biases
        )

        total_params = embedding_params + (per_layer_params * num_layers)

        return int(total_params)

    def _get_default_config(self) -> Dict:
        """Retourne la configuration par défaut."""
        return {
            "vocab_size": 32000,
            "hidden_size": 768,
            "num_layers": 12,
            "intermediate_size": 3072,
        }

    def get_model_info(self, model_path: str) -> Optional[Dict]:
        """Récupère les informations du modèle."""
        if not os.path.exists(model_path):
            return None

        try:
            if model_path.endswith(".json"):
                with open(model_path, "r") as f:
                    data = json.load(f)
                    return {
                        "name": self.model_name,
                        "path": model_path,
                        "type": "json",
                        "size_mb": os.path.getsize(model_path) / (1024 * 1024),
                        "iterations": len(data.get("iterations", [])),
                        "tokens_processed": data.get("total_tokens_processed", 0),
                        "training_duration": data.get("training_duration_seconds", 0),
                    }
            elif model_path.endswith(".gguf"):
                return {
                    "name": self.model_name,
                    "path": model_path,
                    "type": "gguf",
                    "size_mb": os.path.getsize(model_path) / (1024 * 1024),
                }
        except Exception as e:
            print(f"Erreur lors de la lecture du modèle: {e}")
            return None

    def save_training_stats(
        self,
        before_params: int,
        after_params: int,
        training_data: Dict,
        model_file: str,
    ) -> str:
        """Sauvegarde les statistiques d'entraînement."""
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        stats_file = os.path.join(
            self.stats_dir, f"{self.model_name}_stats_{timestamp}.json"
        )

        stats = {
            "model_name": self.model_name,
            "timestamp": datetime.utcnow().isoformat(),
            "parameters": {
                "before_training": before_params,
                "after_training": after_params,
                "difference": after_params - before_params,
                "percentage_change": (
                    ((after_params - before_params) / before_params * 100)
                    if before_params > 0
                    else 0
                ),
            },
            "training_metrics": {
                "iterations": len(training_data.get("iterations", [])),
                "total_tokens_processed": training_data.get("total_tokens_processed", 0),
                "training_duration_seconds": training_data.get(
                    "training_duration_seconds", 0
                ),
                "coder_a_quality": training_data.get("learning_metrics", {}).get(
                    "coder_a_quality", 0
                ),
                "coder_b_quality": training_data.get("learning_metrics", {}).get(
                    "coder_b_quality", 0
                ),
                "arbiter_quality": training_data.get("learning_metrics", {}).get(
                    "arbiter_decision_quality", 0
                ),
            },
            "model_file": model_file,
        }

        with open(stats_file, "w") as f:
            json.dump(stats, f, indent=2)

        return stats_file

    def display_training_summary(
        self,
        before_params: int,
        after_params: int,
        training_data: Dict,
        model_file: str,
    ):
        """Affiche un résumé complet de l'entraînement."""
        print("\n" + "=" * 80)
        print("📊 ANALYSE DES PARAMÈTRES DU MODÈLE".center(80))
        print("=" * 80)

        print(f"\n🤖 Modèle: {self.model_name}")

        # Paramètres
        print(f"\n📈 Paramètres:")
        print(f"  • Avant entraînement: {before_params:,} paramètres")
        print(f"  • Après entraînement: {after_params:,} paramètres")

        diff = after_params - before_params
        if diff != 0:
            pct_change = (diff / before_params * 100) if before_params > 0 else 0
            symbol = "↑" if diff > 0 else "↓"
            print(f"  • Différence: {symbol} {abs(diff):,} ({pct_change:+.2f}%)")
        else:
            print(f"  • Différence: → Aucun changement")

        # Métriques d'entraînement
        print(f"\n⏱️  Entraînement:")
        iterations = len(training_data.get("iterations", []))
        tokens = training_data.get("total_tokens_processed", 0)
        duration = training_data.get("training_duration_seconds", 0)

        print(f"  • Itérations: {iterations}")
        print(f"  • Tokens traités: {tokens:,}")
        if duration > 0:
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            print(f"  • Durée: {minutes}m {seconds}s")

        # Qualité
        print(f"\n🎯 Qualité des agents:")
        metrics = training_data.get("learning_metrics", {})
        print(f"  • Coder A: {metrics.get('coder_a_quality', 0):.2%}")
        print(f"  • Coder B: {metrics.get('coder_b_quality', 0):.2%}")
        print(f"  • Arbitre: {metrics.get('arbiter_decision_quality', 0):.2%}")

        # Fichiers
        print(f"\n📁 Fichiers:")
        print(f"  • Modèle: {model_file}")

        # Taille du modèle
        if os.path.exists(model_file):
            size_mb = os.path.getsize(model_file) / (1024 * 1024)
            print(f"  • Taille: {size_mb:.2f} MB")

        print("\n" + "=" * 80)

    def display_model_comparison(self, models_to_compare: list):
        """Affiche une comparaison entre plusieurs modèles."""
        print("\n" + "=" * 80)
        print("📊 COMPARAISON DES MODÈLES".center(80))
        print("=" * 80)

        print(f"\n{'Modèle':<30} {'Paramètres':<20} {'Tokens':<15} {'Qualité':<15}")
        print("-" * 80)

        for model_name, model_file in models_to_compare:
            info = self.get_model_info(model_file)
            if info:
                params = self.estimate_parameters()
                tokens = info.get("tokens_processed", 0)
                quality = 0  # À calculer depuis les données

                print(
                    f"{model_name:<30} {params:>15,} {tokens:>15,} {quality:>14.2%}"
                )

        print("\n" + "=" * 80)

    def get_training_history(self) -> list:
        """Récupère l'historique d'entraînement."""
        history = []

        if not os.path.exists(self.stats_dir):
            return history

        for filename in sorted(os.listdir(self.stats_dir)):
            if filename.endswith(".json"):
                filepath = os.path.join(self.stats_dir, filename)
                try:
                    with open(filepath, "r") as f:
                        data = json.load(f)
                        history.append(data)
                except Exception as e:
                    print(f"Erreur lors de la lecture de {filename}: {e}")

        return history

    def display_training_history(self):
        """Affiche l'historique d'entraînement."""
        history = self.get_training_history()

        if not history:
            print("\n⚠️  Aucun historique d'entraînement trouvé")
            return

        print("\n" + "=" * 80)
        print("📈 HISTORIQUE D'ENTRAÎNEMENT".center(80))
        print("=" * 80)

        print(
            f"\n{'Date':<20} {'Itérations':<15} {'Paramètres':<20} {'Qualité':<15}"
        )
        print("-" * 80)

        for entry in history:
            date = entry.get("timestamp", "")[:10]
            iterations = entry.get("training_metrics", {}).get("iterations", 0)
            params = entry.get("parameters", {}).get("after_training", 0)
            quality = entry.get("training_metrics", {}).get("arbiter_quality", 0)

            print(f"{date:<20} {iterations:>15} {params:>18,} {quality:>14.2%}")

        print("\n" + "=" * 80)
