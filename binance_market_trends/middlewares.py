import logging
from http import HTTPStatus

from fastapi import Request, Response

logger = logging.getLogger(__name__)


async def catch_exceptions_middleware(request: Request, call_next):
    try:
        return await call_next(request)
    except Exception as err:
        logger.exception({
            'message': str(err),
        })
        return Response(status_code=HTTPStatus.INTERNAL_SERVER_ERROR, content=HTTPStatus.INTERNAL_SERVER_ERROR.phrase)
