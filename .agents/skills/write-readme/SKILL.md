---
name: write-readme
description: "プロジェクトの内容（ソースコード、設定ファイル、ディレクトリ構造等）に基づいて README.md を作成または更新するスキル。ルート、backend/、frontend/ の README.md を実態に沿って整理する際使用します。"
user-invocable: true
---

# README.md 作成・更新スキル

対象ディレクトリ配下のソースコード、設定ファイル、既存 README、ロックファイル、フォルダ構成を確認し、プロジェクトの実態に沿った `README.md` を作成または更新します。

このリポジトリは FastAPI 製 backend と Next.js 製 frontend で構成されたチャットアプリケーションです。必要に応じてルート、`backend/`、`frontend/` の各 `README.md` を作成・更新します。

## 基本方針

- **フォーマット**: Markdown 形式、日本語で記述。
- **事実ベース**: ソースコードや設定ファイルから確認できる内容を優先。推測が必要な情報は断定せず「要確認」と明記する。
- **自然な表現**: 文字化けしているコメントや表示文言はそのまま転記せず、識別子・型・API・ファイル構成から読み取れる自然な日本語に整理する。
- **実用性**: 初めて参加する開発者が概要理解、環境構築、起動、主要機能の把握まで進められる内容にする。
- **更新方針**: 既存 `README.md` がある場合は古いテンプレート文を残さず、このプロジェクト固有の内容に更新する。

## 確認すべき主要ファイル

処理を開始する前に、以下のファイルを読み込んで確認します。

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
- `frontend/yarn.lock` または使用されているロックファイル
- `frontend/app/**/*.tsx`
- `frontend/app/**/*.ts`
- `.env.example` または環境変数を参照しているコード

## 手順・アクション

1. **プロジェクトの実態把握**:
   - 上記ファイルを探索・読み込み、技術スタック、環境変数、APIエンドポイント、起動コマンド、ディレクトリ構成などの最新状態を収集します。
2. **構成要素の整理**:
   - 下記の「README に含める標準構成」に従い、収集した情報を章ごとに整理します。
3. **ファイルへの出力・更新**:
   - 収集した情報に基づいて `README.md`（必要に応じて `backend/README.md`, `frontend/README.md`）を作成または更新します。

---

## README に含める標準構成

各章の必要性に応じて記述します（該当しない章は省略可能）。

### 1. プロジェクト名
- リポジトリ名や既存ファイルから判断できる名前。判断できない場合は「要確認」とする。

### 2. 概要
- アプリケーションの目的
- ユーザーができること
- backend と frontend の役割
- LLM を利用したチャットアプリであること

### 3. 主な機能
ソースコードから確認できる機能を箇条書きで整理：
- チャットの作成
- チャット履歴の表示・保存・削除
- ユーザー入力に対する assistant 応答の生成
- システムプロンプトの取得・更新
- チャットモデルの選択
- モデルパラメータの設定

### 4. 技術スタック
- **Frontend**: Next.js, React, TypeScript, MUI, Tailwind CSS など
- **Backend**: FastAPI, Pydantic, uvicorn, uv など
- **AI/LLM**: Gemini API, Gemma 系ローカルモデル, LangChain Google GenAI, Transformers, PyTorch など
- **Tooling**: ESLint, Prettier, Ruff など

### 5. ディレクトリ構成
主要ディレクトリと重要ファイルだけをツリー形式で記載（ロックファイルや生成物をすべて列挙しすぎない）。

### 6. セットアップ

#### Backend
- 必要な Python バージョン（`.python-version` 参照）
- `uv` を使った依存関係のインストール方法
- 必要な環境変数
- `DATA_DIR` 配下に必要なデータ構成
- Gemini API を使う場合の設定
- Gemma ローカルモデルを使う場合のモデル配置や GPU 要件

#### Frontend
- 必要な Node.js / パッケージマネージャの前提
- 依存関係のインストール方法
- `BACKEND_URL` など必要な環境変数

### 7. 起動方法
- Backend / Frontend それぞれの開発サーバー起動手順。
- 実際のスクリプトやエントリポイントに基づき記述（未確認コマンドは「要確認」）。

### 8. 環境変数
コードから参照されている環境変数を表形式で整理。

| 変数名 | 使用箇所 | 説明 | 既定値 |
| --- | --- | --- | --- |
| `BACKEND_URL` | frontend | backend API のベース URL | なし |
| `DATA_DIR` | backend | チャット履歴・システムプロンプト・モデルの保存先 | `./develop` |
| `CHAT_MODEL` | backend | 初期選択するチャットモデル | `Gemini(API)` |
| `GEMINI_MODEL` | backend | Gemini API で使用するモデル名 | `gemini-2.5-flash-lite` |
| `ENVIRON` | backend | ログ設定の切り替え | `prod` |

※ コード上で直接確認できないが暗黙的に必要な環境変数は「要確認」として記載。

### 9. API 概要
`backend/main.py` および `backend/modules/schema.py` に基づく主要エンドポイントを表形式で整理。
- `GET /`
- `GET /init`
- `PUT /new`
- `DELETE /delete`
- `GET /history`
- `GET /settings`
- `PATCH /system_prompt`
- `PATCH /model`
- `POST /chat`

### 10. データ保存
`DATA_DIR` を基準としたチャット履歴、システムプロンプト、ローカルモデル等の保存場所・形式（JSON, Markdownなど）の説明。

### 11. 開発コマンド
確認できる範囲で Lint, Format, Test, Build などのコマンドを記載（存在しないコマンドは作成しない）。

### 12. 注意点・今後の改善候補
ソースコードから読み取れる制約や改善候補。
- README 作成時点でテストが確認できない/不十分な点
- ローカルモデル利用に必要な GPU / モデルファイルに関する注意
- 必要な `.env.example` の作成推奨など

---

## 出力ルール

- `README.md` としてそのまま保存できる Markdown を出力する。
- コードブロックには適切な言語名を指定する。
- 外部ドキュメントへのリンクは必要最小限に留める。
- 実装と異なる一般的なテンプレート文は残さない。
- 最後に Author として実行したモデル名を記載する。
