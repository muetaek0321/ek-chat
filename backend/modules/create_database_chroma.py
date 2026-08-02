import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_core.embeddings import Embeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from tqdm import tqdm

# 環境変数の読み込み
load_dotenv()


def get_embedding(mode: str) -> Embeddings:
    """Embeddingモデルの読み込み

    Args:
        mode (str): Embeddingモデルの種類（"huggingface"または"gemini"）

    Returns:
        Embeddings: 指定されたEmbeddingモデルのインスタンス
    """

    # Embeddingモデルの読み込み
    if mode == "huggingface":
        embedding = HuggingFaceEmbeddings(
            model_name="",
            model_kwargs={"device": "cuda", "trust_remote_code": True},
        )
    elif mode == "gemini":
        embedding = GoogleGenerativeAIEmbeddings(
            model="gemini-embedding-2", output_dimensionality=1536 * 2
        )
    else:
        raise ValueError(f"Invalid EMBEDDING_MODE: {mode}")

    return embedding


def create_database() -> None:
    """データベースの作成"""
    # データ格納先のディレクトリ
    data_dir = Path(os.getenv("DATA_DIR", "data"))
    persist_directory = data_dir / "chroma"

    # Embeddingモデルの読み込み
    embedding = get_embedding(os.getenv("EMBEDDING_MODE", "gemini"))

    # ChromaDBの作成
    vectorstore = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
        collection_name="elephants",
    )

    # 楽曲のデータをベクトル化して保存
    song_data_pathlist = list((data_dir / "elephantkashimashi" / "songs").iterdir())
    for song_data_path in tqdm(song_data_pathlist, desc="songs"):
        # 楽曲のデータをベクトル化して保存
        docs = TextLoader(song_data_path, encoding="utf-8").load()

        vectorstore.add_documents(docs)

        time.sleep(10)  # 10秒待機（API制限回避のため）


if __name__ == "__main__":
    # データベースの作成
    # create_database()

    ### test ###
    question = "「今宵の月のように」はどんな曲？"

    # データ格納先のディレクトリ
    data_dir = Path(os.getenv("DATA_DIR", "data"))
    persist_directory = data_dir / "chroma"

    # Embeddingモデルの読み込み
    embedding = get_embedding(os.getenv("EMBEDDING_MODE", "gemini"))

    # ベクトルDBから検索
    vectorstore = Chroma(
        embedding_function=embedding,
        persist_directory=persist_directory,
        collection_name="elephants",
    )
    docs = vectorstore.similarity_search(query=question, k=3)

    for index, doc in enumerate(docs):
        print(f"{index + 1}: \n{doc.page_content}\n")
