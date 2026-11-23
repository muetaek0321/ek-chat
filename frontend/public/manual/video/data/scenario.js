// Fallback scenario data for local file:/// execution
window.SCENARIO_DATA = {
  "id": "ek-chat-operation-manual-video",
  "title": "ek-chat 操作解説動画",
  "description": "チャットボットアプリ ek-chat の画面構成、対話、RAG切り替え、設定変更、データベース閲覧の操作ガイド動画",
  "settings": {
    "baseResolution": { "width": 1920, "height": 1080 },
    "aspectRatio": "16:9",
    "theme": "dark",
    "imageContainer": {
      "width": 1536,
      "height": 960,
      "offsetX": 192,
      "offsetY": 40
    }
  },
  "scenes": [
    {
      "id": "scene_01_intro",
      "title": "はじめに",
      "duration": 6000,
      "image": "../images/chat_screen.png",
      "transition": "fade",
      "elements": [
        {
          "type": "caption",
          "text": "ek-chat 操作マニュアル動画へようこそ。基本操作から各種設定までをわかりやすく解説します。",
          "startTime": 500,
          "duration": 5000
        },
        {
          "type": "callout",
          "title": "ek-chat 操作ガイド",
          "text": "マルチLLM ＆ RAG対応チャットボット\n基本操作と活用方法を約1分でご紹介します。",
          "x": 660,
          "y": 420,
          "startTime": 800,
          "duration": 4800
        }
      ]
    },
    {
      "id": "scene_02_layout",
      "title": "画面構成とレイアウト",
      "duration": 7000,
      "image": "../images/chat_screen.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "画面は左側の「操作サイドバー」と右側の「チャット＆入力エリア」の2カラム構成です。",
          "startTime": 500,
          "duration": 6000
        },
        {
          "type": "highlight",
          "label": "操作サイドバー",
          "x": 192,
          "y": 40,
          "width": 300,
          "height": 960,
          "color": "#3b82f6",
          "startTime": 1000,
          "duration": 5500
        },
        {
          "type": "highlight",
          "label": "チャット＆入力エリア",
          "x": 492,
          "y": 40,
          "width": 1236,
          "height": 960,
          "color": "#10b981",
          "startTime": 2500,
          "duration": 4000
        }
      ]
    },
    {
      "id": "scene_03_send_message",
      "title": "メッセージの入力と送信",
      "duration": 7500,
      "image": "../images/chat_screen.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "下部のテキスト欄に質問を入力し、Enterキーまたは送信ボタンをクリックして送信します。",
          "startTime": 500,
          "duration": 6500
        },
        {
          "type": "highlight",
          "label": "メッセージ入力欄",
          "x": 486,
          "y": 926,
          "width": 1164,
          "height": 66,
          "color": "#2563eb",
          "startTime": 800,
          "duration": 6200
        },
        {
          "type": "cursor",
          "startX": 950,
          "startY": 880,
          "endX": 1680,
          "endY": 965,
          "moveTime": 1500,
          "clickTime": 3500,
          "startTime": 1500
        },
        {
          "type": "callout",
          "text": "Enter: 送信\nShift + Enter: 改行",
          "x": 1380,
          "y": 820,
          "startTime": 3800,
          "duration": 3200
        }
      ]
    },
    {
      "id": "scene_04_rag_toggle",
      "title": "RAG（検索拡張生成）の切り替え",
      "duration": 8000,
      "image": "../images/chat_screen.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "入力欄上部の虫眼鏡ボタンでRAGのON/OFFを切り替えます。ONにすると楽曲DBから検索して回答します。",
          "startTime": 500,
          "duration": 7000
        },
        {
          "type": "highlight",
          "label": "RAG有効化ボタン",
          "x": 486,
          "y": 880,
          "width": 70,
          "height": 60,
          "color": "#f59e0b",
          "startTime": 800,
          "duration": 6800
        },
        {
          "type": "cursor",
          "startX": 800,
          "startY": 800,
          "endX": 521,
          "endY": 912,
          "moveTime": 1200,
          "clickTime": 2500,
          "startTime": 1000
        },
        {
          "type": "callout",
          "title": "RAGモードの使い分け",
          "text": "・ON (グレー背景): 楽曲データベースを参照して正確に応答\n・OFF (白背景): モデル本来の汎用知識で自由に対話",
          "x": 580,
          "y": 760,
          "startTime": 2800,
          "duration": 4800
        }
      ]
    },
    {
      "id": "scene_05_metadata",
      "title": "AI応答とメタデータの確認",
      "duration": 8000,
      "image": "../images/chat_screen.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "AI応答の右下にあるℹ️アイコンにカーソルを合わせると、推論速度（token/sec）や生成時間を確認できます。",
          "startTime": 500,
          "duration": 7000
        },
        {
          "type": "highlight",
          "label": "応答メタデータ (ℹ️)",
          "x": 1654,
          "y": 559,
          "width": 59,
          "height": 46,
          "color": "#06b6d4",
          "startTime": 800,
          "duration": 6800
        },
        {
          "type": "cursor",
          "startX": 1200,
          "startY": 500,
          "endX": 1683,
          "endY": 582,
          "moveTime": 1400,
          "clickTime": 2600,
          "startTime": 1000
        },
        {
          "type": "callout",
          "title": "表示されるメタ情報",
          "text": "・モデル名: Gemini(API)\n・token/sec: 48.2 tokens/sec\n・生成時間: 1.12秒\n・実行日時: 2026-11-23 17:05",
          "x": 1300,
          "y": 380,
          "startTime": 2800,
          "duration": 4800
        }
      ]
    },
    {
      "id": "scene_06_chat_history",
      "title": "履歴・セッション管理",
      "duration": 8000,
      "image": "../images/chat_screen.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "「新しいチャット」で新規会話を開始できます。過去の会話はサイドバーから切り替えや削除が可能です。",
          "startTime": 500,
          "duration": 7000
        },
        {
          "type": "highlight",
          "label": "新しいチャット",
          "x": 187,
          "y": 200,
          "width": 307,
          "height": 60,
          "color": "#3b82f6",
          "startTime": 800,
          "duration": 3200
        },
        {
          "type": "highlight",
          "label": "チャット履歴リスト",
          "x": 187,
          "y": 298,
          "width": 308,
          "height": 100,
          "color": "#8b5cf6",
          "startTime": 3600,
          "duration": 4000
        },
        {
          "type": "callout",
          "text": "最初の発言からタイトルが自動設定されます。\n右端の ⌫ ボタンで履歴を削除できます。",
          "x": 520,
          "y": 240,
          "startTime": 2000,
          "duration": 5500
        }
      ]
    },
    {
      "id": "scene_07_open_settings",
      "title": "設定モーダルを開く",
      "duration": 6000,
      "image": "../images/chat_screen.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "サイドバーの「設定」ボタンをクリックして、システムプロンプトやモデル設定モーダルを開きます。",
          "startTime": 500,
          "duration": 5000
        },
        {
          "type": "highlight",
          "label": "設定ボタン",
          "x": 187,
          "y": 251,
          "width": 307,
          "height": 50,
          "color": "#f59e0b",
          "startTime": 800,
          "duration": 4800
        },
        {
          "type": "cursor",
          "startX": 600,
          "startY": 400,
          "endX": 341,
          "endY": 276,
          "moveTime": 1200,
          "clickTime": 2400,
          "startTime": 1000
        }
      ]
    },
    {
      "id": "scene_08_prompt_edit",
      "title": "システムプロンプトの編集",
      "duration": 8000,
      "image": "../images/settings_modal.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "システムプロンプト欄でAIのキャラクターや口調を指示できます。編集後は「登録」で即座に反映されます。",
          "startTime": 500,
          "duration": 7000
        },
        {
          "type": "highlight",
          "label": "指示文入力エリア (Markdown対応)",
          "x": 618,
          "y": 395,
          "width": 684,
          "height": 345,
          "color": "#3b82f6",
          "startTime": 800,
          "duration": 6800
        },
        {
          "type": "highlight",
          "label": "登録ボタン",
          "x": 1240,
          "y": 748,
          "width": 82,
          "height": 48,
          "color": "#10b981",
          "startTime": 3600,
          "duration": 4000
        },
        {
          "type": "cursor",
          "startX": 800,
          "startY": 600,
          "endX": 1281,
          "endY": 772,
          "moveTime": 1200,
          "clickTime": 5000,
          "startTime": 3600
        }
      ]
    },
    {
      "id": "scene_09_model_settings",
      "title": "チャットモデルとパラメータ設定",
      "duration": 8500,
      "image": "../images/settings_model_tab.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "モデル選択のほか、回答の創造性（Temperature）や思考の深さ（Thinking）をスライダー等で柔軟に調整できます。",
          "startTime": 500,
          "duration": 7500
        },
        {
          "type": "highlight",
          "label": "モデル選択プルダウン",
          "x": 835,
          "y": 408,
          "width": 476,
          "height": 77,
          "color": "#f59e0b",
          "startTime": 800,
          "duration": 3200
        },
        {
          "type": "highlight",
          "label": "回答の創造性（Temperature 0.0〜1.0）",
          "x": 571,
          "y": 504,
          "width": 719,
          "height": 84,
          "color": "#06b6d4",
          "startTime": 3600,
          "duration": 4500
        }
      ]
    },
    {
      "id": "scene_10_database_view",
      "title": "データベース閲覧機能",
      "duration": 8000,
      "image": "../images/database_screen.png",
      "transition": "crossfade",
      "elements": [
        {
          "type": "caption",
          "text": "サイドバーの「データベースへ移動」から、AIが参照している全270曲以上の楽曲データベースを直接閲覧できます。",
          "startTime": 500,
          "duration": 7000
        },
        {
          "type": "highlight",
          "label": "楽曲一覧リスト（クリックで詳細表示）",
          "x": 504,
          "y": 110,
          "width": 1200,
          "height": 890,
          "color": "#10b981",
          "startTime": 800,
          "duration": 6800
        },
        {
          "type": "callout",
          "text": "各楽曲をクリックすると、作詞・作曲、発売日、歌詞、YouTube動画が確認できます。",
          "x": 650,
          "y": 220,
          "startTime": 2500,
          "duration": 5000
        }
      ]
    },
    {
      "id": "scene_11_outro",
      "title": "おわりに",
      "duration": 6000,
      "image": "../images/chat_screen.png",
      "transition": "fade",
      "elements": [
        {
          "type": "caption",
          "text": "操作解説は以上です。より詳しい仕様やFAQはHTMLマニュアル（manual/index.html）をご確認ください。",
          "startTime": 500,
          "duration": 5000
        },
        {
          "type": "callout",
          "title": "ご視聴ありがとうございました",
          "text": "ek-chat で快適な対話とナレッジ検索をお楽しみください。\n詳細ドキュメントは「操作マニュアルへ戻る」から参照できます。",
          "x": 650,
          "y": 420,
          "startTime": 800,
          "duration": 4800
        }
      ]
    }
  ]
};
