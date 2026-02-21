"""
API HTTP locale pour utiliser le modèle LLM entraîné.
Permet d'utiliser le modèle indépendamment d'UnityIAPro.

À QUOI ÇA SERT :
- Générer du code basé sur des prompts
- Analyser du code (qualité, sécurité, performance)
- Comparer deux solutions de code
- Entraîner le modèle avec de nouvelles données
- Exporter le modèle au format Ollama (GGUF)

ENDPOINTS :
- GET /health : Vérifier l'état de l'API
- GET /model/info : Obtenir les infos du modèle
- POST /generate : Générer du code
- POST /analyze : Analyser du code
- POST /compare : Comparer deux solutions
- POST /train : Entraîner le modèle
- POST /export : Exporter le modèle
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import logging
import json
from datetime import datetime
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration globale
config = {
    "model_name": "llama2-unity",
    "max_tokens_default": 512,
    "temperature_default": 0.7,
    "top_p_default": 0.9,
    "host": "127.0.0.1",
    "port": 8000,
}

app = FastAPI(
    title="IAtrainer Model API",
    description="API locale pour générer, analyser et entraîner des modèles LLM. Génère du code, analyse la qualité, compare les solutions, entraîne avec de nouvelles données, exporte en format Ollama.",
    version="1.0.0",
)


# Modèles Pydantic
class GenerateRequest(BaseModel):
    """Requête de génération de code."""
    prompt: str
    max_tokens: int = 512
    temperature: float = 0.7
    top_p: float = 0.9


class GenerateResponse(BaseModel):
    """Réponse de génération."""
    generated_code: str
    tokens_used: int
    model: str
    timestamp: str


class AnalyzeRequest(BaseModel):
    """Requête d'analyse de code."""
    code: str
    analysis_type: str = "quality"  # quality, security, performance, style


class AnalyzeResponse(BaseModel):
    """Réponse d'analyse."""
    analysis: dict
    score: float
    recommendations: List[str]
    timestamp: str


class CompareRequest(BaseModel):
    """Requête de comparaison de code."""
    code_a: str
    code_b: str


class CompareResponse(BaseModel):
    """Réponse de comparaison."""
    winner: str  # "a", "b", ou "tie"
    score_a: float
    score_b: float
    justification: str
    timestamp: str


class TrainingData(BaseModel):
    """Données d'entraînement."""
    topic: str
    content: str
    code_examples: List[str]


# État du modèle
model_state = {
    "is_loaded": False,
    "model_name": config["model_name"],
    "training_iterations": 0,
    "last_trained": None,
    "training_data_count": 0,
}


@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage."""
    logger.info("=" * 70)
    logger.info("API IAtrainer démarrée")
    logger.info("=" * 70)
    logger.info(f"Modèle: {model_state['model_name']}")
    logger.info(f"Configuration:")
    logger.info(f"  - Max tokens par défaut: {config['max_tokens_default']}")
    logger.info(f"  - Température par défaut: {config['temperature_default']}")
    logger.info(f"  - Top-P par défaut: {config['top_p_default']}")
    logger.info("=" * 70)
    model_state["is_loaded"] = True


@app.get("/")
async def root():
    """Page d'accueil avec documentation."""
    return {
        "title": "IAtrainer Model API",
        "description": "API locale pour générer, analyser et entraîner des modèles LLM",
        "docs": "http://localhost:8000/docs",
        "endpoints": {
            "GET /health": "Vérifier l'état de l'API",
            "GET /model/info": "Obtenir les informations du modèle",
            "POST /generate": "Générer du code",
            "POST /analyze": "Analyser du code",
            "POST /compare": "Comparer deux solutions",
            "POST /train": "Entraîner le modèle",
            "POST /export": "Exporter le modèle",
            "GET /config": "Voir la configuration actuelle",
            "POST /config/update": "Mettre à jour la configuration",
        },
    }


@app.get("/health")
async def health_check():
    """Vérifier l'état de l'API."""
    return {
        "status": "healthy",
        "model_loaded": model_state["is_loaded"],
        "model": model_state["model_name"],
        "training_iterations": model_state["training_iterations"],
    }


@app.get("/model/info")
async def get_model_info():
    """Obtenir les informations du modèle."""
    return {
        "name": model_state["model_name"],
        "is_loaded": model_state["is_loaded"],
        "training_iterations": model_state["training_iterations"],
        "last_trained": model_state["last_trained"],
        "training_data_count": model_state["training_data_count"],
    }


@app.get("/config")
async def get_config():
    """Obtenir la configuration actuelle."""
    return {
        "model_name": config["model_name"],
        "max_tokens_default": config["max_tokens_default"],
        "temperature_default": config["temperature_default"],
        "top_p_default": config["top_p_default"],
        "host": config["host"],
        "port": config["port"],
    }


@app.post("/config/update")
async def update_config(
    model_name: Optional[str] = None,
    max_tokens: Optional[int] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
):
    """Mettre à jour la configuration."""
    if model_name:
        config["model_name"] = model_name
        model_state["model_name"] = model_name
        logger.info(f"Modèle changé en: {model_name}")

    if max_tokens:
        config["max_tokens_default"] = max_tokens
        logger.info(f"Max tokens changé en: {max_tokens}")

    if temperature is not None:
        config["temperature_default"] = temperature
        logger.info(f"Température changée en: {temperature}")

    if top_p is not None:
        config["top_p_default"] = top_p
        logger.info(f"Top-P changé en: {top_p}")

    return {
        "status": "updated",
        "config": config,
    }


@app.post("/generate", response_model=GenerateResponse)
async def generate_code(request: GenerateRequest):
    """
    Génère du code basé sur un prompt.
    """
    if not model_state["is_loaded"]:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    logger.info(f"Génération de code pour: {request.prompt[:50]}...")

    # Simuler la génération (remplacer par un vrai modèle)
    generated_code = f"""# Code généré pour: {request.prompt}
# Température: {request.temperature}
# Max tokens: {request.max_tokens}

def generated_function():
    '''Fonction générée automatiquement'''
    # Implémentation basée sur le prompt
    result = process_input()
    return result

def process_input():
    '''Traiter l'entrée'''
    return "Résultat du traitement"
"""

    return GenerateResponse(
        generated_code=generated_code,
        tokens_used=min(request.max_tokens, len(generated_code.split())),
        model=model_state["model_name"],
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_code(request: AnalyzeRequest):
    """
    Analyse du code (qualité, sécurité, performance, style).
    """
    if not model_state["is_loaded"]:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    logger.info(f"Analyse de code ({request.analysis_type}): {len(request.code)} caractères")

    # Simuler l'analyse
    analysis = {
        "type": request.analysis_type,
        "lines_of_code": len(request.code.split("\n")),
        "functions": request.code.count("def "),
        "complexity": "medium",
    }

    recommendations = [
        "Ajouter des docstrings aux fonctions",
        "Améliorer la gestion des erreurs",
        "Optimiser les boucles",
    ]

    # Calculer un score (0-100)
    score = 75.0

    return AnalyzeResponse(
        analysis=analysis,
        score=score,
        recommendations=recommendations,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/compare", response_model=CompareResponse)
async def compare_code(request: CompareRequest):
    """
    Compare deux solutions de code.
    """
    if not model_state["is_loaded"]:
        raise HTTPException(status_code=503, detail="Modèle non chargé")

    logger.info("Comparaison de deux solutions de code")

    # Simuler la comparaison
    len_a = len(request.code_a)
    len_b = len(request.code_b)

    score_a = 0.85
    score_b = 0.78

    if score_a > score_b:
        winner = "a"
        justification = "La solution A est plus efficace et lisible"
    elif score_b > score_a:
        winner = "b"
        justification = "La solution B est plus performante"
    else:
        winner = "tie"
        justification = "Les deux solutions sont équivalentes"

    return CompareResponse(
        winner=winner,
        score_a=score_a,
        score_b=score_b,
        justification=justification,
        timestamp=datetime.utcnow().isoformat(),
    )


@app.post("/train")
async def train_model(data: TrainingData):
    """
    Entraîne le modèle avec de nouvelles données.
    """
    logger.info(f"Entraînement du modèle sur le sujet: {data.topic}")
    logger.info(f"Données: {len(data.content)} caractères, {len(data.code_examples)} exemples")

    # Simuler l'entraînement
    model_state["training_iterations"] += 1
    model_state["last_trained"] = datetime.utcnow().isoformat()
    model_state["training_data_count"] += len(data.code_examples)

    return {
        "status": "training_completed",
        "iterations": model_state["training_iterations"],
        "data_count": model_state["training_data_count"],
        "timestamp": model_state["last_trained"],
    }


@app.post("/export")
async def export_model(format: str = "json"):
    """
    Exporte le modèle entraîné pour Ollama ou JSON.
    """
    logger.info(f"Export du modèle (format: {format})")

    export_data = {
        "model_name": model_state["model_name"],
        "training_iterations": model_state["training_iterations"],
        "training_data_count": model_state["training_data_count"],
        "last_trained": model_state["last_trained"],
        "export_timestamp": datetime.utcnow().isoformat(),
        "format": format,
    }

    timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')

    if format == "gguf":
        export_path = f"model_{timestamp}.gguf.json"
        export_data["ollama_compatible"] = True
        export_data["instructions"] = "Convertir au GGUF et charger dans Ollama"
    else:
        export_path = f"model_export_{timestamp}.json"

    with open(export_path, "w") as f:
        json.dump(export_data, f, indent=2)

    logger.info(f"Modèle exporté: {export_path}")

    return {
        "status": "exported",
        "file": export_path,
        "format": format,
        "data": export_data,
    }


def interactive_configuration():
    """Configuration interactive en console."""
    print("\n" + "=" * 70)
    print("CONFIGURATION DE L'API IATRAINER")
    print("=" * 70)

    while True:
        print("\nOptions disponibles:")
        print("1. Voir la configuration actuelle")
        print("2. Changer le nom du modèle")
        print("3. Changer le nombre de tokens par défaut")
        print("4. Changer la température par défaut")
        print("5. Changer le Top-P par défaut")
        print("6. Changer le host")
        print("7. Changer le port")
        print("8. Démarrer l'API")
        print("9. Quitter")

        choice = input("\nChoisissez une option (1-9): ").strip()

        if choice == "1":
            print("\nConfiguration actuelle:")
            for key, value in config.items():
                print(f"  {key}: {value}")

        elif choice == "2":
            new_name = input("Nouveau nom du modèle (ex: llama2-unity): ").strip()
            if new_name:
                config["model_name"] = new_name
                model_state["model_name"] = new_name
                print(f"✓ Modèle changé en: {new_name}")

        elif choice == "3":
            try:
                new_tokens = int(input("Nouveau nombre de tokens par défaut (ex: 512): ").strip())
                config["max_tokens_default"] = new_tokens
                print(f"✓ Max tokens changé en: {new_tokens}")
            except ValueError:
                print("✗ Veuillez entrer un nombre valide")

        elif choice == "4":
            try:
                new_temp = float(input("Nouvelle température par défaut (0.0-2.0, ex: 0.7): ").strip())
                if 0.0 <= new_temp <= 2.0:
                    config["temperature_default"] = new_temp
                    print(f"✓ Température changée en: {new_temp}")
                else:
                    print("✗ La température doit être entre 0.0 et 2.0")
            except ValueError:
                print("✗ Veuillez entrer un nombre valide")

        elif choice == "5":
            try:
                new_top_p = float(input("Nouveau Top-P par défaut (0.0-1.0, ex: 0.9): ").strip())
                if 0.0 <= new_top_p <= 1.0:
                    config["top_p_default"] = new_top_p
                    print(f"✓ Top-P changé en: {new_top_p}")
                else:
                    print("✗ Le Top-P doit être entre 0.0 et 1.0")
            except ValueError:
                print("✗ Veuillez entrer un nombre valide")

        elif choice == "6":
            new_host = input("Nouveau host (ex: 127.0.0.1 ou 0.0.0.0): ").strip()
            if new_host:
                config["host"] = new_host
                print(f"✓ Host changé en: {new_host}")

        elif choice == "7":
            try:
                new_port = int(input("Nouveau port (ex: 8000): ").strip())
                if 1 <= new_port <= 65535:
                    config["port"] = new_port
                    print(f"✓ Port changé en: {new_port}")
                else:
                    print("✗ Le port doit être entre 1 et 65535")
            except ValueError:
                print("✗ Veuillez entrer un nombre valide")

        elif choice == "8":
            print("\n" + "=" * 70)
            print("DÉMARRAGE DE L'API")
            print("=" * 70)
            print(f"Host: {config['host']}")
            print(f"Port: {config['port']}")
            print(f"Modèle: {config['model_name']}")
            print("=" * 70)
            print("\nPour accéder à l'API:")
            print(f"  - Documentation: http://{config['host']}:{config['port']}/docs")
            print(f"  - Health check: http://{config['host']}:{config['port']}/health")
            print(f"  - Config: http://{config['host']}:{config['port']}/config")
            print("\nAppuyez sur CTRL+C pour arrêter l'API\n")

            import uvicorn
            uvicorn.run(
                app,
                host=config["host"],
                port=config["port"],
                log_level="info",
            )

        elif choice == "9":
            print("Au revoir!")
            break

        else:
            print("✗ Option invalide, veuillez choisir entre 1 et 9")


if __name__ == "__main__":
    interactive_configuration()
