import os
from pathlib import Path

import ahocorasick
import pandas as pd

from modules.logger import get_logger

# ロガー設定
logger = get_logger(__name__)


class SongsExtractor:
    """楽曲名抽出クラス"""

    def __init__(self) -> None:
        """初期化"""
        # データ格納先のディレクトリ
        self.songs_data_path = Path(os.getenv("SONGS_DATA_PATH", "./develop/songs.parquet"))
        self.automaton = ahocorasick.Automaton()
        self.is_available = self.songs_data_path.exists()

        # 曲名リストを取得
        if self.is_available:
            self.songs_df = pd.read_parquet(self.songs_data_path, columns=["title"])
        else:
            # NOTE: データが存在しない場合は空のデータフレームを作成して対応
            logger.warning(f"楽曲情報データが見つかりません: {self.songs_data_path}")
            self.songs_df = pd.DataFrame(columns=["title"])

        self.songs_ids = {}
        for id, row in self.songs_df.iterrows():
            title = row["title"]
            # 楽曲名とIDの対応データの作成
            self.songs_ids[title] = id
            # 楽曲名をオートマトンに追加
            self.automaton.add_word(title, title)

        # Trie木からオートマトンを生成
        self.automaton.make_automaton()

    def _remove_overlapping_matches(self, matches: list[tuple[int, int, str]]) -> list[str]:
        """重複、内包する単語を除いて抽出する単語を選択す

        Args:
            matches (list[tuple[int, int, str]]): 抽出したい単語とその出現位置を格納したリスト

        Returns:
            list[str]: 抽出した単語のリスト
        """

        # 長い単語を優先
        matches = sorted(matches, key=lambda x: (-(x[1] - x[0] + 1), x[0]))

        # 重複や内包されたものを除いて単語抽出
        selected = []
        for start, end, word in matches:
            # すでに採用した単語と範囲が重なっているか確認
            overlap = any(
                start <= selected_end and end >= selected_start
                for selected_start, selected_end, _ in selected
            )

            if not overlap:
                selected.append((start, end, word))

        # 単語のみを取得
        words = [word for _, _, word in selected]

        return words

    def extract_songs(self, input_text: str) -> list[str]:
        """入力テキストから楽曲名を抽出する

        Args:
            input_text (str): 入力テキスト

        Returns:
            list[str]: 抽出された楽曲名のリスト
        """
        if not self.is_available:
            logger.warning("楽曲情報データが存在しないため、抽出をスキップします")
            return []

        # 抽出したい単語と出現位置を格納
        matches = []
        for end_index, title in self.automaton.iter(input_text):
            start_index = end_index - len(title) + 1
            matches.append((start_index, end_index, title))

        # 重複や内包されているものを除外
        songs = self._remove_overlapping_matches(matches)
        # 楽曲名をIDに変換
        ids = [self.songs_ids[title] for title in songs]

        return ids


if __name__ == "__main__":
    # test

    input_text = "漂う人の性とDEAD OR ALIVEが好きです。"
    extractor = SongsExtractor()
    songs = extractor.extract_songs(input_text)
    print(songs)
