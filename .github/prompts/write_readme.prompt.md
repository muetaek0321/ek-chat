---
name: write_readme
tools:
  [
    "vscode",
    "execute",
    "read",
    "agent",
    "ms-python.python/getPythonEnvironmentInfo",
    "ms-python.python/getPythonExecutableCommand",
    "ms-python.python/installPythonPackage",
    "ms-python.python/configurePythonEnvironment",
    "todo",
  ]
description: README.md をプロジェクト内容に基づいて作成・更新するプロンプト
---

# README.md 作成・更新プロンプト

あなたはソフトウェア開発プロジェクトのドキュメント作成を担当するエンジニアです。
対象ディレクトリ配下のソースコード、設定ファイル、既存 README、ロックファイル、フォルダ構成を確認し、プロジェクトの実態に沿った README.md を作成または更新してください。

このリポジトリは、FastAPI 製 backend と Next.js 製 frontend で構成されたチャットアプリケーションです。
ルート、`backend/`、`frontend/` の各 README.md を必要に応じて作成・更新してください。

## 基本方針

- README.md は Markdown 形式で、日本語で記述する。
- ソースコードと設定ファイルから確認できる内容を優先する。
- 推測が必要な情報は断定せず、「要確認」と明記する。
- 文字化けしているコメントや表示文言はそのまま転記せず、識別子・型・API・ファイル構成から読み取れる範囲で自然な日本語に整理する。
- 初めて参加する開発者が、概要理解、環境構築、起動、主要機能の把握まで進められる内容にする。
- 既存 README.md がある場合は、古いテンプレート文を残さず、このプロジェクト固有の内容に更新する。

## 必ず確認するファイル

- `README.md`
- `backend/README.md`
- `backend/pyproject.toml`
- `backend/uv.lock`
- `backend/main.py`
- `backend/modules/schema.py`
- `backend/modules/chat_manager.py`
- `backend/modules/response_generator/*.py`
- `frontend/README.md`
- `frontend/package.json`
- `frontend/yarn.lock`
- `frontend/app/**/*.tsx`
- `frontend/app/**/*.ts`
- `.env.example` または環境変数を参照しているコード

## README に含める内容

必要に応じて、以下の章を作成してください。該当しない章は省略して構いません。

## プロジェクト名

リポジトリ名や既存ファイルから判断できる名前を記載する。
判断できない場合は仮の名前を使わず、「要確認」とする。

## 概要

- アプリケーションの目的
- ユーザーができること
- backend と frontend の役割
- LLM を利用したチャットアプリであること

## 主な機能

ソースコードから確認できる機能を箇条書きで整理する。
このプロジェクトでは、少なくとも以下を確認する。

- チャットの作成
- チャット履歴の表示・保存・削除
- ユーザー入力に対する assistant 応答の生成
- システムプロンプトの取得・更新
- チャットモデルの選択
- モデルパラメータの設定

## 技術スタック

確認できる範囲で分類して記載する。

- Frontend: Next.js, React, TypeScript, MUI, Tailwind CSS など
- Backend: FastAPI, Pydantic, uvicorn, uv など
- AI/LLM: Gemini API, Gemma 系ローカルモデル, LangChain Google GenAI, Transformers, PyTorch など
- Tooling: ESLint, Prettier, Ruff など

## ディレクトリ構成

主要ディレクトリと重要ファイルだけをツリー形式で記載する。
ロックファイルや生成物をすべて列挙しすぎない。

## セットアップ

backend と frontend を分けて記載する。

### Backend

- 必要な Python バージョン
- `uv` を使った依存関係のインストール方法
- 必要な環境変数
- `DATA_DIR` 配下に必要なデータ構成
- Gemini API を使う場合に必要な設定
- Gemma ローカルモデルを使う場合のモデル配置や GPU 要件

### Frontend

- 必要な Node.js / Yarn の前提
- 依存関係のインストール方法
- `BACKEND_URL` など必要な環境変数

## 起動方法

backend と frontend それぞれの開発サーバー起動手順を記載する。
実際のスクリプトやエントリポイントに基づいて記載し、未確認のコマンドは「要確認」とする。

## 環境変数

コードから参照されている環境変数を表形式で整理する。
例:

| 変数名         | 使用箇所 | 説明                                             | 既定値                  |
| -------------- | -------- | ------------------------------------------------ | ----------------------- |
| `BACKEND_URL`  | frontend | backend API のベース URL                         | なし                    |
| `DATA_DIR`     | backend  | チャット履歴・システムプロンプト・モデルの保存先 | `./develop`             |
| `CHAT_MODEL`   | backend  | 初期選択するチャットモデル                       | `Gemini(API)`           |
| `GEMINI_MODEL` | backend  | Gemini API で使用するモデル名                    | `gemini-2.5-flash-lite` |
| `ENVIRON`      | backend  | ログ設定の切り替え                               | `prod`                  |

API キーなど、ライブラリが暗黙的に要求する可能性がある環境変数は、コード上で直接確認できない場合は「要確認」として記載する。

## API 概要

FastAPI の主要エンドポイントを表形式で整理する。
`backend/main.py` と `backend/modules/schema.py` に基づいて、メソッド、パス、用途、主なリクエスト・レスポンスを記載する。

少なくとも以下を確認する。

- `GET /`
- `GET /init`
- `PUT /new`
- `DELETE /delete`
- `GET /history`
- `GET /settings`
- `PATCH /system_prompt`
- `PATCH /model`
- `POST /chat`

## データ保存

チャット履歴、システムプロンプト、ローカルモデルの保存場所を、`DATA_DIR` を基準に説明する。
保存形式が確認できる場合は、JSON や Markdown などの形式も記載する。

## 開発コマンド

確認できる範囲で以下を記載する。

- Lint
- Format
- Test
- Build

コマンドが存在しない場合は、存在しないことを明記するか、その章を省略する。
存在しないコマンドを作らない。

## 注意点・今後の改善候補

ソースコードから読み取れる制約や改善候補があれば記載する。
例:

- README 作成時点でテストが確認できない
- 一部コメントや UI 文言に文字化けがある
- ローカルモデル利用には GPU とモデルファイルが必要
- 必要な `.env.example` が存在しない場合は作成を推奨

## 出力ルール

- README.md としてそのまま保存できる Markdown を出力する。
- コードブロックには適切な言語名を付ける。
- 長すぎる説明は避け、実際に開発で参照しやすい粒度にする。
- 外部ドキュメントへのリンクは、必要最小限にする。
- 現在の実装と異なる一般的なテンプレート文は残さない。
- 最後にAuthorとして自身のモデル名を記載する。
