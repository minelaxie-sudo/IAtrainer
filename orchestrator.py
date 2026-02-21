"""
Orchestrateur principal pour IAtrainer.
Gère le scraping, l'entraînement multi-agents et l'intégration avec UnityIAPro.
"""

import logging
import time
from typing import List, Dict, Optional
from scraper import WebScraper
from multi_agent_system import MultiAgentSystem
from trpc_client import TRPCClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class IAtrainerOrchestrator:
    """Orchestrateur principal pour IAtrainer."""

    def __init__(
        self,
        dashboard_url: str = "http://localhost:3000/api/trpc",
        model_name: str = "llama2-unity",
    ):
        self.scraper = WebScraper()
        self.multi_agent_system = MultiAgentSystem()
        self.trpc_client = TRPCClient(dashboard_url)
        self.model_name = model_name
        self.training_data: List[Dict] = []

    def scrape_training_data(self, topic: str, num_pages: int = 5, code_only: bool = False) -> List[Dict]:
        """
        Scrape les données d'entraînement depuis internet.
        Si code_only=True, scrape uniquement du code (GitHub, etc.)
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"SCRAPING: {topic} (code_only={code_only})")
        logger.info(f"{'='*60}")

        # Scraper le sujet
        self.training_data = self.scraper.scrape_topic(topic, num_pages, code_only=code_only)

        logger.info(f"✓ {len(self.training_data)} pages scrapées")

        # Afficher les sources
        for idx, data in enumerate(self.training_data, 1):
            logger.info(f"  {idx}. {data['title'][:60]}...")

        return self.training_data

    def prepare_training_tasks(self) -> List[str]:
        """
        Prépare les tâches d'entraînement à partir des données scrapées.
        """
        tasks = []

        for data in self.training_data:
            # Extraire les tâches du contenu
            content = data.get("content", "")
            if len(content) > 100:
                # Créer une tâche basée sur le contenu
                task = f"Implémenter une solution basée sur: {data.get('title', 'Tâche')[:50]}"
                tasks.append(task)

        logger.info(f"✓ {len(tasks)} tâches d'entraînement préparées")
        return tasks

    def run_training_session(
        self,
        topic: str,
        num_pages: int = 5,
        num_iterations: int = 3,
        dashboard_enabled: bool = True,
        code_only: bool = False,
    ) -> Dict:
        """
        Lance une session d'entraînement complète.
        """
        logger.info(f"\n{'='*70}")
        logger.info(f"DÉMARRAGE DE LA SESSION D'ENTRAÎNEMENT")
        logger.info(f"Sujet: {topic}")
        logger.info(f"Itérations: {num_iterations}")
        logger.info(f"Dashboard: {dashboard_enabled}")
        logger.info(f"{'='*70}")

        session_id = None

        try:
            # Étape 1: Scraper les données
            logger.info("\n[ÉTAPE 1] Scraping des données...")
            self.scrape_training_data(topic, num_pages, code_only=code_only)

            # Étape 2: Créer une session dans le dashboard
            if dashboard_enabled:
                logger.info("\n[ÉTAPE 2] Création de la session dans UnityIAPro...")
                session_id = self.trpc_client.create_session(
                    name=f"Training: {topic}",
                    model_name=self.model_name,
                    description=f"Session d'entraînement sur {topic}",
                    config={
                        "num_pages": num_pages,
                        "num_iterations": num_iterations,
                        "topic": topic,
                    },
                )

                if session_id:
                    self.trpc_client.update_session_status("running")
                    logger.info(f"✓ Session créée: {session_id}")
                else:
                    logger.warning("⚠ Impossible de créer une session (dashboard non disponible?)")
                    dashboard_enabled = False

            # Étape 3: Préparer les tâches
            logger.info("\n[ÉTAPE 3] Préparation des tâches...")
            tasks = self.prepare_training_tasks()

            if not tasks:
                logger.warning("⚠ Aucune tâche préparée, utilisation de tâches par défaut")
                tasks = [
                    f"Implémenter une solution optimisée pour {topic}",
                    f"Créer une fonction efficace pour {topic}",
                    f"Optimiser le code pour {topic}",
                ]

            # Étape 4: Exécuter les itérations
            logger.info(f"\n[ÉTAPE 4] Exécution de {num_iterations} itérations...")

            for iteration in range(num_iterations):
                task = tasks[iteration % len(tasks)]
                context = self.training_data[0].get("content", "")[:500] if self.training_data else ""

                # Exécuter l'itération
                result = self.multi_agent_system.run_iteration(task, context)

                # Envoyer les données au dashboard
                if dashboard_enabled and session_id:
                    self._send_iteration_to_dashboard(result)

                # Pause entre les itérations
                if iteration < num_iterations - 1:
                    logger.info("Pause avant l'itération suivante...")
                    time.sleep(2)

            # Étape 5: Résumé final
            logger.info("\n[ÉTAPE 5] Génération du résumé...")
            summary = self.multi_agent_system.get_session_summary()

            if dashboard_enabled and session_id:
                self.trpc_client.update_session_status("completed")

            logger.info(f"\n{'='*70}")
            logger.info("RÉSUMÉ DE LA SESSION")
            logger.info(f"{'='*70}")
            logger.info(f"Itérations: {summary['iterations']}")
            logger.info(f"Messages totaux: {summary['total_messages']}")
            logger.info(f"Décisions: {summary['total_decisions']}")
            logger.info(f"Qualité Coder A: {summary['coder_a_metrics']['avg_quality_score']:.2f}")
            logger.info(f"Qualité Coder B: {summary['coder_b_metrics']['avg_quality_score']:.2f}")
            logger.info(f"Qualité Arbitre: {summary['arbiter_metrics']['avg_decision_quality']:.2f}")

            return {
                "status": "completed",
                "session_id": session_id,
                "summary": summary,
                "training_data_count": len(self.training_data),
            }

        except Exception as e:
            logger.error(f"✗ Erreur lors de la session: {e}")

            if dashboard_enabled and session_id:
                try:
                    self.trpc_client.create_alert(
                        severity="error",
                        title="Erreur lors de l'entraînement",
                        description=str(e),
                    )
                    self.trpc_client.update_session_status("error")
                except Exception as alert_error:
                    logger.error(f"Impossible d'envoyer l'alerte: {alert_error}")

            return {
                "status": "error",
                "session_id": session_id,
                "error": str(e),
            }

        finally:
            self.trpc_client.close()

    def _send_iteration_to_dashboard(self, iteration_result: Dict) -> None:
        """
        Envoie les résultats d'une itération au dashboard.
        """
        try:
            iteration = iteration_result["iteration"]
            decision = iteration_result["decision"]

            # Envoyer les statuts des agents
            self.trpc_client.update_agent_status(
                "coder_a",
                "idle",
                True,
                self.multi_agent_system.coder_a.metrics,
            )
            self.trpc_client.update_agent_status(
                "coder_b",
                "idle",
                True,
                self.multi_agent_system.coder_b.metrics,
            )
            self.trpc_client.update_agent_status(
                "arbiter",
                "idle",
                True,
                self.multi_agent_system.arbiter.metrics,
            )

            # Envoyer la décision d'arbitrage
            self.trpc_client.create_arbitration_decision(
                iteration_number=iteration,
                coder_a_solution_id=iteration_result["solution_a_id"],
                coder_b_solution_id=iteration_result["solution_b_id"],
                selected_solution=decision["selected_solution"],
                justification=decision["justification"],
            )

            logger.info(f"✓ Itération {iteration} envoyée au dashboard")

        except Exception as e:
            logger.error(f"✗ Erreur lors de l'envoi au dashboard: {e}")


def main():
    """Point d'entrée principal."""
    import argparse

    parser = argparse.ArgumentParser(description="IAtrainer - Système d'entraînement multi-agents")
    parser.add_argument(
        "--topic",
        type=str,
        default="Unity game development best practices",
        help="Sujet à scraper et entraîner",
    )
    parser.add_argument(
        "--pages",
        type=int,
        default=3,
        help="Nombre de pages à scraper",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=3,
        help="Nombre d'itérations d'entraînement",
    )
    parser.add_argument(
        "--dashboard-url",
        type=str,
        default="http://localhost:3000/api/trpc",
        help="URL du dashboard UnityIAPro",
    )
    parser.add_argument(
        "--no-dashboard",
        action="store_true",
        help="Désactiver l'intégration avec le dashboard",
    )
    parser.add_argument(
        "--code-only",
        action="store_true",
        help="Scraper uniquement du code (GitHub, etc.) pour un modèle full codage",
    )

    args = parser.parse_args()

    # Créer l'orchestrateur
    orchestrator = IAtrainerOrchestrator(
        dashboard_url=args.dashboard_url,
        model_name="llama2-unity",
    )

    # Lancer la session d'entraînement
    result = orchestrator.run_training_session(
        topic=args.topic,
        num_pages=args.pages,
        num_iterations=args.iterations,
        dashboard_enabled=not args.no_dashboard,
        code_only=args.code_only,
    )

    # Afficher le résultat final
    if result["status"] == "completed":
        logger.info("\n✓ Session d'entraînement réussie!")
        logger.info(f"Session ID: {result['session_id']}")
    else:
        logger.error(f"\n✗ Erreur: {result.get('error', 'Erreur inconnue')}")


if __name__ == "__main__":
    main()
