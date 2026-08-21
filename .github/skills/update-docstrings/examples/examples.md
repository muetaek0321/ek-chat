# Docstring / JSDoc 作成例・テンプレート集

本ドキュメントでは、各言語・フレームワークごとの Docstring / JSDoc の具体的な作成例をまとめています。

---

## 1. Python: 一般的な関数・クラス (Google Style Docstring)

- **適用対象**: 通常のヘルパー関数、ビジネスロジック、サービスクラス、メソッドなど。
- **ポイント**: 
  - 型ヒントが明記されている場合は `Args:` / `Returns:` での型名の重複を避ける。
  - 事前条件、事後条件、発生し得る例外を記載。

```python
def generate_response(
    messages: list[ChatMessage],
    model_name: str,
    temperature: float = 0.7,
) -> str:
    """メッセージ履歴に基づき指定されたLLMモデルを用いて応答テキストを生成する。

    Args:
        messages: 過去のチャットメッセージのリスト。
        model_name: 使用するLLMモデルの識別名。
        temperature: 生成時のランダム性を制御するパラメータ（0.0〜1.0）。

    Returns:
        LLMによって生成された応答文字列。

    Raises:
        ValueError: サポートされていないモデル名が指定された場合。
        APIError: LLM APIとの通信に失敗した場合。
    """
```

---

## 2. Python: FastAPI APIエンドポイント (Swagger UI 向け)

- **適用対象**: `@router.get`, `@router.post`, `@app.get` などの FastAPI パスオペレーション関数。
- **ポイント**:
  - **1行目 (Summary)**: Swagger UI のアコーディオン見出しとして表示されるため、簡潔かつ分かりやすく記述。
  - **2行目以降 (Description)**: Swagger UI 上でリッチテキストとして描画される Markdown（処理フロー、エラー仕様など）を活用。

```python
@router.post(
    "/sessions/{session_id}/messages",
    response_model=MessageResponse,
    status_code=status.HTTP_201_CREATED,
)
async def send_message(
    session_id: str = Path(..., description="対象のチャットセッションID"),
    request: SendMessageRequest = ...,
    db: AsyncSession = Depends(get_db),
) -> MessageResponse:
    """指定されたチャットセッションに新規メッセージを送信し、LLMの応答を取得する。

    クライアントからのメッセージをDBに保存し、設定されたモデルを用いて応答をストリーミングまたは一括生成します。

    ### 処理の流れ
    1. セッションの存在確認およびユーザーのアクセス権チェック
    2. ユーザーメッセージの永続化
    3. LLM API の呼び出しとレスポンスの受信
    4. アシスタントメッセージの保存とレスポンス返却

    ### エラーレスポンス
    - **400 Bad Request**: メッセージ本文が空、または文字数制限を超過している場合
    - **404 Not Found**: 指定された `session_id` が存在しない場合
    - **500 Internal Server Error**: LLM サービスとの通信障害、またはDBエラー
    """
```

---

## 3. TypeScript / JavaScript (JSDoc)

- **適用対象**: Reactコンポーネント、TypeScript/JavaScript のユーティリティ関数、APIクライアントなど。
- **ポイント**:
  - `@param`, `@returns`, `@throws` などの標準JSDocタグを使用。

```typescript
/**
 * ユーザーのチャット履歴を取得し、日付順にソートして返します。
 *
 * @param userId - 取得対象のユーザーID
 * @param limit - 取得する最大件数（デフォルト: 20）
 * @returns ソートされたチャット履歴オブジェクトの配列
 * @throws {NotFoundError} ユーザーが存在しない場合に発生します
 */
export async function fetchUserChats(userId: string, limit: number = 20): Promise<Chat[]> {
```
