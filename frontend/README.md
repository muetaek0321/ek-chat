# ek-chat Frontend

ek-chat アプリケーションのフロントエンド UI です。Next.js と React を用いて構築されており、バックエンド API と連携してチャットインターフェースを提供します。

## 主な機能

- バックエンド API (`FastAPI`) との通信
- チャット履歴の表示およびチャット画面の UI 提供
- モデル切り替えやパラメータ設定のための UI
- Material UI (MUI) および Tailwind CSS を活用したスタイリング

## セットアップ

### 必要要件
- Node.js (v20 以上推奨)
- パッケージマネージャ: Yarn または npm (プロジェクトには `yarn.lock` が存在するため Yarn を推奨)

### 依存関係のインストール

プロジェクトルートから `frontend` ディレクトリへ移動し、依存関係をインストールします。

```bash
cd frontend
yarn install
```

### 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、バックエンドの URL を指定します。

```bash
# Linux/macOS
cp .env.example .env

# Windows (PowerShell)
Copy-Item .env.example .env
# Windows (Command Prompt)
copy .env.example .env
```

| 変数名 | 使用箇所 | 説明 | 既定値 |
|---|---|---|---|
| `BACKEND_URL` | frontend | backend API サーバーのベース URL | `http://localhost:8000` |

### 起動方法

開発用サーバーを起動します。

```bash
yarn dev
```

起動後、ブラウザで [http://localhost:3000](http://localhost:3000) にアクセスすることでアプリケーションを利用できます。

## 開発コマンド

`package.json` に定義されているスクリプトです。

- **Dev**: `yarn dev` (開発サーバーの起動)
- **Build**: `yarn build` (本番環境向けビルドの作成)
- **Start**: `yarn start` (ビルド済みの本番サーバーの起動)
- **Lint**: `yarn lint` (ESLint によるコードの静的解析)
- **Test**: `yarn test` (Vitest によるテストの実行)

---
*Author: Gemini 3.1 Pro (High)*
