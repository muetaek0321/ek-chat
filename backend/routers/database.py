import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from modules.get_database_info import get_database_list_data, get_song_database
from modules.logger import get_endpoint_logger
from schemas.database import DatabaseListResponse, SongData, SongDataRequest

# APIRouterの定義
router = APIRouter(prefix="/database", tags=["database"])


@router.get(
    "/list",
    response_model=DatabaseListResponse,
    summary="データベースの表示データ一覧を取得",
)
async def get_database_list(
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> DatabaseListResponse:
    """データベースページに表示するデータ一覧を取得"""
    api_logger.debug("データベースの表示データ一覧を取得します")

    # 各DBの概要データのリストをまとめたデータを取得
    database_list_data = get_database_list_data()

    return database_list_data


@router.get(
    "/song_data",
    response_model=SongData,
    summary="楽曲の詳細情報を取得する",
)
async def get_song_data(
    query: Annotated[SongDataRequest, Depends()],
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> SongData:
    """楽曲の詳細情報を取得"""
    song_id = query.song_id
    api_logger.debug(f"楽曲の詳細情報データ一覧を取得します: {song_id}")

    # 楽曲ID指定で楽曲の情報を取得
    song_data = get_song_database(song_id=song_id)

    return song_data
