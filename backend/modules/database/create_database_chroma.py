import os
import sys
from pathlib import Path

# backendフォルダのrootから実行してデータベースを作成するためsys.pathに追加
sys.path.append("./")

from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_community.document_loaders import TextLoader
from tqdm import tqdm

from modules.database.embedding_models import get_embedding
from modules.database.json_to_markdown import songs_json_to_markdown_doc

# 環境変数の読み込み
load_dotenv("./.env")


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
        # 楽曲のjsonデータをmarkdown形式に変換
        doc = songs_json_to_markdown_doc(song_data_path)
        # ベクトル化して保存
        vectorstore.add_documents([doc])

    # その他テキストデータをベクトル化して保存
    song_data_pathlist = list((data_dir / "elephantkashimashi" / "other").iterdir())
    for txt_data_path in tqdm(song_data_pathlist, desc="other"):
        # テキストデータの読み込み
        docs = TextLoader(str(txt_data_path), encoding="cp932").load()
        # カテゴリをメタデータに追加
        for doc in docs:
            doc.metadata["category"] = "other"
        # ベクトル化して保存
        vectorstore.add_documents(docs)


if __name__ == "__main__":
    # このプログラムを実行してデータベースを作成する
    # python .\modules\database\create_database_chroma.py

    # データベースの作成
    create_database()

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
