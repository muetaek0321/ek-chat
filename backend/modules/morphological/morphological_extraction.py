"""
ビルドコマンド:
uv run sudachipy ubuild -s backend/.venv/Lib/site-packages/sudachidict_core/resources/system.dic F:/elephantkashimashi/keywords.csv
"""

import sudachipy


class MorphologicalExtraction:
    """SudachiPyを用いた形態素解析を行い、形態素の情報を取得するクラス"""

    def __init__(self):
        """初期化"""
        # SudachiPyの辞書から形態素解析器を作成
        dictionary = sudachipy.Dictionary(config_path="./modules/morphological/sudachi.json")
        self.tokenizer = dictionary.create()

    def extract_songs(self, input_text: str) -> list:
        morphemes = self.tokenizer.tokenize(input_text, sudachipy.SplitMode.C)

        # 形態素の品詞情報を取得し、曲名に該当する形態素を抽出
        songs = [m.normalized_form() for m in morphemes if m.part_of_speech()[2] == "曲名"]

        for m in morphemes:
            print(m.surface(), m.part_of_speech(), m.normalized_form())
        return songs


if __name__ == "__main__":
    # test

    input_text = "風と四月の風が好きです。"
    extractor = MorphologicalExtraction()
    songs = extractor.extract_songs(input_text)
    print(songs)
