# ek-chat Backend

ek-chat アプリケーションのバックエンド API サーバーです。FastAPIを利用して構築されており、LLMを利用したチャット応答の生成や履歴の管理を行います。

## 主な機能

- FastAPIによるREST APIの提供
- チャット履歴・システムプロンプトの読み込み、保存、削除
- Gemini API (`langchain-google-genai`) やローカルモデル (Gemma等) を用いたチャット応答の生成
- チャットモデルの選択・パラメータ (temperature, thinking等) の設定

## セットアップ

### 必要要件
- Python 3.13 以上
- パッケージマネージャ [uv](https://github.com/astral-sh/uv)

### 依存関係のインストール

プロジェクトルートから `backend` ディレクトリへ移動し、`uv` を用いてパッケージをインストールします。

```bash
cd backend
# 依存関係の同期 (要確認: uvの基本的なインストールコマンド)
uv sync
```

※ GPUを利用したローカルモデルを使用する場合は、CUDA対応環境に合わせてPyTorchなどの設定が必要です (`pyproject.toml` に `torch-cu128` のインデックス指定が含まれています)。

### 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、必要な値を設定します。

```bash
# Linux/macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
# Windows (Command Prompt)
copy .env.example .env
```

| 変数名           | 使用箇所 | 説明                                             | 既定値                  |
| ---------------- | -------- | ------------------------------------------------ | ----------------------- |
| `ENVIRON`        | backend  | ログ設定の切り替え (`dev` でデバッグログ有効)    | `prod` (コード上)       |
| `DATA_DIR`       | backend  | チャット履歴・システムプロンプト・モデルの保存先 | `./develop`             |
| `CHAT_MODEL`     | backend  | 初期選択するチャットモデル                       | `Gemini(API)`           |
| `GOOGLE_API_KEY` | backend  | Gemini API を使用する場合の API キー             | `your-google-api-key`   |
| `GEMINI_MODEL`   | backend  | Gemini API で使用するモデル名                    | `gemini-2.5-flash`      |

### 起動方法

開発サーバーを起動します。（`main.py` 内に定義されたFastAPIアプリケーションを立ち上げます）

```bash
uv run uvicorn main:app --reload
# または、main.py を直接実行 (要確認: __main__ブロックが存在するため)
uv run python main.py
```

サーバーはデフォルトで `http://localhost:8000` にて起動します。Swagger UI は `http://localhost:8000/docs` で確認できます。

## API 概要

主要なエンドポイントは以下の通りです。詳細なスキーマは Swagger UI (`/docs`) にて確認可能です。

| メソッド | パス | 用途 | 主なリクエストパラメータ | 主なレスポンス |
|---|---|---|---|---|
| `GET` | `/` | SwaggerUIにRedirect | - | RedirectResponse |
| `GET` | `/init` | アプリの初期データ(チャット一覧)を取得 | - | `ChatInfoList` |
| `PUT` | `/new` | 新しいチャットを作成 | - | `ChatInfo` |
| `DELETE` | `/delete` | チャットを削除 | `chat_id` (クエリ) | 204 No Content |
| `GET` | `/history` | チャットの履歴を取得 | `chat_id` (クエリ) | `ChatHistory` |
| `GET` | `/settings` | 設定項目(SystemPromptと利用可能モデル)を取得 | - | `SettingsResponse` |
| `PATCH` | `/system_prompt` | SystemPromptのテキストを作成・更新 | `SystemPromptText` (Body) | 204 No Content |
| `PATCH` | `/model` | 選択されたモデルに変更し設定を適用 | `SelectedChatModel` (Body) | 204 No Content |
| `POST` | `/chat` | ユーザーの入力に対してassistantの応答を生成 | `ChatMessage` (Body) | `GenerateChatResponse` |

## 開発コマンド

- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Test**: `uv run pytest`

---
*Author: Gemini 3.1 Pro (High)*
