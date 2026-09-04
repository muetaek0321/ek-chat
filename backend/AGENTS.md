---
name: backend-instructions
description: Backend Python development guidelines for the backend folder.
applyTo: "backend/**"
---

# Backend Instructions

## Python & Architecture

- `.python-version` に記載された Python バージョン (>=3.13) で動作させる。
- PEP 8 に従う。
- 型ヒントを必ず付与する（関数引数、戻り値、主要な変数）。
- `pathlib.Path` を優先し、`os.path` は必要な場合のみ使用する。
- **データモデルの使い分け**:
  - API エンドポイントのリクエスト/レスポンス・バリデーションには、`modules.schema.EndpointModel` を継承した Pydantic モデルを使用する（camelCase <-> snake_case 変換に対応）。
  - 内部処理用の軽量なデータ保持には `dataclass` を検討する。
- **LLM モデルの拡張**:
  - 新しいチャットモデルを追加する場合は `modules.response_generator.base.ResponseGenerator` を継承し、抽象メソッドの `setup()`、`cleanup()`、`get_parameters()`、`update_parameters()`、`__call__()` を実装した上で `ChatManager` に登録する。
- 標準ライブラリで実現できる場合は標準ライブラリを優先する。
- マジックナンバーは避け、定数や Enum (`StrEnum` 等) を定義して利用する。
- 関数は単一責任を意識し、長くなり過ぎないようにする。

## Code Quality & Tooling

- パッケージ管理には `uv` を使用する。
- import 順序は Ruff に従う。
- 未使用 import や未使用変数を残さない。
- `noqa` によるルール回避は必要最小限とする。
- 既存の公開 API との互換性を可能な限り維持する。

変更後は、`backend` ディレクトリで次を実行して確認する。

```bash
uv run ruff format .
uv run ruff check .
```

## Docstrings

公開 API、主要なクラス・関数には Google スタイルの Docstring を記述する。必要に応じて概要、Args、Returns、Raises を含め、コードから明らかな内容は繰り返さない。

## Error Handling and Logging

- 想定される例外は適切に処理し、FastAPI の `HTTPException` やカスタム例外ハンドラで整ったエラーレスポンスを返す。
- エラーメッセージは原因が分かる具体的な内容にする。
- `print` は使用せず、モジュールのロギングには `modules.logger.get_logger(__name__)`、API エンドポイントのロギングには `modules.logger.get_endpoint_logger(req)` を使用し、適切なログレベル（DEBUG / INFO / WARNING / ERROR）で出力する。
- 外部入力は信頼せず、Pydantic スキーマ等で検証する。

## Performance and File Handling

- 不必要なメモリコピーを避ける。
- イテレータやジェネレータを利用できる場合は優先する。
- 大きなファイルやLLMストリーミングは一括読み込みを避け、チャンク処理・ストリーミング処理を検討する。

## Testing

既存機能を変更した場合は必要に応じてテストを更新する。外部API通信やローカルLLM/GPU推論、重い処理を伴う部分は `unittest.mock` (`patch`) を用いてモック化し、高速かつ安定して動作する単体テストを作成する。

```bash
uv run pytest
```
