"""
Système multi-agents pour l'entraînement du modèle LLM.
Inclut Coder A, Coder B et Arbitre.
"""

import json
import uuid
from typing import Dict, List, Optional
from datetime import datetime
from enum import Enum
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AgentType(str, Enum):
    """Types d'agents."""
    CODER_A = "coder_a"
    CODER_B = "coder_b"
    ARBITER = "arbiter"


class MessageType(str, Enum):
    """Types de messages."""
    TASK = "task"
    SOLUTION = "solution"
    COMPARISON = "comparison"
    DECISION = "decision"
    FEEDBACK = "feedback"
    ERROR = "error"


class Message:
    """Représente un message entre agents."""

    def __init__(
        self,
        from_agent: AgentType,
        to_agent: AgentType,
        message_type: MessageType,
        content: str,
        code_content: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ):
        self.message_id = str(uuid.uuid4())
        self.from_agent = from_agent
        self.to_agent = to_agent
        self.message_type = message_type
        self.content = content
        self.code_content = code_content
        self.metadata = metadata or {}
        self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict:
        """Convertir en dictionnaire."""
        return {
            "message_id": self.message_id,
            "from_agent": self.from_agent.value,
            "to_agent": self.to_agent.value,
            "message_type": self.message_type.value,
            "content": self.content,
            "code_content": self.code_content,
            "metadata": self.metadata,
            "timestamp": self.timestamp,
        }


class CoderAgent:
    """Agent Coder (A ou B) qui génère des solutions."""

    def __init__(self, agent_type: AgentType):
        assert agent_type in [AgentType.CODER_A, AgentType.CODER_B]
        self.agent_type = agent_type
        self.status = "idle"
        self.metrics = {
            "solutions_generated": 0,
            "avg_quality_score": 0.0,
            "response_time_ms": 0,
            "success_rate": 0.0,
        }

    def generate_solution(self, task: str, context: str = "") -> Message:
        """
        Génère une solution pour une tâche donnée.
        """
        self.status = "generating"
        logger.info(f"{self.agent_type.value} génère une solution pour: {task[:50]}...")

        # Simuler la génération de code
        code_solution = f"""
# Solution par {self.agent_type.value}
# Tâche: {task}

def solve_task():
    '''Solution générée pour: {task}'''
    # Implémentation basée sur le contexte
    result = process_data()
    return result

def process_data():
    '''Traiter les données'''
    return "Résultat du traitement"
        """

        solution_content = f"J'ai généré une solution pour: {task}. Voici mon approche: {context[:200] if context else 'Approche standard'}"

        self.status = "idle"
        self.metrics["solutions_generated"] += 1

        return Message(
            from_agent=self.agent_type,
            to_agent=AgentType.ARBITER,
            message_type=MessageType.SOLUTION,
            content=solution_content,
            code_content=code_solution,
            metadata={
                "quality_score": 0.85,
                "confidence": 0.9,
                "approach": "standard",
            },
        )

    def update_metrics(self, quality_score: float, response_time: int):
        """Met à jour les métriques de l'agent."""
        self.metrics["avg_quality_score"] = (
            (self.metrics["avg_quality_score"] + quality_score) / 2
        )
        self.metrics["response_time_ms"] = response_time
        self.metrics["success_rate"] = min(1.0, self.metrics["success_rate"] + 0.05)


class ArbiterAgent:
    """Agent Arbitre qui compare et choisit la meilleure solution."""

    def __init__(self):
        self.agent_type = AgentType.ARBITER
        self.status = "idle"
        self.decisions_made = 0
        self.metrics = {
            "avg_decision_quality": 0.0,
            "decisions_made": 0,
            "response_time_ms": 0,
        }

    def compare_solutions(
        self, solution_a: Message, solution_b: Message
    ) -> Dict:
        """
        Compare deux solutions et choisit la meilleure.
        """
        self.status = "comparing"
        logger.info("Arbitre compare les solutions...")

        # Évaluation simple basée sur les métadonnées
        score_a = solution_a.metadata.get("quality_score", 0.5)
        score_b = solution_b.metadata.get("quality_score", 0.5)

        if score_a > score_b:
            selected = "coder_a"
            justification = f"Solution A a un score de qualité supérieur ({score_a:.2f} vs {score_b:.2f})"
        elif score_b > score_a:
            selected = "coder_b"
            justification = f"Solution B a un score de qualité supérieur ({score_b:.2f} vs {score_a:.2f})"
        else:
            selected = "hybrid"
            justification = "Les deux solutions sont équivalentes, fusion recommandée"

        decision = {
            "decision_id": str(uuid.uuid4()),
            "selected_solution": selected,
            "justification": justification,
            "score_a": score_a,
            "score_b": score_b,
            "quality_score": max(score_a, score_b),
            "timestamp": datetime.utcnow().isoformat(),
        }

        self.status = "idle"
        self.decisions_made += 1
        self.metrics["decisions_made"] = self.decisions_made
        self.metrics["avg_decision_quality"] = (
            (self.metrics["avg_decision_quality"] + decision["quality_score"]) / 2
        )

        logger.info(f"Décision: {selected} - {justification}")
        return decision


class MultiAgentSystem:
    """Système multi-agents complet."""

    def __init__(self):
        self.coder_a = CoderAgent(AgentType.CODER_A)
        self.coder_b = CoderAgent(AgentType.CODER_B)
        self.arbiter = ArbiterAgent()
        self.messages: List[Message] = []
        self.decisions: List[Dict] = []
        self.iteration = 0

    def run_iteration(self, task: str, context: str = "") -> Dict:
        """
        Exécute une itération complète du système multi-agents.
        """
        self.iteration += 1
        logger.info(f"\n{'='*60}")
        logger.info(f"Itération {self.iteration}: {task}")
        logger.info(f"{'='*60}")

        # Étape 1: Coder A génère une solution
        solution_a = self.coder_a.generate_solution(task, context)
        self.messages.append(solution_a)
        logger.info(f"✓ Coder A a généré une solution (ID: {solution_a.message_id})")

        # Étape 2: Coder B génère une solution
        solution_b = self.coder_b.generate_solution(task, context)
        self.messages.append(solution_b)
        logger.info(f"✓ Coder B a généré une solution (ID: {solution_b.message_id})")

        # Étape 3: Arbitre compare et décide
        decision = self.arbiter.compare_solutions(solution_a, solution_b)
        self.decisions.append(decision)
        logger.info(f"✓ Arbitre a pris une décision (ID: {decision['decision_id']})")

        # Étape 4: Feedback
        feedback_message = Message(
            from_agent=AgentType.ARBITER,
            to_agent=AgentType.CODER_A if decision["selected_solution"] == "coder_b" else AgentType.CODER_B,
            message_type=MessageType.FEEDBACK,
            content=decision["justification"],
            metadata={"iteration": self.iteration},
        )
        self.messages.append(feedback_message)

        # Mettre à jour les métriques
        self.coder_a.update_metrics(decision["score_a"], 1000)
        self.coder_b.update_metrics(decision["score_b"], 1200)

        return {
            "iteration": self.iteration,
            "task": task,
            "solution_a_id": solution_a.message_id,
            "solution_b_id": solution_b.message_id,
            "decision": decision,
            "messages_count": len(self.messages),
        }

    def get_session_summary(self) -> Dict:
        """Retourne un résumé de la session."""
        return {
            "iterations": self.iteration,
            "total_messages": len(self.messages),
            "total_decisions": len(self.decisions),
            "coder_a_metrics": self.coder_a.metrics,
            "coder_b_metrics": self.coder_b.metrics,
            "arbiter_metrics": self.arbiter.metrics,
            "decisions": self.decisions,
        }

    def export_messages(self) -> List[Dict]:
        """Exporte tous les messages."""
        return [msg.to_dict() for msg in self.messages]


def main():
    """Test du système multi-agents."""
    system = MultiAgentSystem()

    # Exécuter quelques itérations
    tasks = [
        "Créer une fonction de tri optimisée",
        "Implémenter un système de cache",
        "Optimiser la gestion de la mémoire",
    ]

    for task in tasks:
        result = system.run_iteration(task, "Contexte: Optimisation de performance")
        print(f"\nRésultat itération {result['iteration']}: {result['decision']['selected_solution']}")

    # Résumé
    summary = system.get_session_summary()
    print(f"\n{'='*60}")
    print("RÉSUMÉ DE SESSION")
    print(f"{'='*60}")
    print(f"Itérations: {summary['iterations']}")
    print(f"Messages totaux: {summary['total_messages']}")
    print(f"Décisions: {summary['total_decisions']}")
    print(f"Qualité moyenne Coder A: {summary['coder_a_metrics']['avg_quality_score']:.2f}")
    print(f"Qualité moyenne Coder B: {summary['coder_b_metrics']['avg_quality_score']:.2f}")


if __name__ == "__main__":
    main()
