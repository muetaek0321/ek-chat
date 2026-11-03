import json
import os
from pathlib import Path

import pandas as pd

from modules.logger import get_logger
from schemas.database import DatabaseListResponse, SongData, SongDataOutline

# ロガー設定
logger = get_logger(__name__)


class DatabaseInfoManager:
    """データベース情報の管理クラス"""

    def __init__(self) -> None:
        """初期化"""
        self.songs_data_path = Path(os.getenv("SONGS_DATA_PATH", "./develop/songs.parquet"))
        self.songs_db: pd.DataFrame = pd.DataFrame(columns=["title", "db"])

    def load_songs_database(self, path: Path | None = None) -> pd.DataFrame:
        """楽曲情報データベースを読み込む。

        Args:
            path: 読み込み対象のファイルパス。指定がない場合は SONGS_DATA_PATH を使用。

        Returns:
            pd.DataFrame: 読み込まれた楽曲情報データ。
        """
        data_path = path or self.songs_data_path

        if data_path.exists():
            self.songs_db = pd.read_parquet(data_path, columns=["title", "db"])
            logger.info(f"楽曲情報データを読み込みました: {data_path} ({len(self.songs_db)}件)")
        else:
            logger.warning(f"楽曲情報データが見つかりません: {data_path}")
            self.songs_db = pd.DataFrame(columns=["title", "db"])

        return self.songs_db

    def get_database_list_data(self) -> DatabaseListResponse:
        """データベースのリストを取得

        Returns:
            DatabaseListResponse: データベースの一覧データ
        """
        # 未読み込みかつファイルが存在する場合は自動読み込み
        if self.songs_db.empty and self.songs_data_path.exists():
            self.songs_db = self.load_songs_database()

        # DBが空の行を除外
        songs_df = self.songs_db[self.songs_db["db"].notna()]

        # 楽曲情報のリストを作成
        songs = [SongDataOutline(id=idx, title=row["title"]) for idx, row in songs_df.iterrows()]

        # レスポンスデータの作成
        # NOTE: 現状は楽曲情報のみだが今後追加する可能性あり
        response = DatabaseListResponse(songs=songs, releases=[])

        return response

    def get_song_database(self, song_id: str) -> SongData:
        """楽曲IDに基づいて楽曲の詳細情報を取得

        Returns:
            SongData: 楽曲データ
        """
        # 未読み込みかつファイルが存在する場合は自動読み込み
        if self.songs_db.empty and self.songs_data_path.exists():
            self.songs_db = self.load_songs_database()

        # 楽曲情報を取得
        song_db_path = Path(self.songs_db.loc[song_id, "db"])
        if not song_db_path.exists():
            raise FileNotFoundError(f"楽曲DBが見つかりません: {song_db_path}")

        # 楽曲DBの読み込み
        with open(song_db_path, "r", encoding="utf-8") as f:
            song_data = SongData.model_validate(json.load(f))

        return song_data
