# ek-chat

LLMを利用したチャットアプリケーションです。FastAPIを用いたバックエンドと、Next.jsを用いたフロントエンドで構成されています。

## 概要

- **アプリケーションの目的**: LLM (Gemini API, ローカルのGemmaモデル等) とのチャット機能を提供するアプリケーション。
- **ユーザーができること**:
  - チャットの新規作成、履歴の表示・保存・削除
  - ユーザーの入力に応じたAI(assistant)からの応答生成
  - システムプロンプトの確認および更新
  - チャットモデル（APIやローカルモデル）の切り替え
  - モデル生成パラメータの調整（思考時間など）
- **構成**:
  - **Backend**: FastAPIによるAPIサーバー。チャットデータや設定の保存、LLMによるテキスト生成を管理します。
  - **Frontend**: Next.js、React、MUIによるユーザーインターフェース。

## 技術スタック

- **Frontend**: Next.js (16.2), React (19), TypeScript, MUI (Material UI), Tailwind CSS, Vitest, React Testing Library
- **Backend**: FastAPI, Pydantic, Uvicorn, uv (パッケージマネージャ), Pytest
- **AI/LLM**: Gemini API (`langchain-google-genai`), PyTorch, Transformers, Accelerate (Gemma等のローカルモデル用)
- **Tooling**: ESLint, Prettier, Ruff

## ディレクトリ構成

```text
ek-chat/
├── backend/            # FastAPIベースのバックエンドAPI
│   ├── modules/        # スキーマ、チャット管理、レスポンス生成などのモジュール群
│   ├── pyproject.toml  # Pythonプロジェクト設定
│   └── main.py         # アプリケーションのエントリポイント
└── frontend/           # Next.jsベースのフロントエンドUI
    ├── app/            # アプリケーションのルーティングと画面コンポーネント
    └── package.json    # npm/yarnパッケージ設定
```

## セットアップと起動方法

各ディレクトリの詳細な手順については、それぞれのREADMEを参照してください。

- [Backend README](./backend/README.md)
- [Frontend README](./frontend/README.md)

1. **環境変数の設定**:
   `backend/` と `frontend/` それぞれに存在する `.env.example` をコピーし、`.env` ファイルを作成してください。
2. **バックエンドの起動**:
   Python 3.13以上の環境で `uv` を用いて依存関係をインストールし、開発サーバーを起動します。
3. **フロントエンドの起動**:
   Node.js と `yarn` を使用し、依存関係のインストール後に開発サーバーを起動します。

## 開発コマンド

各環境における主要な開発コマンドです。

### Backend (`backend/`)
- **Lint**: `uv run ruff check .`
- **Format**: `uv run ruff format .`
- **Test**: `uv run pytest`

### Frontend (`frontend/`)
- **Lint**: `yarn lint`
- **Format**: `yarn prettier --write .`
- **Test**: `yarn test` (Vitest によるテスト)
- **Build**: `yarn build`

## 注意点

- ローカルモデル (Gemma等) を利用するには、適切なGPU環境（CUDA）およびローカルへのモデル配置が必要となる場合があります。

---
### Author
- *[muetaek0321](https://github.com/muetaek0321)*
- *Gemini 3.1 Pro (High)*
