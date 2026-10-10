import os
from pathlib import Path

import pandas as pd

from schemas.database import DatabaseListResponse, SongDataOutline


def get_database_list_data() -> DatabaseListResponse:
    """データベースのリストを取得"""
    # 楽曲情報リストの取得
    songs_data_path = Path(os.getenv("SONGS_DATA_PATH", "./develop/songs.parquet"))
    if not songs_data_path.exists():
        raise FileNotFoundError(f"楽曲情報データが見つかりません: {songs_data_path}")
    songs_df = pd.read_parquet(songs_data_path, columns=["title", "db"])

    # DBが空の行を除外
    songs_df = songs_df[songs_df["db"].notna()]

    # 楽曲情報のリストを作成
    songs = [SongDataOutline(id=idx, title=row["title"]) for idx, row in songs_df.iterrows()]

    # レスポンスデータの作成
    # NOTE: 現状は楽曲情報のみだが今後追加する可能性あり
    response = DatabaseListResponse(songs=songs)

    return response
