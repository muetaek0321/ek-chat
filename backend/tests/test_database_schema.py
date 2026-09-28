import json

from schemas.database import SongData


class TestDatabaseSchema:
    """database.pyのスキーマテスト"""

    def test_song_data_from_json(self):
        """提供されたJSON形式データからSongDataが正しく生成・パースできることを検証"""
        json_data = {
            "id": "song_0050",
            "title": "笑顔の未来へ",
            "artist": "エレファントカシマシ",
            "release_date": "2008-01-01",
            "lyrics": ["宮本浩次"],
            "music": ["宮本浩次"],
            "included_in": [
                {"type": "シングル", "title": "笑顔の未来へ"},
                {"type": "アルバム", "title": "STARTING OVER"},
                {"type": "ベストアルバム", "title": "THE BEST 2007-2012 俺たちの明日"},
                {"type": "ベストアルバム", "title": "All Time Best Album THE FIGHTING MAN"},
            ],
            "details": {
                "background": {
                    "description": "ユニバーサルミュージック移籍後の第二弾シングルとして制作。2007年4月の初披露時には「涙のテロリスト」というタイトルであったが、その後のライブを経て「笑顔の未来へ」へと改称された。前作のカップリングに続き、蔦谷好位置がプロデュースおよび共同編曲を担当している。",
                    "artist_comment": "アレンジャーの蔦谷好位置が制作したデモ音源を聴いた宮本浩次は、自身の内面を鋭く捉えた音作りに涙を流し、「なんで俺の気持ちわかるんですかぁ!!」と深い感激と信頼を表明した。",
                },
                "musical_features": {
                    "genre": ["J-POP", "ロック"],
                    "description": "ストリングスとピアノを大胆に配した、透明感と疾走感溢れるポップロック。宮本浩次の繊細かつ情感豊かなボーカル表現と、バンドとしてのソリッドなグルーヴが融合したミディアムテンポの楽曲。冬ソングとしての抒情性と力強い生命力を内包する。",
                },
                "reception": {
                    "description": "元旦発売という特殊な流通スケジュールにより、オリコン週間チャートでは合算週の歪みを受けて47位に留まるものの、JAPAN COUNTDOWNでは最高3位を獲得するなど、実質的な支持の広さを示した。同業者であるいきものがかりの吉岡聖恵が「2008年に最も聴いた楽曲」として絶賛している。",
                },
                "related_information": [
                    {
                        "type": "タイアップ",
                        "title": "ダウンタウンDX",
                        "description": "2007年12月から2008年1月まで、読売テレビ（日本テレビ系列）全国ネット「ダウンタウンDX」のエンディングテーマとして起用された。",
                    },
                    {
                        "type": "ミュージックビデオ",
                        "title": "「笑顔の未来へ」ミュージックビデオ",
                        "description": "写真家・佐内正史が監督を務め、白いシャツを纏った宮本浩次と赤いワンピースを着た5歳のモデルであるカノン・ジャンが共演。過度な演出を排し、両者の自然体のやり取りをドキュメンタリー調に切り取った映像作品。",
                    },
                ],
            },
            "youtubeVideoId": ["jHmpt5et9bk", "nC4QwiFWWJ0"],
        }

        # 辞書からのバリデーション
        song = SongData.model_validate(json_data)
        assert song.id == "song_0050"
        assert song.title == "笑顔の未来へ"
        assert song.artist == "エレファントカシマシ"
        assert song.release_date == "2008-01-01"
        assert song.lyrics == ["宮本浩次"]
        assert song.music == ["宮本浩次"]
        assert len(song.included_in) == 4
        assert song.included_in[0].type == "シングル"
        assert song.included_in[0].title == "笑顔の未来へ"

        # detailsの検証
        assert song.details.background is not None
        assert "涙のテロリスト" in song.details.background.description
        assert song.details.background.artist_comment is not None
        assert "なんで俺の気持ちわかるんですかぁ!!" in song.details.background.artist_comment

        assert song.details.musical_features is not None
        assert song.details.musical_features.genre == ["J-POP", "ロック"]
        assert "ストリングス" in song.details.musical_features.description

        assert song.details.reception is not None
        assert "JAPAN COUNTDOWN" in song.details.reception.description

        assert len(song.details.related_information) == 2
        assert song.details.related_information[0].type == "タイアップ"
        assert song.details.related_information[0].title == "ダウンタウンDX"

        # youtubeVideoIdの検証（alias経由）
        assert song.youtube_video_id == ["jHmpt5et9bk", "nC4QwiFWWJ0"]

        # JSON文字列からのバリデーション
        json_str = json.dumps(json_data, ensure_ascii=False)
        song_from_json = SongData.model_validate_json(json_str)
        assert song_from_json.id == "song_0050"
        assert song_from_json.youtube_video_id == ["jHmpt5et9bk", "nC4QwiFWWJ0"]

        # camelCaseでのシリアライズ検証（EndpointModelの動作）
        dumped_alias = song.model_dump(by_alias=True)
        assert "releaseDate" in dumped_alias
        assert "includedIn" in dumped_alias
        assert "youtubeVideoId" in dumped_alias
        assert "artistComment" in dumped_alias["details"]["background"]
        assert "musicalFeatures" in dumped_alias["details"]
        assert "relatedInformation" in dumped_alias["details"]

    def test_song_data_optional_defaults(self):
        """オプショナル項目のデフォルト値検証"""
        minimal_data = {
            "id": "song_9999",
            "title": "テスト楽曲",
            "artist": "テストアーティスト",
            "release_date": "2020-01-01",
            "details": {
                "background": {"description": "背景説明"},
                "musical_features": {"description": "音楽特徴説明"},
                "reception": {"description": "評価説明"},
            },
        }
        song = SongData.model_validate(minimal_data)
        assert song.lyrics == []
        assert song.music == []
        assert song.included_in == []
        assert song.youtube_video_id == []
        assert song.details.background.artist_comment is None
        assert song.details.musical_features.genre == []
        assert song.details.related_information == []
