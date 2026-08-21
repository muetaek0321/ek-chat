# ek-chat

FastAPI バックエンドと Next.js フロントエンドで構成された、LLM・RAG（検索拡張生成）対応のチャットアプリケーションです。

---

## 概要

- **目的**: 外部 API（Gemini API、Ollama Cloud）およびローカル LLM（Gemma 4、Qwen 3.8、Muse-Glimmer 等）を活用し、Chroma ベクトルデータベースによる RAG 機能と組み合わせたチャット機能を提供します。
- **ユーザーができること**:
  - チャットの新規作成、履歴の閲覧・保存・削除
  - AI（assistant）によるコンテキストを踏まえた返答生成（RAG 連携）
  - システムプロンプトの閲覧・編集・保存
  - チャットモデル（API / ローカル / クラウド）の動的切り替え
  - モデルパラメータ（Temperature、Thinking Budget など）の調整
  - テーマ切り替え（Light / Dark）やフォントサイズ設定
- **構成**:
  - **Backend**: FastAPI を用いた RESTful API サーバー。LLM 生成パイプライン、Chroma によるベクトル検索・RAG、履歴や設定のファイル永続化を担当。
  - **Frontend**: Next.js (App Router)、React、Material UI (MUI)、Tailwind CSS によるモダンなチャット UI。

---

## 主な機能

1. **マルチモデル対応**:
   - **Gemini(API)**: `langchain-google-genai` を用いた Gemini API 呼び出し（Thinking 時間調整対応）
   - **Gemma4:E2B**: Hugging Face `transformers` + `accelerate` による Speculative Decoding（補助モデルを用いた高速推論）
   - **Gemma4:12B**: `llama-cpp-python`（`ChatLlamaCpp`）による GGUF 量子化モデル推論
   - **Qwen3.8:27B / Muse-Glimmer:30B**: Ollama ローカル推論との連携
   - **Ollama(cloud)**: Ollama Cloud API を利用したリモート推論
2. **RAG（検索拡張生成）**:
   - Chroma ベクトルデータベース（`langchain-chroma`）から類似ドキュメントを取得し、質問コンテキストとしてモデルへ注入
   - Embedding バックエンドの切り替え（Hugging Face ローカルモデル `ruri-v3-310m` または Google Gemini `gemini-embedding-2`）
3. **チャットセッション管理**:
   - 会話履歴の自動保存（JSON形式）
   - 最初の発言に基づいたタイトルの自動生成
   - 過去セッションの選択・削除
4. **システムプロンプト・設定管理**:
   - UI からのシステムプロンプト即時更新（Markdown 形式で永続化）
   - モデルごとのパラメータ（Temperature、Thinking Budget）の設定・動的反映
5. **UI カスタマイズ**:
   - Light / Dark テーマのサポート
   - フォントサイズ変更（環境変数設定）

---

## 技術スタック

| レイヤー | 主要技術・ライブラリ |
|---|---|
| **Frontend** | Next.js 16.2, React 19.2, TypeScript 5, MUI v9, Tailwind CSS v4, Emotion, Vitest |
| **Backend** | Python >= 3.13, FastAPI, Pydantic v2, Uvicorn, uv |
| **AI / LLM** | LangChain (`langchain-google-genai`, `langchain-ollama`, `langchain-chroma`, `langchain-community`), Transformers, Accelerate, PyTorch (CUDA 12.8), `llama-cpp-python` |
| **Embedding / DB** | ChromaDB, Hugging Face Embeddings (`ruri-v3-310m`), Gemini Embeddings (`gemini-embedding-2`) |
| **Tooling** | Ruff, ESLint, Prettier, Pytest |

---

## ディレクトリ構成

```text
ek-chat/
├── backend/                  # FastAPI バックエンド
│   ├── modules/              # 各種バックエンドモジュール
│   │   ├── database/         # Chroma DB 作成、Embedding、RAG コンテキスト取得
│   │   ├── response_generator/ # 各種 LLM（Gemini, Gemma, Ollama, Qwen 等）のアダプタ
│   │   ├── chat_manager.py   # チャット履歴・モデル管理・応答生成フロー
│   │   ├── logger.py         # ログ設定モジュール
│   │   └── schema.py         # Pydantic スキーマ定義
│   ├── tests/                # バックエンド用単体テスト
│   ├── main.py               # FastAPI エントリポイント
│   ├── pyproject.toml        # uv / Python プロジェクト定義
│   └── README.md             # バックエンド詳細ドキュメント
│
├── frontend/                 # Next.js フロントエンド
│   ├── app/                  # Next.js App Router 構成
│   │   ├── chat/             # チャット画面および関連コンポーネント
│   │   ├── components/       # 汎用 UI コンポーネント（ダイアログ、スライダー等）
│   │   ├── lib/              # API クライアント (fetchData)
│   │   ├── ThemeProvider.tsx # MUI / Emotion テーマプロバイダ
│   │   └── layout.tsx        # ルートレイアウト
│   ├── package.json          # Node.js パッケージ定義
│   └── README.md             # フロントエンド詳細ドキュメント
│
└── README.md                 # プロジェクト全体 README（本ファイル）
```

---

## セットアップ

詳細なセットアップ手順や依存関係のインストール方法については、各ディレクトリの README を参照してください。

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

### 1. 環境変数の設定

`backend/` および `frontend/` に用意されている `.env.example` をコピーし、`.env` ファイルを作成して必要な設定を記述します。

```bash
# Backend の環境変数
cp backend/.env.example backend/.env

# Frontend の環境変数
cp frontend/.env.example frontend/.env
```

### 2. バックエンドのセットアップ

```bash
cd backend
# uv を用いて依存関係を同期
uv sync
```

※ ローカルモデル・GPU 推論を利用する場合、CUDA 環境および必要なモデル・DB データの配置が必要です（詳細は [Backend README](./backend/README.md) を参照）。

### 3. フロントエンドのセットアップ

```bash
cd frontend
# Yarn による依存関係のインストール
yarn install
```

---

## 起動方法

### バックエンドの起動

```bash
cd backend
uv run uvicorn main:app --reload
```

- API サーバー: `http://localhost:8000`
- Swagger UI (API ドキュメント): `http://localhost:8000/docs`

### フロントエンドの起動

```bash
cd frontend
yarn dev
```

- Web アプリケーション: `http://localhost:3000`

---

## 環境変数一覧

### Backend (`backend/.env`)

| 変数名 | 説明 | 既定値 / 設定例 |
|---|---|---|
| `ENVIRON` | ログレベル設定 (`dev` で DEBUG ログ出力) | `dev` / `prod` |
| `DATA_DIR` | チャット履歴、プロンプト、モデル、DB 等のデータ保存先パス | `./develop` |
| `CUDA_VISIBLE_DEVICES` | 使用する GPU デバイス番号 | `0` |
| `HF_HOME` | Hugging Face モデルキャッシュディレクトリ | `./develop/models` |
| `CHAT_MODEL` | 起動時に初期選択されるチャットモデル名 | `Gemini(API)` |
| `GOOGLE_API_KEY` | Gemini API を使用するための API キー | `your-google-api-key` |
| `GEMINI_MODEL` | 使用する Gemini モデル名 | `gemini-2.5-flash` |
| `OLLAMA_API_KEY` | Ollama Cloud を使用する場合の API キー | `your-ollama-api-key` |
| `OLLAMA_CLOUD_MODEL` | Ollama Cloud で使用するモデル名 | `gpt-oss:120b` |
| `EMBEDDING_MODE` | RAG 用 Embedding モデルの種類 (`huggingface` または `gemini`) | `huggingface` |

### Frontend (`frontend/.env`)

| 変数名 | 説明 | 既定値 / 設定例 |
|---|---|---|
| `BACKEND_URL` | バックエンド API サーバーのベース URL | `http://localhost:8000` |
| `DEFAULT_THEME` | デフォルトのカラーテーマ (`light` または `dark`) | `light` |
| `DEFAULT_FONT_SIZE` | デフォルトフォントサイズ (px) | `16` |

---

## API 概要

バックエンド (`FastAPI`) が提供する主な REST API エンドポイントです。

| メソッド | パス | 説明 | リクエスト | レスポンス |
|---|---|---|---|---|
| `GET` | `/` | Swagger UI (`/docs`) へリダイレクト | なし | `RedirectResponse` |
| `GET` | `/init` | 保存済みチャット一覧の取得 | なし | `ChatInfoList` |
| `PUT` | `/new` | 新規チャットセッションの作成 | なし | `ChatInfo` |
| `DELETE` | `/delete` | 指定 ID のチャットを削除 | `chat_id` (Query) | 204 No Content |
| `GET` | `/history` | 指定チャットのメッセージ履歴を取得 | `chat_id` (Query) | `ChatHistory` |
| `GET` | `/settings` | システムプロンプトおよびモデル一覧設定を取得 | なし | `SettingsResponse` |
| `PATCH` | `/system_prompt` | システムプロンプトの作成・更新 | `SystemPromptText` (Body) | 204 No Content |
| `PATCH` | `/model` | 選択チャットモデルおよびパラメータの変更 | `SelectedChatModel` (Body) | 204 No Content |
| `POST` | `/chat` | ユーザー入力に対するアシスタント返答生成 (RAG 含む) | `ChatMessage` (Body) | `GenerateChatResponse` |

---

## データ保存構造

`DATA_DIR`（デフォルト: `./develop`）配下に保存されるデータ構造です。

```text
develop/
├── chat_history/              # チャット履歴（JSON形式: <chat_id>.json）
├── system_prompt.md           # 設定中のシステムプロンプト（Markdown形式）
├── chroma/                    # Chroma ベクトルデータベース永続化ディレクトリ
├── models/                    # ローカル LLM / Embedding モデル配置ディレクトリ
│   ├── gemma-4-E2B-it/
│   ├── gemma-4-E2B-it-assistant/
│   ├── gemma-4-12B-it-qat-q4_0-gguf/
│   └── ruri-v3-310m/
└── elephantkashimashi/        # RAG 投入用元データ
    ├── songs/                 # 楽曲 JSON データ
    └── other/                 # テキストデータ
```

---

## 開発コマンド

### Backend

```bash
# 静的コード解析 (Ruff)
uv run ruff check .

# コードフォーマット (Ruff)
uv run ruff format .

# 単体テスト実行 (Pytest)
uv run pytest

# RAG ベクトルデータベースの作成
uv run python modules/database/create_database_chroma.py
```

### Frontend

```bash
# 開発サーバー起動
yarn dev

# 静的コード解析 (ESLint)
yarn lint

# コードフォーマット (Prettier)
yarn prettier --write .

# テスト実行 (Vitest)
yarn test

# 本番ビルド
yarn build
```

---

## 注意点

- **ローカルモデルと GPU 要件**:
  - `Gemma4:E2B`, `Gemma4:12B` などのローカルモデルを実行する場合、CUDA 対応 GPU および十分な VRAM が必要です。GPU が利用できない環境では自動的に無効（`is_use = False`）となります。
- **RAG 用ベクトルデータベースの初期化**:
  - RAG 検索を有効にするには、あらかじめ `modules/database/create_database_chroma.py` を実行して Chroma DB（`DATA_DIR/chroma`）を生成しておく必要があります。
- **Ollama / API キー**:
  - `Qwen3.8:27B` や `Muse-Glimmer:30B` を利用する場合はローカルで Ollama サービスが稼働している必要があります。
  - Gemini API や Ollama Cloud を利用する場合は `.env` に有効な API キーを設定してください。

---

### Author
- *[muetaek0321](https://github.com/muetaek0321)*
- *Gemini 3.7 Flash*
