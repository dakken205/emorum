# -*- coding: utf-8 -*-

from datetime import datetime
from bisect import bisect_left

import numpy as np


def convert_emotion_value_to_text(emotion_value: float, border: "float | int" = .0) -> str:
    '''
    感情値をラベリングします．
    '''
    if emotion_value < border:
        return 'ネガティブかも？'
    if emotion_value > border:
        return 'ポジティブ！'
    if emotion_value == border:
        return 'なんともいえない..'


def convert_emotion_value_to_rgba(emotion_value: float, sep: int = None) -> str:
    '''
    感情値をrgba値に変換します．sep段階の断続値に，sep引数が与えられない場合は連続値に変換されます．
    >>> convert_emotion_value_to_rgba(1)
    'rgba(0, 255, 0, 0.3)'
    >>> convert_emotion_value_to_rgba(-1)
    'rgba(255, 0, 0, 0.3)
    '''
    if sep is None:
        coe = round(255 / 2 * (emotion_value - .1) + 255 / 2)
    else:
        breakpoints = np.linspace(-1, 1, sep)
        coes = np.append(np.linspace(0, 255, sep), 255)
        coe = round(coes[bisect_left(breakpoints, emotion_value)])
    return f'rgba({255-coe}, {coe}, 0, 0.3)'


def format_time_delta(before: datetime, after: datetime) -> str:
    '''
    前後のdatetimeの差分を最大の単位を付与して返します．
    '''
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
