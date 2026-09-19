import csv
from pathlib import Path

import ahocorasick

DEFAULT_CSV_PATH = Path("F:/elephantkashimashi/keywords.csv")


class SongsExtractor:
    """曲名抽出クラス"""

    def __init__(self, csv_path: Path | str = DEFAULT_CSV_PATH) -> None:
        """CSVから曲名リストを読み込み、Aho-Corasickオートマトンを構築する

        Args:
            csv_path (Path | str): 曲名キーワードが記述されたCSVのパス
        """
        self.csv_path = Path(csv_path)
        self.automaton = ahocorasick.Automaton()

        # csvを読み込んで曲名リストを取得
        with self.csv_path.open(mode="r", encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if not row:
                    continue
                song_name = row[0].strip()
                if not song_name:
                    continue
                self.automaton.add_word(song_name, song_name)

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
        """入力テキストから曲名を抽出する

        Args:
            input_text (str): 入力テキスト

        Returns:
            list[str]: 抽出された曲名のリスト
        """
        # 抽出したい単語と出現位置を格納
        matches = []
        for end_index, title in self.automaton.iter(input_text):
            start_index = end_index - len(title) + 1
            matches.append((start_index, end_index, title))

        # 重複や内包されているものを除外
        songs = self._remove_overlapping_matches(matches)

        return songs


if __name__ == "__main__":
    # test

    input_text = "漂う人の性とDEAD OR ALIVEが好きです。"
    extractor = SongsExtractor()
    songs = extractor.extract_songs(input_text)
    print(songs)
