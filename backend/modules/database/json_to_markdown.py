import json
from argparse import ArgumentParser
from pathlib import Path

from langchain_core.documents import Document


def songs_json_to_markdown_doc(json_path: Path) -> Document:
    """楽曲情報jsonをmarkdown化しDocumentに変換

    Args:
        json_path(Path): jsonファイルのパス

    Returns:
        Document: メタデータと文書を含むDocument形式のデータ
    """
    # jsonファイルの読み込み
    with open(json_path, mode="r", encoding="utf-8") as f:
        data = json.load(f)

    md = []

    # タイトルとアーティスト
    title = data.get("title", "Unknown Title")
    artist = data.get("artist", "Unknown Artist")
    md.append(f"# {title}")
    md.append(f"**アーティスト**: {artist}")
    md.append("")

    # リリース日
    if "release_date" in data:
        md.append(f"**リリース日**: {data['release_date']}")

    # 作詞と作曲
    if "lyrics" in data:
        md.append(f"**作詞**: {', '.join(data['lyrics'])}")
    if "music" in data:
        md.append(f"**作曲**: {', '.join(data['music'])}")

    md.append("")

    # 収録作品 (Included In)
    if "included_in" in data and data["included_in"]:
        md.append("## 収録作品")
        for item in data["included_in"]:
            md.append(f"- 【{item.get('type', '')}】 {item.get('title', '')}")
        md.append("")

    # 詳細 (Details)
    if "details" in data:
        details = data["details"]
        md.append("## 詳細")
        md.append("")

        # 背景 (Background)
        if "background" in details:
            md.append("### 背景")
            bg = details["background"]
            if "description" in bg:
                md.append(bg["description"])
                md.append("")
            if "artist_comment" in bg:
                md.append(f"> {bg['artist_comment']}")
                md.append("")

        # 音楽的特徴 (Musical Features)
        if "musical_features" in details:
            md.append("### 音楽的特徴")
            mf = details["musical_features"]
            if "genre" in mf:
                md.append(f"- **ジャンル**: {', '.join(mf['genre'])}")
                md.append("")
            if "description" in mf:
                md.append(mf["description"])
                md.append("")

        # 評価・受容 (Reception)
        if "reception" in details:
            md.append("### 評価・受容")
            rec = details["reception"]
            if "description" in rec:
                md.append(rec["description"])
                md.append("")

        # 関連情報 (Related Information)
        if "related_information" in details and details["related_information"]:
            md.append("### 関連情報")
            for info in details["related_information"]:
                md.append(f"#### {info.get('type', '')}: {info.get('title', '')}")
                if "description" in info:
                    md.append(info["description"])
                md.append("")

    markdown_text = "\n".join(md)

    # Document形式のデータを作成
    doc = Document(
        metadata={"source": str(json_path), "title": data["title"], "category": "song"},
        page_content=markdown_text,
    )

    return doc


if __name__ == "__main__":
    parser = ArgumentParser(description="JSONファイルをマークダウン形式に変換するスクリプト")
    parser.add_argument("input_json", help="入力するJSONファイルのパス")

    args = parser.parse_args()

    song_doc = songs_json_to_markdown_doc(args.input_json)

    print(song_doc.metadata)
    print(song_doc.page_content)
