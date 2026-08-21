---
name: update-docstrings
description: "指定されたソースコードファイル（Python, TypeScript等）の関数・クラス・メソッドに対して、DocstringやJSDocコメントを新規作成、またはコードの現行実装に合わせて更新するスキル。「Docstringの生成」「関数ドキュメントの更新」「JSDocの追加」などの要求に対して使用します。"
user-invocable: true
---

# 関数のドキュメント（Docstring / JSDoc）作成・更新スキル

指定されたファイル内の関数・メソッド・クラスについて、実装の内容や型情報を分析し、新規にドキュメントコメントを作成するか、既存の古いドキュメントを最新の実装に合わせて更新します。

---

## 基本方針

- **コードを変更しない**: 関数のロジックや動作を変更せず、ドキュメントコメント（Docstring / JSDoc）のみを追加・更新します。
- **実態の反映**: シグネチャ、型ヒント、内部で発生する例外（Raises / @throws）、引数の役割、戻り値の正確な意味をコードから分析して記述します。
- **冗長性の排除**: コードの型や名前から明らかに読み取れる不要な説明は避け、「なぜその処理を行うか」「引数や戻り値が表すドメイン上の意味」「事前条件・事後条件・例外条件」を中心に記述します。
- **言語別・フレームワーク別スタイル規定**:
  - **Python (全般 / Google Style Docstring)**:
    - 基本的に [Google Python Style Guide] の Docstring 形式に従う。
    - 構成セクション: 概要（Summary）、`Args:`、`Returns:`、`Yields:`、`Raises:`、`Examples:` など。
    - 型ヒント（Type Hints）がコードに明記されている場合、Docstring内での型表記の重複は避け、役割や制約の説明に集中する。
    - プロジェクトの `.github/copilot-instructions.md` の規定を遵守する。
  - **FastAPI (API エンドポイント / Swagger UI 連携)**:
    - エンドポイント関数の Docstring は Swagger UI / OpenAPI ドキュメントに直接反映・レンダリングされることを前提に記述する。
    - **1行目（Summary）**: エンドポイントの簡潔な概要（Swagger UI のタイトル／アコーディオン見出しとして表示されるため、1行でわかりやすく記述）。
    - **2行目以降（Description）**: Swagger UI 上でリッチテキストとして表示されるため、Markdown（箇条書き、太字、コード等）を活用して詳細・前提条件・処理フローを記載。
    - **エラー・ステータスコードの補足**: 想定されるレスポンス（200系）やエラー（400, 401, 404, 500等）の発生条件や詳細を明記する。
  - **TypeScript / JavaScript**: [JSDoc スタイル] に従う。
    - タグ: `@param`, `@returns`, `@throws` など。

---

## 手順・アクション

### 1. 対象ファイルとコンテキストの収集
1. 指定されたファイル（例: `backend/routers/chat.py` や `backend/modules/chat_manager.py` など）を読み込みます。
2. 関連する型定義・スキーマファイル（`backend/schemas/` や Pydantic モデル等）やエラー定義を確認します。

### 2. 関数・メソッド・エンドポイントの分析とドキュメント差分チェック
ファイル内の各関数・メソッド・クラスについて以下を確認します：
- **通常の関数・クラスか、FastAPI のエンドポイントか**:
  - ルーターデコレータ（`@router.get`, `@router.post`, `@app.get` 等）が付与されている場合は FastAPI 向けスタイルを適用。
  - 通常の関数・クラス・モジュールメソッドの場合は標準の Google Style を適用。
- **既存のドキュメントコメントの検証**:
  - なければ新規作成対象。
  - 存在する場合は、引数名・型・戻り値・送出例外・Swagger UIでの見栄えが現在の実装と整合しているか確認。
- **引数 (Args / @param / Query & Path パラメータ)**:
  - 型ヒントやバリデーション制約（`Query()`, `Path()`, `Depends()` など）を確認。
- **戻り値・レスポンス (Returns / Response Model)**:
  - 戻り値の型・Pydanticスキーマの意味。
- **例外・エラー (Raises / Status Codes)**:
  - `raise HTTPException(...)` や内部例外の発生条件。

### 3. ドキュメントコメントの生成・更新
コードのインデントを崩さず、適切なスタイルで記述します。各言語・フレームワークごとの詳細な作成例は [examples/examples.md](examples/examples.md) を参照してください。

- **Python (一般関数・クラス)**: Google Style に従い `Args:`, `Returns:`, `Raises:` などを構成。
- **FastAPI (エンドポイント)**: 1行目を概要（Summary）、2行目以降を Markdown による詳細（Description・処理フロー・エラーコード等）として記述。
- **TypeScript / JavaScript**: `@param`, `@returns`, `@throws` を用いた JSDoc 形式で記述。

### 4. 品質検証チェックリスト
作業完了時、以下を満たしているか確認します：
- [ ] 既存のコード処理（インデントやロジック）を誤って壊していないか。
- [ ] 未使用の引数や、存在しない例外・エンドポイント仕様がドキュメントに残っていないか。
- [ ] FastAPI エンドポイントの場合、Swagger UI 上でタイトルと詳細が見やすく階層化されているか。
- [ ] Ruff / ESLint 等のリンターで構文エラーや警告が発生していないか。

---

## 呼び出し例

ユーザーが以下のように要求した際に本スキルを起動します：
- `backend/modules/chat_manager.py の関数にDocstringを追加して`
- `backend/routers/chat.py のAPIエンドポイントにSwagger UI向けのDocstringを追加して`
- `frontend/app/lib/fetchData.ts のJSDocコメントを最新のコードに合わせて更新して`
- `このファイルの関数ドキュメントをレビューして作成し直して`
