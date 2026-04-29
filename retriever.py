import os
import pickle
from typing import Dict, List

import faiss
from sentence_transformers import SentenceTransformer

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INDEX_PATH = os.path.join(BASE_DIR, "data", "redhat_docs.index")
METADATA_PATH = os.path.join(BASE_DIR, "data", "chunk_metadata.pkl")

_model = None
_index = None
_metadata = None


def load_resources():
    global _model, _index, _metadata

    if _model is None:
        _model = SentenceTransformer("all-MiniLM-L6-v2")

    if _index is None:
        if not os.path.exists(INDEX_PATH):
            raise FileNotFoundError(f"FAISS index not found at {INDEX_PATH}")
        _index = faiss.read_index(INDEX_PATH)

    if _metadata is None:
        if not os.path.exists(METADATA_PATH):
            raise FileNotFoundError(f"Metadata file not found at {METADATA_PATH}")
        with open(METADATA_PATH, "rb") as f:
            _metadata = pickle.load(f)

    return _model, _index, _metadata


# ✅ PRELOAD (OUTSIDE FUNCTION)
load_resources()


def clean_text(text: str) -> str:
    return " ".join(str(text).replace("\n", " ").split())


def is_useful_text(text: str) -> bool:
    if not isinstance(text, str):
        return False

    text = clean_text(text)

    if len(text) < 80:
        return False

    noisy_tokens = ["noarch", ".rpm", "redhat_", "x86_64", "package list", "copyright"]

    if sum(token in text.lower() for token in noisy_tokens) >= 2:
        return False

    return True


def retrieve_documents(query: str, top_k: int = 8, max_results: int = 4) -> List[Dict[str, object]]:
    model, index, metadata = load_resources()

    query_embedding = model.encode([query], normalize_embeddings=True).astype("float32")
    distances, indices = index.search(query_embedding, top_k)

    results = []
    seen = set()

    for rank, idx in enumerate(indices[0], start=1):
        if not (0 <= idx < len(metadata)):
            continue

        item = metadata[idx]

        if isinstance(item, dict):
            text = item.get("chunk_text") or item.get("text") or str(item)
            source = item.get("source") or item.get("title") or "Red Hat documentation"
        else:
            text = str(item)
            source = "Red Hat documentation"

        text = clean_text(text)
        fingerprint = text[:180]

        if fingerprint in seen or not is_useful_text(text):
            continue

        seen.add(fingerprint)

        results.append({
            "rank": rank,
            "score": float(distances[0][rank - 1]),
            "source": source,
            "text": text[:1200]
        })

        if len(results) >= max_results:
            break

    return results