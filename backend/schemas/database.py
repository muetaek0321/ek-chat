from pydantic import Field

from schemas.common import EndpointModel


class SongDataOutline(EndpointModel):
    """楽曲DBの概要データ"""

    id: str = Field(..., description="楽曲ID")
    title: str = Field(..., description="楽曲名")


class DatabaseListResponse(EndpointModel):
    """チャットの情報を表すBaseModel"""

    songs: list[SongDataOutline] = Field(..., description="楽曲DBのデータリスト")


class SongIncludedIn(EndpointModel):
    """楽曲の収録作品情報"""

    type: str = Field(..., description="収録作品の種別（例: シングル, アルバム, ベストアルバム）")
    title: str = Field(..., description="収録作品のタイトル")


class SongBackground(EndpointModel):
    """楽曲の制作背景情報"""

    description: str = Field(..., description="制作背景の説明")
    artist_comment: str | None = Field(default=None, description="アーティストのコメント")


class SongMusicalFeatures(EndpointModel):
    """楽曲の音楽的特徴情報"""

    genre: list[str] = Field(default_factory=list, description="ジャンル一覧")
    description: str = Field(..., description="音楽的特徴の説明")


class SongReception(EndpointModel):
    """楽曲の評価・受容情報"""

    description: str = Field(..., description="評価・受容の説明")


class SongRelatedInformation(EndpointModel):
    """楽曲の関連情報（タイアップ、ミュージックビデオ等）"""

    type: str = Field(..., description="関連情報の種別（例: タイアップ, ミュージックビデオ）")
    title: str = Field(..., description="関連情報のタイトル")
    description: str = Field(..., description="関連情報の説明")


class SongDetails(EndpointModel):
    """楽曲の詳細情報"""

    background: SongBackground | None = Field(default=None, description="制作背景情報")
    musical_features: SongMusicalFeatures | None = Field(default=None, description="音楽的特徴情報")
    reception: SongReception | None = Field(default=None, description="評価・受容情報")
    related_information: list[SongRelatedInformation] = Field(
        default_factory=list, description="関連情報リスト"
    )


class SongData(EndpointModel):
    """楽曲の詳細データ"""

    id: str = Field(..., description="楽曲ID")
    title: str = Field(..., description="楽曲名")
    artist: str = Field(..., description="アーティスト名")
    release_date: str = Field(..., description="リリース日（YYYY-MM-DD）")
    lyrics: list[str] = Field(default_factory=list, description="作詞者リスト")
    music: list[str] = Field(default_factory=list, description="作曲者リスト")
    included_in: list[SongIncludedIn] = Field(default_factory=list, description="収録作品リスト")
    details: SongDetails = Field(..., description="楽曲の詳細情報")
    youtube_video_id: list[str] = Field(default_factory=list, description="YouTube動画IDリスト")
