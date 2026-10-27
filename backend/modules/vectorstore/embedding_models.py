import os
from pathlib import Path

from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings


def get_embedding(mode: str) -> Embeddings:
    """Embeddingモデルの読み込み

    Args:
        mode (str): Embeddingモデルの種類（"huggingface"または"gemini"）

    Returns:
        Embeddings: 指定されたEmbeddingモデルのインスタンス
    """

    # Embeddingモデルの読み込み
    if mode == "huggingface":
        model_path = Path(os.getenv("DATA_DIR", "./develop")) / "models" / "ruri-v3-310m"
        embedding = HuggingFaceEmbeddings(
            model_name=str(model_path),
            model_kwargs={"device": "cuda", "trust_remote_code": True},
        )
    elif mode == "gemini":
        embedding = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2", output_dimensionality=3072
        )
    else:
        raise ValueError(f"Invalid EMBEDDING_MODE: {mode}")

    return embedding
