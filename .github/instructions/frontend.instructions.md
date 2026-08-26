---
name: frontend-instructions
description: Frontend TypeScript and React development guidelines for the frontend folder.
applyTo: "frontend/**"
---

# Frontend Instructions

## TypeScript & Architecture

- TypeScript の strict 設定を維持し、適切な型注釈を行う（`any` は避ける）。
- 既存の Next.js (App Router)、React 19、Material UI (MUI v9) の構成と API を尊重する。
- **ディレクティブの明示**:
  - インタラクティブな UI コンポーネントや React フックを使用するファイルには `'use client'` を付与する。
  - Server Component はデフォルトでサーバー側で実行されるため、通常は `'use server'` を付与しない。クライアントから呼び出す Server Action を定義する場合に限り、ファイル先頭へ `'use server'` を付与する。
- **パスエイリアスの活用**:
  - 相対パスの階層が深くなるのを避け、`tsconfig.json` に定義されたエイリアス（`@types`, `@styles`, `@components/*`, `@lib/*`）を使用する。
- **データ型と API 通信の統一**:
  - バックエンド連携のデータ型や設定型は `app/types.ts` (`@types`) に集約・定義する。
  - 通常のバックエンド API 通信では直接 `fetch` を呼ばず、`app/lib/fetchData.ts` (`@lib/fetchData`) に定義されたユーティリティ（`getRequest`, `postRequest`, `putRequest`, `deleteRequest` など）および `ApiResponse<T>` を使用する。通信ユーティリティ自体や要件上必要な特殊な通信処理では、用途に応じて直接 `fetch` を使用してよい。
- コンポーネントは単一責任を意識し、責務ごとに適切に分割する。
- アクセシブルな HTML 要素、ラベル、キーボード操作を優先する。

## Styling and UI

- スタイル定義は `app/styles.ts` (`@styles`) の共通スタイルや `app/theme.ts` のカラートークン・テーマ設定を優先して再利用する（直接の色コードやサイズのリテラル埋め込みは極力避ける）。
- デスクトップとモバイルの両方で、テキストや操作要素が重ならないレスポンシブデザインを維持する。
- UI 変更時は、ローディング中（`isRunning` 等）、エラー表示、空状態（Empty State）、キーボード操作などの状態遷移を考慮する。
- ユーザー向けの文言やインタラクションは、既存画面のトーン＆マナーに合わせる。

## Code Quality & Tooling

- パッケージ管理には `yarn` を使用する。
- ESLint と Prettier の既存設定に従う。
- 未使用 import、未使用変数、不要な `any` を残さない。
- 不要な外部依存関係（ライブラリ）を追加しない。
- 変更範囲は必要最小限にし、要求されていないリファクタリングを行わない。
- コメントはコードから意図が読み取りにくい理由を補う場合に限り、簡潔に記述する。

変更後は `frontend` ディレクトリで次を実行して確認する。

```bash
yarn lint
yarn tsc --noEmit
```

## Testing

- 既存機能を変更した場合は関連テストを更新する。
- 新しい処理やコンポーネントには、可能な限り Vitest と React Testing Library によるテストを追加する。
- 外部通信モジュール（`@lib/fetchData`）を呼び出すコンポーネントのテストは、`vi.mock` を用いてモック化し、安定して動作するように作成する。
- `frontend` ディレクトリで関連テスト、または次を実行して確認する。

```bash
yarn test run
```

