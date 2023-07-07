from enum import Enum
from typing import Any


def transform_enum_to_tuple(enum: Enum):
    return list(map(lambda value: (value.value, value.value), enum.__iter__()))


def generateHttpResponse(
    data: Any | None = None,
    error: str | list[str] | None = None,
    message: str | list[str] | None = None,
):
    return {
        "result": data,
        "error": error,
        "message": message,
        "skipResponseFormatter": True,
    }
