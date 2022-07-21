# -*- coding: utf-8 -*-

from datetime import datetime
from bisect import bisect_left

import numpy as np


def convert_emotion_value_to_text(emotion_value: float) -> str:
    '''
    感情値に応じたラベルを返します．
    '''
    if emotion_value == -.1:
        return 'なんともいえない..'
    if emotion_value < 0:
        return 'ネガティブかも？'
    if emotion_value >= 0:
        return 'ポジティブ！'


def convert_emotion_value_to_rgba(emotion_value: float, sep: int = None) -> str:
    '''
    感情値からrgba値を返します．
    sep引数が与えられた場合，<sep>段階の断続的な値を，
    sep引数が与えられない場合，rgb(0,255,0)~rgb(255,0,0)までの連続的な値を返します．
    特に感情値が-0.1の場合，背景色は適用されません．
    >>> convert_emotion_value_to_rgba(1)
    'rgba(0, 255, 0, 0.3)'
    >>> convert_emotion_value_to_rgba(-1)
    'rgba(255, 0, 0, 0.3)'
    '''
    if emotion_value == -.1:
        return 'rgba(0, 0, 0, 0)'
    if sep is None:
        coef = round(255 / 2 * emotion_value + 255 / 2)
    else:
        breakpoints = np.linspace(-1, 1, sep)
        coes = np.append(np.linspace(0, 255, sep), 255)
        coef = round(coes[bisect_left(breakpoints, emotion_value)])
    return f'rgba({255-coef}, {coef}, 0, 0.2)'


def format_time_delta(before: datetime, after: datetime) -> str:
    '''
    前後のdatetimeの差分を最大の単位を付与して返します．
    '''
    delta = (after - before).seconds
    if delta // 86400:
        return f'{delta // 86400}日前'
    if delta // 3600:
        return f'{delta // 3600}時間前'
    if delta // 60:
        return f'{delta // 60}分前'
    if delta // 1:
        return f'{delta // 1}秒前'
    return f'ちょっと前'
