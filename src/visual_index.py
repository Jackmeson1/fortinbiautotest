import json
import os
from typing import List, Tuple

import faiss
import open_clip
import numpy as np
from PIL import Image
import torch


# Default paths
PROJECT_ROOT = os.path.dirname(os.path.dirname(__file__))
BASELINE_DIR = os.path.join(PROJECT_ROOT, "resources", "baseline_images")
INDEX_PATH = os.path.join(PROJECT_ROOT, "resources", "faiss.index")
MAPPING_PATH = INDEX_PATH + ".json"
MODEL_NAME = "ViT-B-32"


def _load_model():
    """Load the CLIP model and preprocessing."""
    model, preprocess = open_clip.create_model_and_transforms(MODEL_NAME, pretrained="openai")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)
    model.eval()
    return model, preprocess, device


def _encode_image(path: str, model, preprocess, device) -> np.ndarray:
    """Encode an image file into a normalized feature vector."""
    image = Image.open(path).convert("RGB")
    tensor = preprocess(image).unsqueeze(0).to(device)
    with torch.no_grad():
        embedding = model.encode_image(tensor)
    embedding = embedding.cpu().numpy().astype("float32")
    faiss.normalize_L2(embedding)
    return embedding


def build_index(image_dir: str = BASELINE_DIR, index_path: str = INDEX_PATH) -> None:
    """Create a FAISS index from images in ``image_dir`` and save it."""
    model, preprocess, device = _load_model()
    image_files = [
        os.path.join(image_dir, f)
        for f in os.listdir(image_dir)
        if f.lower().endswith((".png", ".jpg", ".jpeg"))
    ]
    if not image_files:
        raise ValueError(f"No images found in {image_dir}")

    embeddings = [
        _encode_image(path, model, preprocess, device) for path in image_files
    ]
    matrix = np.vstack(embeddings)

    index = faiss.IndexFlatIP(matrix.shape[1])
    index.add(matrix)
    faiss.write_index(index, index_path)
    with open(MAPPING_PATH, "w") as f:
        json.dump(image_files, f)


# pylint: disable=unused-argument

def search(
    image_path: str, top_k: int = 3, index_path: str = INDEX_PATH
) -> List[Tuple[str, float]]:
    """Return the ``top_k`` most similar baseline images for ``image_path``."""
    if not os.path.exists(index_path) or not os.path.exists(MAPPING_PATH):
        raise FileNotFoundError("Index not built. Call build_index() first.")

    model, preprocess, device = _load_model()
    index = faiss.read_index(index_path)
    with open(MAPPING_PATH, "r") as f:
        image_files = json.load(f)

    query = _encode_image(image_path, model, preprocess, device)
    scores, indices = index.search(query, top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        if 0 <= idx < len(image_files):
            results.append((image_files[idx], float(score)))
    return results


if __name__ == "__main__":
    build_index()
