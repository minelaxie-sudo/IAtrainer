"""
Client tRPC pour envoyer les données d'entraînement à UnityIAPro.
"""

import httpx
import json
import logging
from typing import Dict, Optional, List
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class TRPCClient:
    """Client pour communiquer avec UnityIAPro via tRPC."""

    def __init__(self, base_url: str = "http://localhost:3000/api/trpc"):
        self.base_url = base_url
        self.client = httpx.Client()
        self.session_id: Optional[str] = None

    def call_procedure(self, procedure: str, input_data: Dict) -> Dict:
        """
        Appelle une procédure tRPC.
        """
        try:
            url = f"{self.base_url}/{procedure}"
            response = self.client.post(url, json={"json": input_data})
            response.raise_for_status()
            result = response.json()
            logger.info(f"✓ Procédure {procedure} exécutée avec succès")
            return result.get("result", {}).get("data", {})
        except Exception as e:
            logger.error(f"✗ Erreur lors de l'appel à {procedure}: {e}")
            return {}

    def create_session(
        self,
        name: str,
        model_name: str,
        description: str = "",
        config: Optional[Dict] = None,
    ) -> str:
        """
        Crée une nouvelle session d'entraînement.
        """
        input_data = {
            "name": name,
            "modelName": model_name,
            "description": description,
            "config": config or {},
        }
        result = self.call_procedure("sessions.create", input_data)
        self.session_id = result.get("sessionId")
        logger.info(f"Session créée: {self.session_id}")
        return self.session_id

    def update_session_status(self, status: str) -> bool:
        """
        Met à jour le statut de la session.
        """
        if not self.session_id:
            logger.error("Aucune session active")
            return False

        input_data = {
            "sessionId": self.session_id,
            "status": status,
        }
        result = self.call_procedure("sessions.updateStatus", input_data)
        return bool(result)

    def update_agent_status(
        self,
        agent_type: str,
        status: str,
        is_active: bool = True,
        metrics: Optional[Dict] = None,
    ) -> bool:
        """
        Met à jour le statut d'un agent.
        """
        if not self.session_id:
            logger.error("Aucune session active")
            return False

        input_data = {
            "sessionId": self.session_id,
            "agentType": agent_type,
            "status": status,
            "isActive": is_active,
            "metrics": metrics or {},
        }
        result = self.call_procedure("agents.updateStatus", input_data)
        return bool(result)

    def send_message(
        self,
        from_agent: str,
        to_agent: str,
        message_type: str,
        content: str,
        code_content: Optional[str] = None,
        metadata: Optional[Dict] = None,
    ) -> str:
        """
        Envoie un message entre agents.
        """
        if not self.session_id:
            logger.error("Aucune session active")
            return ""

        input_data = {
            "sessionId": self.session_id,
            "fromAgent": from_agent,
            "toAgent": to_agent,
            "messageType": message_type,
            "content": content,
            "codeContent": code_content,
            "metadata": metadata or {},
        }
        result = self.call_procedure("messages.create", input_data)
        message_id = result.get("messageId", "")
        logger.info(f"Message envoyé: {message_id}")
        return message_id

    def create_arbitration_decision(
        self,
        iteration_number: int,
        coder_a_solution_id: str,
        coder_b_solution_id: str,
        selected_solution: str,
        justification: str,
    ) -> str:
        """
        Crée une décision d'arbitrage.
        """
        if not self.session_id:
            logger.error("Aucune session active")
            return ""

        input_data = {
            "sessionId": self.session_id,
            "iterationNumber": iteration_number,
            "coderASolutionId": coder_a_solution_id,
            "coderBSolutionId": coder_b_solution_id,
            "selectedSolution": selected_solution,
            "justification": justification,
        }
        result = self.call_procedure("arbitration.create", input_data)
        decision_id = result.get("decisionId", "")
        logger.info(f"Décision créée: {decision_id}")
        return decision_id

    def log_unity_interaction(
        self,
        request_type: str,
        request_payload: Dict,
        response_status: Optional[int] = None,
        response_payload: Optional[Dict] = None,
        error_message: Optional[str] = None,
        execution_time: Optional[int] = None,
    ) -> str:
        """
        Crée un log d'interaction Unity.
        """
        if not self.session_id:
            logger.error("Aucune session active")
            return ""

        input_data = {
            "sessionId": self.session_id,
            "requestType": request_type,
            "requestPayload": request_payload,
            "responseStatus": response_status,
            "responsePayload": response_payload,
            "errorMessage": error_message,
            "executionTime": execution_time,
        }
        result = self.call_procedure("unityLogs.create", input_data)
        log_id = result.get("logId", "")
        logger.info(f"Log créé: {log_id}")
        return log_id

    def create_alert(
        self,
        severity: str,
        title: str,
        description: str,
        metadata: Optional[Dict] = None,
    ) -> str:
        """
        Crée une alerte.
        """
        if not self.session_id:
            logger.error("Aucune session active")
            return ""

        input_data = {
            "sessionId": self.session_id,
            "severity": severity,
            "title": title,
            "description": description,
            "metadata": metadata or {},
        }
        result = self.call_procedure("alerts.create", input_data)
        alert_id = result.get("alertId", "")
        logger.info(f"Alerte créée: {alert_id}")
        return alert_id

    def close(self):
        """Ferme la connexion."""
        self.client.close()


def main():
    """Test du client tRPC."""
    client = TRPCClient()

    try:
        # Créer une session
        session_id = client.create_session(
            name="Test Training Session",
            model_name="llama2-unity",
            description="Session de test",
            config={"max_iterations": 10, "temperature": 0.7},
        )

        if session_id:
            # Mettre à jour le statut de la session
            client.update_session_status("running")

            # Mettre à jour les statuts des agents
            client.update_agent_status("coder_a", "thinking", True, {"confidence": 0.9})
            client.update_agent_status("coder_b", "thinking", True, {"confidence": 0.85})
            client.update_agent_status("arbiter", "idle", True)

            # Envoyer des messages
            msg_a = client.send_message(
                from_agent="coder_a",
                to_agent="arbiter",
                message_type="solution",
                content="Voici ma solution",
                code_content="def solve(): pass",
                metadata={"quality": 0.9},
            )

            msg_b = client.send_message(
                from_agent="coder_b",
                to_agent="arbiter",
                message_type="solution",
                content="Voici ma solution alternative",
                code_content="def solve_alt(): pass",
                metadata={"quality": 0.85},
            )

            # Créer une décision d'arbitrage
            if msg_a and msg_b:
                client.create_arbitration_decision(
                    iteration_number=1,
                    coder_a_solution_id=msg_a,
                    coder_b_solution_id=msg_b,
                    selected_solution="coder_a",
                    justification="Solution A est plus efficace",
                )

            # Logger une interaction Unity
            client.log_unity_interaction(
                request_type="compile_code",
                request_payload={"code": "..."},
                response_status=200,
                response_payload={"result": "success"},
                execution_time=5000,
            )

            # Créer une alerte
            client.create_alert(
                severity="info",
                title="Session démarrée",
                description="La session d'entraînement a démarré",
            )

            # Terminer la session
            client.update_session_status("completed")

    finally:
        client.close()


if __name__ == "__main__":
    main()
