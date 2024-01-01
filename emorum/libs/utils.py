# -*- coding: utf-8 -*-

import dataclasses
import datetime

__all__ = [
    "RGB",
    "format_time_delta",
]


@dataclasses.dataclass
class RGB:
    r: int
    g: int
    b: int

    def __repr__(self) -> str:
        return f"rgb({self.r}, {self.g}, {self.b})"


def format_time_delta(before: datetime.datetime, after: datetime.datetime) -> str:
    """
    datetimeの差分のうち、値が1以上となる最大の単位の部分を返す。

    >>> from datetime import datetime
    >>> format_time_delta(datetime(2021, 1, 1, 0, 0, 0),
    ...                   datetime(2021, 1, 1, 0, 0, 30))
    '30秒前'
    >>> format_time_delta(datetime(2021, 1, 1, 0, 0, 0),
    ...                   datetime(2021, 1, 4, 0, 0, 0))
    '3日前'
    >>> format_time_delta(datetime(2021, 1, 1, 0, 0, 0),
    ...                   datetime(2021, 1, 1, 0, 0, 0))
    'ちょっと前'
    """

    delta_day = (after - before).days
    delta_sec = (after - before).seconds

    if delta_day:
        return f"{delta_day}日前"
    if delta_sec // 3600:
        return f"{delta_sec // 3600}時間前"
    if delta_sec // 60:
        return f"{delta_sec // 60}分前"
    if delta_sec // 1:
        return f"{delta_sec // 1}秒前"

    return "ちょっと前"


if __name__ == "__main__":
    import doctest

    doctest.testmod()
