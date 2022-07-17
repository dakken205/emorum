# -*- coding: utf-8 -*-

from datetime import datetime
from bisect import bisect_left


def convert_emotion_value_to_text(emotion_value: float) -> str:
    if emotion_value < .1:
        return 'ネガティブかも？'
    if emotion_value > .1:
        return 'ポジティブ！'
    if emotion_value == 1:
        return 'なんともいえない..'

def convert_emotion_value_to_rgba(emotion_value: float) -> str:
    coe = round(- 255 / 2 * emotion_value + 255 / 2)
    return f'rgba({coe}, {255-coe}, 0, 0.4)'


def format_time_delta(before: datetime, after: datetime) -> str:
    delta = (after - before).seconds
    if (days := delta // 86400):
        return f'{days}日前'
    if (hours := delta // 3600):
        return f'{hours}時間前'
    if (minutes := delta // 60):
        return f'{minutes}分前'
    if (seconds := delta // 1):
        return f'{seconds}秒前'
    return f'ちょっと前'