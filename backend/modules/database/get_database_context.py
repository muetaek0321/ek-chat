import os
from pathlib import Path

from langchain_chroma import Chroma

from modules.database.embedding_models import get_embedding

RAG_PROMPT = """
あなたは質問応答タスクのアシスタントです。
検索された以下のコンテキストの一部を使って直前に与えられた質問に答えてください。
答えがわからなければ、わからないと答えてください。

コンテキスト:
{context}
"""


def get_context(query: str) -> str:
    """ChromaDBからの検索でコンテキストを作成

    Args:
        query (str): 検索クエリ（ユーザの入力文）

    Return:
        str: 検索結果をまとめたコンテキストデータ
    """
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

    # 類似文書検索
    docs = vectorstore.similarity_search(query=query, k=5)

    context = "\n---------------\n".join([doc.page_content for doc in docs])

    return RAG_PROMPT.format(context=context)
