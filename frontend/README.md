# ek-chat Frontend

ek-chat アプリケーションのフロントエンド UI です。Next.js (App Router) と React を用いて構築されており、FastAPI バックエンドと連携したチャットインターフェースを提供します。

---

## 主な機能

- **チャット UI**:
  - メッセージ送受信（Markdown レンダリング対応）
  - 新規チャット作成、履歴一覧のサイドバー表示、履歴の切り替え・削除
  - 送信中のローディング表示および入力制御
- **設定モーダル**:
  - **システムプロンプトの編集**: リアルタイム取得・更新
  - **チャットモデル設定**: 利用可能なモデルの選択（利用不可モデルはグレーアウト表示）
  - **パラメータ調整**: Temperature（スライダー）、Thinking Budget（トグルボタン）
- **テーマ & デザイン**:
  - Material UI (MUI v9) と Tailwind CSS v4 を組み合わせたレスポンシブデザイン
  - Light / Dark テーマ切り替え対応（`ThemeProvider`）
  - フォントサイズ設定

---

## セットアップ

### 必要要件

- Node.js (v20 以上推奨)
- パッケージマネージャ: Yarn（`yarn.lock` を利用）

### 依存関係のインストール

```bash
cd frontend
yarn install
```

### 環境変数の設定

`.env.example` をコピーして `.env` ファイルを作成し、設定を記述します。

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
| `BACKEND_URL` | バックエンド API サーバーのベース URL | `http://localhost:8000` |
| `DEFAULT_THEME` | デフォルトのカラーテーマ (`light` または `dark`) | `light` |
| `DEFAULT_FONT_SIZE` | デフォルトフォントサイズ (px) | `16` |

---

## 起動方法

### 開発用サーバーの起動

```bash
yarn dev
```

ブラウザで [http://localhost:3000](http://localhost:3000) にアクセスして利用します。

---

## 開発コマンド

`package.json` に定義されている主要スクリプトです。

| コマンド | 説明 |
|---|---|
| `yarn dev` | Next.js 開発サーバーの起動 |
| `yarn build` | 本番環境向けビルドの実行 |
| `yarn start` | ビルド済み本番サーバーの起動 |
| `yarn lint` | ESLint によるコードの静的解析 |
| `yarn prettier --write .` | Prettier によるコードフォーマット |
| `yarn test` | Vitest / React Testing Library による単体テストの実行 |

---

## ディレクトリ構成

```text
frontend/
├── app/
│   ├── chat/                     # チャット関連画面
│   │   ├── components/           # チャット個別コンポーネント (ChatList, SettingButton 等)
│   │   └── page.tsx              # チャットページ
│   ├── components/               # 汎用 UI コンポーネント (Slider, TabPanel, Dialog 等)
│   ├── lib/                      # API 呼び出しモジュール (fetchData)
│   ├── ThemeProvider.tsx         # テーマプロバイダ
│   ├── theme.ts                  # MUI テーマ定義 (Light / Dark)
│   ├── styles.ts                 # 共通 MUI スタイル定義
│   ├── types.ts                  # TypeScript 型定義
│   ├── layout.tsx                # ルートレイアウト
│   └── page.tsx                  # ルートページ (リダイレクト)
├── public/                       # 静的アセット
├── package.json                  # パッケージ定義
└── vitest.config.ts              # Vitest 設定
```

---

### Author
- *[muetaek0321](https://github.com/muetaek0321)*
- *Gemini 3.7 Flash*
