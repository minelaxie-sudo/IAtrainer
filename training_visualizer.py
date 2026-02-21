"""
Visualiseur en temps réel du processus d'entraînement du modèle.
Affiche les progrès, métriques et permet d'arrêter proprement l'entraînement.
"""

import json
import os
from datetime import datetime
from typing import Dict, List
import threading
import time

class TrainingVisualizer:
    """Visualise l'entraînement en temps réel."""

    def __init__(self, model_name: str = "llama2-unity"):
        self.model_name = model_name
        self.training_data = {
            "model_name": model_name,
            "start_time": datetime.utcnow().isoformat(),
            "iterations": [],
            "total_iterations": 0,
            "total_tokens_processed": 0,
            "learning_metrics": {
                "avg_loss": 0.0,
                "avg_accuracy": 0.0,
                "coder_a_quality": 0.0,
                "coder_b_quality": 0.0,
                "arbiter_decision_quality": 0.0,
            },
            "is_training": False,
            "paused": False,
        }
        self.should_stop = False
        self.pause_event = threading.Event()
        self.pause_event.set()  # Non pausé par défaut

    def start_training(self, total_iterations: int):
        """Démarre l'entraînement."""
        self.training_data["is_training"] = True
        self.training_data["total_iterations"] = total_iterations
        self.should_stop = False
        self.display_header()

    def display_header(self):
        """Affiche l'en-tête du dashboard."""
        print("\n" + "=" * 80)
        print("🤖 TABLEAU DE BORD D'ENTRAÎNEMENT - IAtrainer".center(80))
        print("=" * 80)
        print(f"Modèle: {self.model_name}")
        print(f"Démarrage: {self.training_data['start_time']}")
        print("=" * 80 + "\n")

    def update_iteration(
        self,
        iteration: int,
        coder_a_solution: str,
        coder_b_solution: str,
        arbiter_decision: str,
        coder_a_quality: float,
        coder_b_quality: float,
        arbiter_quality: float,
        tokens_processed: int,
    ):
        """Met à jour les données d'une itération."""
        # Attendre si en pause
        self.pause_event.wait()

        if self.should_stop:
            return False

        iteration_data = {
            "iteration": iteration,
            "timestamp": datetime.utcnow().isoformat(),
            "coder_a_solution": coder_a_solution[:100] + "..." if len(coder_a_solution) > 100 else coder_a_solution,
            "coder_b_solution": coder_b_solution[:100] + "..." if len(coder_b_solution) > 100 else coder_b_solution,
            "arbiter_decision": arbiter_decision,
            "coder_a_quality": coder_a_quality,
            "coder_b_quality": coder_b_quality,
            "arbiter_quality": arbiter_quality,
            "tokens_processed": tokens_processed,
        }

        self.training_data["iterations"].append(iteration_data)
        self.training_data["total_tokens_processed"] += tokens_processed

        # Mettre à jour les métriques moyennes
        self._update_metrics()

        # Afficher le progrès
        self.display_progress(iteration)

        return True

    def _update_metrics(self):
        """Met à jour les métriques moyennes."""
        if not self.training_data["iterations"]:
            return

        iterations = self.training_data["iterations"]
        self.training_data["learning_metrics"]["coder_a_quality"] = sum(
            it["coder_a_quality"] for it in iterations
        ) / len(iterations)
        self.training_data["learning_metrics"]["coder_b_quality"] = sum(
            it["coder_b_quality"] for it in iterations
        ) / len(iterations)
        self.training_data["learning_metrics"]["arbiter_decision_quality"] = sum(
            it["arbiter_quality"] for it in iterations
        ) / len(iterations)

    def display_progress(self, current_iteration: int):
        """Affiche la barre de progression."""
        total = self.training_data["total_iterations"]
        progress = current_iteration / total if total > 0 else 0

        # Barre de progression
        bar_length = 40
        filled = int(bar_length * progress)
        bar = "█" * filled + "░" * (bar_length - filled)

        # Pourcentage
        percentage = int(progress * 100)

        # Affichage
        print(f"\n[Itération {current_iteration}/{total}]")
        print(f"Progress: |{bar}| {percentage}%")

        # Afficher les dernières données
        if self.training_data["iterations"]:
            last_iter = self.training_data["iterations"][-1]
            print(f"\n📊 Dernière itération:")
            print(f"  ✓ Coder A qualité: {last_iter['coder_a_quality']:.2%}")
            print(f"  ✓ Coder B qualité: {last_iter['coder_b_quality']:.2%}")
            print(f"  ✓ Arbitre qualité: {last_iter['arbiter_quality']:.2%}")
            print(f"  ✓ Tokens traités: {last_iter['tokens_processed']}")
            print(f"  ✓ Décision: {last_iter['arbiter_decision']}")

        # Afficher les métriques moyennes
        metrics = self.training_data["learning_metrics"]
        print(f"\n📈 Métriques moyennes:")
        print(f"  • Coder A: {metrics['coder_a_quality']:.2%}")
        print(f"  • Coder B: {metrics['coder_b_quality']:.2%}")
        print(f"  • Arbitre: {metrics['arbiter_decision_quality']:.2%}")
        print(f"  • Total tokens: {self.training_data['total_tokens_processed']}")

        print(f"\n💡 Commandes:")
        print(f"  [P] Pause/Reprendre  [S] Arrêter  [I] Infos détaillées")

    def pause_training(self):
        """Met en pause l'entraînement."""
        if self.training_data["paused"]:
            self.pause_event.set()
            self.training_data["paused"] = False
            print("\n▶️  Entraînement repris...")
        else:
            self.pause_event.clear()
            self.training_data["paused"] = True
            print("\n⏸️  Entraînement en pause...")

    def stop_training(self):
        """Arrête l'entraînement."""
        self.should_stop = True
        self.pause_event.set()  # Débloquer si en pause
        print("\n⏹️  Arrêt de l'entraînement...")

    def save_model(self, output_dir: str = "trained_models"):
        """Sauvegarde le modèle et les apprentissages."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        model_file = os.path.join(output_dir, f"{self.model_name}_{timestamp}.json")

        # Ajouter les infos de fin
        self.training_data["end_time"] = datetime.utcnow().isoformat()
        self.training_data["is_training"] = False

        # Calculer la durée
        start = datetime.fromisoformat(self.training_data["start_time"])
        end = datetime.fromisoformat(self.training_data["end_time"])
        duration = (end - start).total_seconds()
        self.training_data["training_duration_seconds"] = duration

        # Sauvegarder
        with open(model_file, "w") as f:
            json.dump(self.training_data, f, indent=2)

        print(f"\n✅ Modèle sauvegardé: {model_file}")
        return model_file

    def display_summary(self):
        """Affiche le résumé final."""
        print("\n" + "=" * 80)
        print("📋 RÉSUMÉ DE L'ENTRAÎNEMENT".center(80))
        print("=" * 80)

        print(f"\nModèle: {self.training_data['model_name']}")
        print(f"Itérations complétées: {len(self.training_data['iterations'])}/{self.training_data['total_iterations']}")
        print(f"Tokens traités: {self.training_data['total_tokens_processed']}")

        if self.training_data.get("end_time"):
            duration = self.training_data.get("training_duration_seconds", 0)
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            print(f"Durée: {minutes}m {seconds}s")

        print(f"\n📊 Qualité moyenne:")
        metrics = self.training_data["learning_metrics"]
        print(f"  • Coder A: {metrics['coder_a_quality']:.2%}")
        print(f"  • Coder B: {metrics['coder_b_quality']:.2%}")
        print(f"  • Arbitre: {metrics['arbiter_decision_quality']:.2%}")

        # Meilleure itération
        if self.training_data["iterations"]:
            best_iter = max(
                self.training_data["iterations"],
                key=lambda x: x["arbiter_quality"]
            )
            print(f"\n🏆 Meilleure itération: #{best_iter['iteration']}")
            print(f"   Qualité arbitre: {best_iter['arbiter_quality']:.2%}")

        print("\n" + "=" * 80)

    def export_for_ollama(self, output_dir: str = "trained_models"):
        """Exporte le modèle au format Ollama."""
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        gguf_file = os.path.join(output_dir, f"{self.model_name}_{timestamp}.gguf.json")

        ollama_data = {
            "model_name": self.model_name,
            "format": "gguf",
            "training_data": self.training_data,
            "export_timestamp": datetime.utcnow().isoformat(),
            "instructions": [
                "1. Convertir ce fichier au format GGUF",
                "2. Créer un Modelfile pour Ollama",
                "3. Charger avec: ollama create mon-modele -f Modelfile",
                "4. Utiliser avec: ollama run mon-modele 'votre prompt'",
            ],
        }

        with open(gguf_file, "w") as f:
            json.dump(ollama_data, f, indent=2)

        print(f"\n✅ Modèle exporté pour Ollama: {gguf_file}")
        return gguf_file

    def get_training_data(self) -> Dict:
        """Retourne les données d'entraînement."""
        return self.training_data

    def display_detailed_info(self):
        """Affiche les infos détaillées."""
        print("\n" + "=" * 80)
        print("📊 INFORMATIONS DÉTAILLÉES".center(80))
        print("=" * 80)

        print(f"\nModèle: {self.training_data['model_name']}")
        print(f"Itérations: {len(self.training_data['iterations'])}")
        print(f"Tokens totaux: {self.training_data['total_tokens_processed']}")

        print(f"\n🔍 Dernières itérations:")
        for iter_data in self.training_data["iterations"][-5:]:
            print(f"\n  Itération #{iter_data['iteration']}:")
            print(f"    • Coder A: {iter_data['coder_a_quality']:.2%}")
            print(f"    • Coder B: {iter_data['coder_b_quality']:.2%}")
            print(f"    • Arbitre: {iter_data['arbiter_quality']:.2%}")
            print(f"    • Décision: {iter_data['arbiter_decision']}")

        print("\n" + "=" * 80)


def demo_training():
    """Démo du système de visualisation."""
    visualizer = TrainingVisualizer("llama2-unity")
    visualizer.start_training(total_iterations=10)

    # Simuler 10 itérations
    for i in range(1, 11):
        # Simuler des données d'entraînement
        import random

        coder_a_quality = 0.5 + (i * 0.04) + random.uniform(-0.05, 0.05)
        coder_b_quality = 0.5 + (i * 0.03) + random.uniform(-0.05, 0.05)
        arbiter_quality = max(coder_a_quality, coder_b_quality) + random.uniform(-0.02, 0.02)

        visualizer.update_iteration(
            iteration=i,
            coder_a_solution=f"def solution_a_{i}(): pass",
            coder_b_solution=f"def solution_b_{i}(): pass",
            arbiter_decision="Coder A" if coder_a_quality > coder_b_quality else "Coder B",
            coder_a_quality=min(coder_a_quality, 1.0),
            coder_b_quality=min(coder_b_quality, 1.0),
            arbiter_quality=min(arbiter_quality, 1.0),
            tokens_processed=random.randint(100, 500),
        )

        time.sleep(1)  # Pause pour la démo

    visualizer.display_summary()
    visualizer.save_model()
    visualizer.export_for_ollama()


if __name__ == "__main__":
    demo_training()
