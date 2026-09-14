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

    def extract_songs(self, input_text: str) -> list[str]:
        """入力テキストから曲名を抽出する

        Args:
            input_text (str): 入力テキスト

        Returns:
            list[str]: 抽出された曲名のリスト
        """
        return [title for _, title in self.automaton.iter(input_text)]


if __name__ == "__main__":
    # test

    input_text = "漂う人の性とDEAD OR ALIVEが好きです。"
    extractor = SongsExtractor()
    songs = extractor.extract_songs(input_text)
    print(songs)
