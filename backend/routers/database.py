import logging
from typing import Annotated

from fastapi import APIRouter, Depends, Request

from modules.database_info import DatabaseInfoManager
from modules.logger import get_endpoint_logger
from schemas.database import DatabaseListResponse, SongData, SongDataRequest

# APIRouterの定義
router = APIRouter(prefix="/database", tags=["database"])


def get_database_info_manager(req: Request) -> DatabaseInfoManager:
    """データベース情報管理クラスを取得する関数

    Args:
        req (Request): APIエンドポイントのRequestオブジェクト

    Returns:
        DatabaseInfoManager: データベース情報管理クラスのインスタンス
    """
    db_manager: DatabaseInfoManager = req.app.state.db_manager
    return db_manager


@router.get(
    "/list",
    response_model=DatabaseListResponse,
    summary="データベースの表示データ一覧を取得",
)
async def get_database_list(
    db_manager: Annotated[DatabaseInfoManager, Depends(get_database_info_manager)],
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> DatabaseListResponse:
    """データベースページに表示するデータ一覧を取得"""
    api_logger.debug("データベースの表示データ一覧を取得します")

    # 各DBの概要データのリストをまとめたデータを取得
    database_list_data = db_manager.get_database_list_data()

    return database_list_data


@router.get(
    "/song_data",
    response_model=SongData,
    summary="楽曲の詳細情報を取得する",
)
async def get_song_data(
    query: Annotated[SongDataRequest, Depends()],
    db_manager: Annotated[DatabaseInfoManager, Depends(get_database_info_manager)],
    api_logger: Annotated[logging.Logger, Depends(get_endpoint_logger)],
) -> SongData:
    """楽曲の詳細情報を取得"""
    song_id = query.song_id
    api_logger.debug(f"楽曲の詳細情報データ一覧を取得します: {song_id}")

    # 楽曲ID指定で楽曲の情報を取得
    song_data = db_manager.get_song_database(song_id=song_id)

    return song_data
