import os
from pathlib import Path

import ahocorasick
import pandas as pd

from modules.logger import get_logger

# ロガー設定
logger = get_logger(__name__)


class SongsExtractor:
    """楽曲名抽出クラス"""

    def __init__(
        self,
        songs_df: pd.DataFrame | None = None,
        auto_load: bool = False,
    ) -> None:
        """初期化。

        Args:
            songs_df: 事前に読み込まれた楽曲情報DataFrame。指定された場合はこれを用いてオートマトンを構築します。
            auto_load: Trueの場合、songs_dfが未指定でも初期化時に自動でファイルを読み込みます。
        """
        # データ格納先のディレクトリ
        self.songs_data_path = Path(os.getenv("SONGS_DATA_PATH", "./develop/songs.parquet"))
        self.automaton = ahocorasick.Automaton()
        self.is_available = False
        self.songs_df = pd.DataFrame(columns=["title"])
        self.songs_ids: dict[str, str] = {}

        if songs_df is not None:
            self.load_data(songs_df=songs_df)
        elif auto_load:
            self.load_data()

    def load_data(self, songs_df: pd.DataFrame | None = None) -> None:
        """楽曲データを読み込み、曲名抽出用オートマトンを構築する。

        Args:
            songs_df: 外部から渡す楽曲情報DataFrame。Noneの場合はファイルから読み込みます。
        """
        if songs_df is not None:
            self.songs_df = songs_df[["title"]] if "title" in songs_df.columns else songs_df
            self.is_available = not self.songs_df.empty
        else:
            self.is_available = self.songs_data_path.exists()
            if self.is_available:
                self.songs_df = pd.read_parquet(self.songs_data_path, columns=["title"])
            else:
                # NOTE: データが存在しない場合は空のデータフレームを作成して対応
                logger.warning(f"楽曲情報データが見つかりません: {self.songs_data_path}")
                self.songs_df = pd.DataFrame(columns=["title"])

        # Trie木からオートマトンを再生成
        self.automaton = ahocorasick.Automaton()
        self.songs_ids = {}

        if self.is_available and not self.songs_df.empty:
            for id, row in self.songs_df.iterrows():
                title = row["title"]
                # 楽曲名とIDの対応データの作成
                self.songs_ids[title] = id
                # 楽曲名をオートマトンに追加
                self.automaton.add_word(title, title)

            self.automaton.make_automaton()
            logger.info(f"曲名抽出用オートマトンを構築しました: {len(self.songs_ids)}曲")

    def _remove_overlapping_matches(self, matches: list[tuple[int, int, str]]) -> list[str]:
        """重複、内包する単語を除いて抽出する単語を選択する。

        Args:
            matches: 抽出したい単語とその出現位置を格納したリスト

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
        """入力テキストから楽曲名を抽出する。

        Args:
            input_text: 入力テキスト

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
    extractor = SongsExtractor(auto_load=True)
    songs = extractor.extract_songs(input_text)
    print(songs)
