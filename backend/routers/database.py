import logging
from typing import Annotated

from fastapi import APIRouter, Depends

from modules.get_database_list import get_database_list_data
from modules.logger import get_endpoint_logger
from schemas.database import DatabaseListResponse

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
