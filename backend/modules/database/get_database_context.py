import os
from pathlib import Path

from langchain_chroma import Chroma

from modules.database.embedding_models import get_embedding

RAG_PROMPT = """\
あなたは提示された情報を元に正確に回答するアシスタントです。
以下の「制約事項」を厳密に守り、「コンテキスト」の情報のみに基づいて「ユーザの質問」に回答してください。

### 制約事項
- 提示されたコンテキストの情報のみを根拠として日本語で回答してください。
- コンテキストに含まれていない事実や予備知識、独自の推測に基づく回答は絶対に行わないでください。
- コンテキストから回答が導き出せない場合は、無理に答えず「提供された情報からは分かりません」と回答してください。
- 回答は簡潔かつ分かりやすく整理して記述してください。

### コンテキスト
{context}

### ユーザの質問
{user_input}
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

    return RAG_PROMPT.format(context=context, user_input=query)
