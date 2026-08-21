# ek-chat Backend

ek-chat アプリケーションのバックエンド API サーバーです。FastAPI を利用して構築されており、各種 LLM による返答生成、Chroma を用いた RAG（検索拡張生成）、チャットセッションおよびシステムプロンプトの管理を行います。

---

## 主な機能

- **RESTful API の提供**: FastAPI による高速・型安全なエンドポイント
- **マルチ LLM サポート**:
  - **Gemini(API)**: `langchain-google-genai`（Thinking パラメータ調整可能）
  - **Gemma4:E2B**: Hugging Face `transformers` + `accelerate`（Speculative Decoding: 補助モデル連携）
  - **Gemma4:12B**: `llama-cpp-python`（`ChatLlamaCpp`）による量子化 GGUF モデル推論
  - **Qwen3.8:27B / Muse-Glimmer:30B**: Ollama ローカル推論連携（`langchain-ollama`）
  - **Ollama(cloud)**: Ollama Cloud 経由でのリモート推論
- **RAG（検索拡張生成）機能**:
  - Chroma ベクトルデータベースと連携し、ユーザー入力に応じたドキュメント検索およびプロンプトへのコンテキスト注入
  - Embedding 切り替え（Hugging Face ローカルモデル `ruri-v3-310m` / Gemini `gemini-embedding-2`）
- **チャット履歴・システムプロンプト管理**:
  - JSON ファイルによる会話履歴の永続化
  - Markdown ファイル（`system_prompt.md`）によるシステムプロンプトの永続化・動的更新
- **モデルパラメータ動的反映**:
  - Temperature、Thinking Budget の設定およびモデル切り替え時のメモリ・キャッシュ解放

---

## セットアップ

### 必要要件

- Python >= 3.13
- パッケージマネージャ [uv](https://github.com/astral-sh/uv)
- (推奨) CUDA 12.8 対応の NVIDIA GPU（ローカルモデル実行時）

### 依存関係のインストール

`backend` ディレクトリへ移動し、`uv` で依存関係を同期します。

```bash
cd backend
uv sync
```

### 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、必要な設定を記述します。

```bash
# Linux/macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env

# Windows (Command Prompt)
copy .env.example .env
```

| 変数名 | 説明 | 既定値 / 設定例 |
|---|---|---|
| `ENVIRON` | 実行環境設定 (`dev` でデバッグログ有効) | `dev` |
| `DATA_DIR` | チャット履歴・モデル・Chroma DB などの保存先ディレクトリ | `./develop` |
| `CUDA_VISIBLE_DEVICES` | 使用する GPU デバイス番号 | `0` |
| `HF_HOME` | Hugging Face モデルキャッシュ先パス | `./develop/models` |
| `CHAT_MODEL` | 起動時に初期選択されるモデル名 | `Gemini(API)` |
| `GOOGLE_API_KEY` | Gemini API を使用する場合の API キー | `your-google-api-key` |
| `GEMINI_MODEL` | Gemini API で使用するモデル名 | `gemini-2.5-flash` |
| `OLLAMA_API_KEY` | Ollama Cloud を使用する場合の API キー | `your-ollama-api-key` |
| `OLLAMA_CLOUD_MODEL` | Ollama Cloud で使用するモデル名 | `gpt-oss:120b` |
| `EMBEDDING_MODE` | Embedding モデルの指定 (`huggingface` または `gemini`) | `huggingface` |

---

## 起動方法

### 開発サーバーの起動

```bash
uv run uvicorn main:app --reload
```

または `main.py` を直接実行します。

```bash
uv run python main.py
```

サーバーはデフォルトで `http://localhost:8000` にて起動します。
API 仕様書（Swagger UI）は `http://localhost:8000/docs` で確認できます。

---

## API エンドポイント一覧

| メソッド | パス | 説明 | リクエストパラメータ / Body | レスポンス |
|---|---|---|---|---|
| `GET` | `/` | Swagger UI (`/docs`) へリダイレクト | - | `RedirectResponse` |
| `GET` | `/init` | 保存済みチャット一覧の取得 | - | `ChatInfoList` |
| `PUT` | `/new` | 新規チャットの作成 | - | `ChatInfo` |
| `DELETE` | `/delete` | 指定チャットの削除 | `chat_id` (Query) | 204 No Content |
| `GET` | `/history` | 指定チャットの履歴を取得 | `chat_id` (Query) | `ChatHistory` |
| `GET` | `/settings` | システムプロンプトおよびモデル一覧設定を取得 | - | `SettingsResponse` |
| `PATCH` | `/system_prompt` | システムプロンプトの作成・更新 | `SystemPromptText` (Body) | 204 No Content |
| `PATCH` | `/model` | チャットモデルおよびパラメータの変更 | `SelectedChatModel` (Body) | 204 No Content |
| `POST` | `/chat` | ユーザー入力に対する応答生成 (RAG 適用) | `ChatMessage` (Body) | `GenerateChatResponse` |

---

## データ保存構造

`DATA_DIR`（デフォルト: `./develop`）配下のディレクトリ構成です。

```text
develop/
├── chat_history/              # チャット履歴 JSON（<chat_id>.json）
├── system_prompt.md           # システムプロンプト
├── chroma/                    # Chroma ベクトルストア
├── models/                    # ローカルモデル・Embedding モデル
└── elephantkashimashi/        # RAG 投入元データ
```

---

## 開発・運用コマンド

```bash
# 静的コードチェック (Ruff)
uv run ruff check .

# コードフォーマット (Ruff)
uv run ruff format .

# テスト実行 (Pytest)
uv run pytest

# RAG ベクトルデータベースの作成
uv run python modules/database/create_database_chroma.py
```

---

## 注意点

- **GPU メモリ管理**:
  - モデル切り替え時には明示的にメモリ解放（`gc.collect()`, `torch.cuda.empty_cache()`）を行っていますが、複数の大型ローカルモデルを扱う場合は VRAM 容量にご注意ください。
- **RAG データベース作成**:
  - `create_database_chroma.py` の実行には `DATA_DIR/elephantkashimashi` 配下に元データが必要です。

---

### Author
- *[muetaek0321](https://github.com/muetaek0321)*
- *Gemini 3.7 Flash*
