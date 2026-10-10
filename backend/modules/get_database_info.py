import json
import os
from pathlib import Path

import pandas as pd

from schemas.database import DatabaseListResponse, SongData, SongDataOutline

# 楽曲情報リストの取得
SONGS_DATA_PATH = Path(os.getenv("SONGS_DATA_PATH", "./develop/songs.parquet"))
if not SONGS_DATA_PATH.exists():
    raise FileNotFoundError(f"楽曲情報データが見つかりません: {SONGS_DATA_PATH}")
SONGS_DB = pd.read_parquet(SONGS_DATA_PATH, columns=["title", "db"])


def get_database_list_data() -> DatabaseListResponse:
    """データベースのリストを取得"""
    # DBが空の行を除外
    songs_df = SONGS_DB[SONGS_DB["db"].notna()]

    # 楽曲情報のリストを作成
    songs = [SongDataOutline(id=idx, title=row["title"]) for idx, row in songs_df.iterrows()]

    # レスポンスデータの作成
    # NOTE: 現状は楽曲情報のみだが今後追加する可能性あり
    response = DatabaseListResponse(songs=songs)

    return response


def get_song_database(song_id: str) -> SongData:
    """楽曲IDに基づいて楽曲の詳細情報を取得"""
    # 楽曲情報を取得
    song_db_path = Path(SONGS_DB.loc[song_id, "db"])
    if not song_db_path.exists():
        raise FileNotFoundError(f"楽曲DBが見つかりません: {song_db_path}")

    # 楽曲DBの読み込み
    with open(song_db_path, "r", encoding="utf-8") as f:
        song_data = SongData.model_validate(json.load(f))

    return song_data
