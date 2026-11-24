---
name: operation-manual-and-video
description: "Webアプリケーション等の操作マニュアル（HTML単体完結・実機スクリーンショット付き）および、ブラウザ上で再生可能な操作解説動画（Canvas API不使用、DOM/CSS/JSベース、シーン・シナリオ駆動型）を作成・保守するスキル。「マニュアルを作成して」「操作説明動画を作って」「マニュアルと解説動画を更新して」などの要求に対して使用します。"
user-invocable: true
---

# 操作マニュアル＆操作解説動画作成スキル

本スキルは、Webアプリケーションを対象に、**ブラウザ単体で閲覧可能なHTML操作マニュアル**および**DOM/CSS/JSベースのブラウザ再生型操作解説動画**を一貫して作成・更新・保守するための実践ガイドです。

---

## 1. 全体基本方針

1. **スタンドアロン動作の保証**:
   - アプリケーションサーバーに依存せず、ローカルファイル（`file:///`）およびWebサーバー配信（`http://...`）の双方で正常に閲覧・再生できる構成とします。
   - 将来的にアプリケーション内部からリンク・iframe・モーダル等で呼び出せるよう、ディレクトリやURLパスを整理します（例: `frontend/public/manual/` 配下）。
2. **実機ベースの正確性**:
   - 架空の画面イメージをでっち上げず、実際のアプリケーションのスクリーンショットをキャプチャして使用します。
   - マニュアルの操作手順と動画の解説ステップを完全に一致させます。
3. **Canvas API不使用（DOMベース動画エンジン）**:
   - 操作解説動画はCanvasではなく、HTML/CSS/SVG/JavaScript（DOM要素）で描画・アニメーションを構築します。
   - テキストの鮮明さ、レスポンシブ縮尺への追従、スタイル調整の容易性を担保します。
4. **シナリオデータとプレイヤーエンジンの分離**:
   - 動画の内容（テキスト、タイミング、座標、画像）はJSONシナリオで定義し、再生ロジック（タイムライン、描画エンジン、UI操作）と分離します。

---

## 2. ディレクトリ構成標準

マニュアルおよび動画は、静的ホスティングに適したディレクトリ（例: `frontend/public/manual/`）に配置します。

```text
manual/
├── index.html                # 操作マニュアル本体（HTML）
├── images/                   # スクリーンショット画像群（1280x800推奨）
│   ├── chat_screen.png
│   ├── settings_modal.png
│   └── ...
└── video/                    # 操作解説動画プレイヤー
    ├── index.html            # 動画プレイヤーHTML
    ├── css/
    │   └── player.css        # プレイヤーおよびアニメーションスタイル
    ├── js/
    │   ├── player.js         # コントローラー（再生・一時停止・シーク・UI）
    │   ├── timeline.js       # requestAnimationFrame時間管理エンジン
    │   └── scene-renderer.js # シーン・オーバーレイ描画エンジン
    └── data/
        ├── scenario.json     # 動画シナリオ定義（Fetch用）
        └── scenario.js       # file:///用フォールバック（window.SCENARIO_DATA = ...）
```

---

## 3. 操作マニュアル（HTML版）の作成手順

### 3.1 アプリケーション調査
- ルーティング、主要画面、サイドバー、モーダル、設定項目、エラー表示等の仕様をコード（フロントエンド・バックエンド）から抽出。
- ユーザー視点での利用フロー（「初期表示」「メッセージ送信」「パラメータ変更」「データ確認」など）を整理。

### 3.2 スクリーンショット取得
- 解像度は原則として **1280×800** など統一したアスペクト比でキャプチャ。
- 画面の状態（入力前、入力中、結果表示後、モーダル展開時）を操作手順に合わせて用意。
- キャプチャ画像は `manual/images/` にわかりやすい命名で保存。

### 3.3 マニュアルHTMLの構成要素
- **ヘッダー**: タイトル、バージョン、操作解説動画へのリンクボタン（`video/index.html`）。
- **ヒーローバナー**: アプリケーション概要と動画視聴へのCTA。
- **目次（TOC）**: スムーズスクロール可能なサイドナビゲーション。
- **機能別セクション**:
  - 概要と目的
  - 操作手順（ステップ番号付きの箇条書き）
  - 実際のスクリーンショット画像（拡大表示対応やキャプション付き）
  - 補足説明・Tips・注意事項（コールアウト）
- **完全自己完結スタイル**: 外部CDNに過度に依存せず、CSSやSVGアイコンをインラインまたは相対パスで完結させる。

---

## 4. 操作解説動画の技術仕様と設計

### 4.1 技術制約・仕様
- **描画方式**: HTML要素（`div`、`img`、`svg`、`span`）のDOM操作。Canvas APIは使用禁止。
- **アニメーション制御**: `requestAnimationFrame` を用いたミリ秒単位のタイムライン駆動。
- **基準解像度**: **1920 × 1080 (16:9)**。
  - 仮想ステージ（1920×1080）を定義し、CSSの `transform: scale(...)` またはコンテナ比率計算により、ウィンドウサイズに応じたレスポンシブ拡大縮小を実現する。
- **トランジション**: `fade`, `crossfade`, `slide`, `zoom` などのCSSトランジション／キーフレーム。
- **音声**: 音声・BGM・ナレーションは含めず、視覚的な誘導（枠線、矢印、テキスト、マウスカーソル）のみで伝える。

### 4.2 プレイヤー機能要件
- 再生／一時停止（スペースキー対応）
- 最初から再生／前のシーン／次のシーン（左右矢印キー対応）
- シークバー操作（ドラッグ・クリックで任意時間へのジャンプと状態の即時復元）
- タイムコード表示（現在時間 / 総時間）
- シーン一覧（クリックで該当シーンへジャンプ）
- フルスクリーン切り替え

### 4.3 `scenario.json` と `scenario.js` の二重管理
ローカルで `file:///.../index.html` を直接開いた場合、ブラウザのセキュリティ制限（CORS）により `fetch('data/scenario.json')` が失敗します。
そのため、必ず以下の仕組みを用意します：

1. `scenario.json`: 純粋なJSONデータ。
2. `scenario.js`: `window.SCENARIO_DATA = { ... };` として同一内容を定義。
3. `player.js`:
   ```javascript
   let scenario = null;
   try {
     const res = await fetch('data/scenario.json');
     if (res.ok) scenario = await res.json();
   } catch (e) {
     // file:/// 実行時等のフォールバック
     if (window.SCENARIO_DATA) scenario = window.SCENARIO_DATA;
   }
   ```
> **重要**: シナリオを更新した際は、**`scenario.json` と `scenario.js` の両方を常に同期**させること。

---

## 5. シナリオ構造と要素（Elements）定義

### 5.1 シナリオスキーマ例
```json
{
  "id": "app-operation-guide",
  "title": "アプリ操作解説動画",
  "description": "基本操作と各種機能の解説",
  "settings": {
    "baseResolution": { "width": 1920, "height": 1080 },
    "aspectRatio": "16:9",
    "imageContainer": {
      "width": 1536,
      "height": 960,
      "offsetX": 192,
      "offsetY": 40
    }
  },
  "scenes": [
    {
      "id": "scene_01",
      "title": "画面概要",
      "duration": 6000,
      "image": "../images/chat_screen.png",
      "transition": "fade",
      "elements": [
        {
          "type": "caption",
          "text": "画面の各エリアについて説明します。",
          "startTime": 500,
          "duration": 5000
        },
        {
          "type": "highlight",
          "label": "サイドバー",
          "x": 210,
          "y": 85,
          "width": 310,
          "height": 890,
          "color": "#3b82f6",
          "startTime": 1000,
          "duration": 4500
        }
      ]
    }
  ]
}
```

### 5.2 サポートするElement種別
| タイプ | 役割 | 主なプロパティ |
|---|---|---|
| `caption` | 画面下部に表示する字幕解説文 | `text`, `startTime`, `duration` |
| `highlight` | 操作対象を囲むアニメーション枠線 | `label`, `x`, `y`, `width`, `height`, `color`, `startTime`, `duration` |
| `cursor` | マウスカーソルの移動とクリック演出 | `startX`, `startY`, `targetX`, `targetY`, `startTime`, `duration`, `click` |
| `callout` | 画面内に浮かぶタイトル・詳細説明カード | `title`, `text`, `x`, `y`, `startTime`, `duration` |
| `arrow` | 操作対象を指し示す誘導矢印 | `fromX`, `fromY`, `toX`, `toY`, `color`, `startTime`, `duration` |
| `zoom` | 特定領域のフォーカス拡大表示 | `targetX`, `targetY`, `scale`, `startTime`, `duration` |

---

## 6. 座標系の計算と位置ズレ防止（重要ノウハウ）

動画ステージ（1920×1080）の中に、ウィンドウ枠（例: 1536×960）を介してスクリーンショット画像（例: 1280×800）が配置される場合、**目分量で座標を設定すると必ずズレが発生します**。

### 6.1 座標変換の計算公式

スクリーンショット内の画像ピクセル座標 `(img_x, img_y, img_w, img_h)` からステージ上の座標 `(stage_x, stage_y, stage_w, stage_h)` を求める公式：

```python
# ウィンドウ枠とスクリーンショットのスケール比
scale_x = window_inner_width / image_width   # 例: 1536 / 1280 = 1.2
scale_y = window_inner_height / image_height # 例: (960 - 38 title_bar) / 800 ≈ 1.1525

offset_x = window_left                       # 例: 192
offset_y = window_top + title_bar_height     # 例: 40 + 38 = 78

pad = 4  # 視覚的な余白（パディング）

stage_x = round(offset_x + (img_x - pad) * scale_x)
stage_y = round(offset_y + (img_y - pad) * scale_y)
stage_w = round((img_w + 2 * pad) * scale_x)
stage_h = round((img_h + 2 * pad) * scale_y)
```

### 6.2 ピクセル解析スクリプトによる正確なバウンディングボックス特定
位置ズレが生じた場合、画像をPython（Pillow / numpy）で解析し、対象UI要素（ボタン、入力欄、テキスト、プルダウン等）の境界ピクセルを特定してから上記公式で変換します。

```python
from PIL import Image
import numpy as np

img = Image.open('manual/images/target_screen.png')
arr = np.array(img)

# 対象領域の背景色との差分からUI部品のバウンディングボックスを抽出
# 例: y=370〜440の範囲で特定色のUIを探す
region = arr[370:440, 300:950, :3]
bg_color = arr[370, 950, :3]
diff = np.abs(region.astype(int) - bg_color.astype(int)).sum(axis=2)
content_pts = np.where(diff > 50)

min_y = content_pts[0].min() + 370
max_y = content_pts[0].max() + 370
min_x = content_pts[1].min() + 300
max_x = content_pts[1].max() + 300

print(f"画像内座標: x={min_x}..{max_x}, y={min_y}..{max_y}, w={max_x-min_x}, h={max_y-min_y}")
```

---

## 7. 作業フェーズと進行手順

本タスクを実行する際は、以下のフェーズに沿って進めます。

### フェーズ 1: 調査・シナリオ設計
1. アプリケーションコードからマニュアル化する機能と操作フローを整理。
2. 必要なスクリーンショット一覧を定義し、実機キャプチャを収集。
3. シーン構成案（シーン一覧、表示秒数、対象画面、説明文、強調箇所）を作成し、全体構成を固める。

### フェーズ 2: マニュアルHTMLの実装
1. `manual/index.html` を作成（CSS、画像配置、ステップ解説）。
2. 動画プレイヤーへのリンク導線を設置。
3. ブラウザで開き、レイアウト・画像パス・リンクが正常であることを確認。

### フェーズ 3: 動画プレイヤー＆シナリオの実装
1. 共通プレイヤー基盤（`index.html`, `player.css`, `player.js`, `timeline.js`, `scene-renderer.js`）を配置。
2. シナリオデータを作成し、`scenario.json` および `scenario.js` に出力。
3. 基準解像度・アスペクト比・レスポンシブ動作を整える。

### フェーズ 4: 座標調整と動作検証
1. ブラウザまたはHeadlessブラウザ（CDP等）を使用し、各シーンの強調枠・カーソル位置を目視／キャプチャ確認。
2. 位置ズレがある要素は、Pillow/numpyで画像ピクセルを測定し、変換公式を用いて正確に再計算。
3. `scenario.json` と `scenario.js` の両方を更新。
4. シーク操作、リサイズ、再生終了時のループ／停止動作を確認。

---

## 8. チェックリスト

作業完了前に以下を確認してください。

- [ ] マニュアル（`index.html`）が単体でブラウザから直接開けるか（余計な外部依存やリンク切れがないか）
- [ ] すべての画像が実機キャプチャであり、パスが相対パスで正しく解決されているか
- [ ] 動画プレイヤーが `file:///` と `http://...` の両環境で動作するか
- [ ] Canvas API を使用せず、DOM要素で映像表現が行われているか
- [ ] `scenario.json` と `scenario.js` の内容が完全に一致しているか
- [ ] すべての `highlight` 枠が実際のUI部品（ボタン、テキスト、入力欄）とピクセル単位で合致しているか
- [ ] シークバーを任意の位置に動かした際、正しいシーンと要素表示が復元されるか
- [ ] ウィンドウサイズを変更しても、16:9の比率と要素の相対位置が崩れないか
