"""
Script d'initialisation des modèles de test.
Crée des modèles de base sans dépendances externes.
"""

import json
import os
from datetime import datetime


def create_test_models():
    """Crée des modèles de test dans base_models/."""
    
    base_models_dir = "base_models"
    if not os.path.exists(base_models_dir):
        os.makedirs(base_models_dir)
    
    print("\n" + "=" * 80)
    print("🤖 INITIALISATION DES MODÈLES DE TEST".center(80))
    print("=" * 80)
    
    # Modèle 1: GPT-2 simulé
    gpt2_dir = os.path.join(base_models_dir, "gpt2-test")
    if not os.path.exists(gpt2_dir):
        os.makedirs(gpt2_dir)
        
        config = {
            "architectures": ["GPT2LMHeadModel"],
            "attention_probs_dropout_prob": 0.1,
            "bos_token_id": 50256,
            "eos_token_id": 50256,
            "hidden_act": "gelu",
            "hidden_dropout_prob": 0.1,
            "hidden_size": 768,
            "initializer_range": 0.02,
            "intermediate_size": 3072,
            "layer_norm_eps": 1e-12,
            "max_position_embeddings": 1024,
            "model_type": "gpt2",
            "n_head": 12,
            "n_layer": 12,
            "n_positions": 1024,
            "num_labels": 1,
            "output_past": True,
            "pad_token_id": 50256,
            "summary_activation": None,
            "summary_first_dropout": 0.1,
            "summary_proj_to_labels": True,
            "summary_type": "cls_index",
            "summary_use_proj": True,
            "vocab_size": 50257,
        }
        
        with open(os.path.join(gpt2_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        # Créer un fichier model.json simulé
        model_data = {
            "model_type": "gpt2",
            "architecture": "GPT2LMHeadModel",
            "parameters": 124440064,
            "vocab_size": 50257,
            "max_sequence_length": 1024,
            "hidden_size": 768,
            "num_layers": 12,
            "num_heads": 12,
        }
        
        with open(os.path.join(gpt2_dir, "model.json"), "w") as f:
            json.dump(model_data, f, indent=2)
        
        print(f"\n✓ Modèle créé: gpt2-test")
        print(f"  📁 Localisation: {gpt2_dir}")
        print(f"  📊 Paramètres: 124,440,064")
        print(f"  🔤 Vocab size: 50,257")
    
    # Modèle 2: Llama-2 simulé
    llama_dir = os.path.join(base_models_dir, "llama2-test")
    if not os.path.exists(llama_dir):
        os.makedirs(llama_dir)
        
        config = {
            "architectures": ["LlamaForCausalLM"],
            "attention_dropout": 0.0,
            "bos_token_id": 1,
            "eos_token_id": 2,
            "hidden_act": "silu",
            "hidden_size": 4096,
            "initializer_range": 0.02,
            "intermediate_size": 11008,
            "max_position_embeddings": 2048,
            "model_type": "llama",
            "num_attention_heads": 32,
            "num_hidden_layers": 32,
            "num_key_value_heads": 32,
            "pad_token_id": 0,
            "pretraining_tp": 1,
            "rms_norm_eps": 1e-06,
            "rope_scaling": None,
            "rope_theta": 10000.0,
            "tie_word_embeddings": False,
            "torch_dtype": "float16",
            "transformers_version": "4.30.0.dev0",
            "use_cache": True,
            "vocab_size": 32000,
        }
        
        with open(os.path.join(llama_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        model_data = {
            "model_type": "llama",
            "architecture": "LlamaForCausalLM",
            "parameters": 6738415616,
            "vocab_size": 32000,
            "max_sequence_length": 2048,
            "hidden_size": 4096,
            "num_layers": 32,
            "num_heads": 32,
        }
        
        with open(os.path.join(llama_dir, "model.json"), "w") as f:
            json.dump(model_data, f, indent=2)
        
        print(f"\n✓ Modèle créé: llama2-test")
        print(f"  📁 Localisation: {llama_dir}")
        print(f"  📊 Paramètres: 6,738,415,616")
        print(f"  🔤 Vocab size: 32,000")
    
    # Modèle 3: Mistral simulé
    mistral_dir = os.path.join(base_models_dir, "mistral-test")
    if not os.path.exists(mistral_dir):
        os.makedirs(mistral_dir)
        
        config = {
            "architectures": ["MistralForCausalLM"],
            "attention_dropout": 0.0,
            "bos_token_id": 1,
            "eos_token_id": 2,
            "hidden_act": "silu",
            "hidden_size": 4096,
            "initializer_range": 0.02,
            "intermediate_size": 14336,
            "max_position_embeddings": 32768,
            "model_type": "mistral",
            "num_attention_heads": 32,
            "num_hidden_layers": 32,
            "num_key_value_heads": 8,
            "rms_norm_eps": 1e-05,
            "rope_theta": 10000.0,
            "sliding_window": 4096,
            "tie_word_embeddings": False,
            "vocab_size": 32000,
        }
        
        with open(os.path.join(mistral_dir, "config.json"), "w") as f:
            json.dump(config, f, indent=2)
        
        model_data = {
            "model_type": "mistral",
            "architecture": "MistralForCausalLM",
            "parameters": 7325625344,
            "vocab_size": 32000,
            "max_sequence_length": 32768,
            "hidden_size": 4096,
            "num_layers": 32,
            "num_heads": 32,
        }
        
        with open(os.path.join(mistral_dir, "model.json"), "w") as f:
            json.dump(model_data, f, indent=2)
        
        print(f"\n✓ Modèle créé: mistral-test")
        print(f"  📁 Localisation: {mistral_dir}")
        print(f"  📊 Paramètres: 7,325,625,344")
        print(f"  🔤 Vocab size: 32,000")
    
    print("\n" + "=" * 80)
    print("✅ Modèles de test initialisés avec succès!".center(80))
    print("=" * 80)
    
    print("\n📚 Prochaines étapes:")
    print("  1. Lancer: python orchestrator.py --choose-model --topic 'Python'")
    print("  2. Choisir un modèle dans le menu")
    print("  3. L'entraînement commencera automatiquement")
    
    print("\n" + "=" * 80 + "\n")


if __name__ == "__main__":
    create_test_models()
