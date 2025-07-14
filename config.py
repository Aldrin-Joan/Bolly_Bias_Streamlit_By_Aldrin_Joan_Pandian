import torch

# Model and Inference
MODEL_NAME = "mistralai/Mistral-7B-Instruct-v0.1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
# Paths
DATA_DIR = "data"
OUTPUT_DIR = "outputs"
CHUNK_SIZE = 250