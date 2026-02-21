"""
API HTTP locale pour utiliser le modèle LLM entraîné.
Permet d'utiliser le modèle indépendamment d'UnityIAPro.
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

app = FastAPI(
    title="IAtrainer Model API",
    description="API locale pour utiliser le modèle LLM entraîné",
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
    "model_name": "llama2-unity",
    "training_iterations": 0,
    "last_trained": None,
    "training_data_count": 0,
}


@app.on_event("startup")
async def startup_event():
    """Initialisation au démarrage."""
    logger.info("API IAtrainer démarrée")
    logger.info(f"Modèle: {model_state['model_name']}")
    model_state["is_loaded"] = True


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


@app.get("/docs")
async def get_documentation():
    """Obtenir la documentation de l'API."""
    return {
        "title": "IAtrainer Model API",
        "version": "1.0.0",
        "endpoints": {
            "GET /health": "Vérifier l'état de l'API",
            "GET /model/info": "Obtenir les informations du modèle",
            "POST /generate": "Générer du code",
            "POST /analyze": "Analyser du code",
            "POST /compare": "Comparer deux solutions",
            "POST /train": "Entraîner le modèle",
            "POST /export": "Exporter le modèle",
        },
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
