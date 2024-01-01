# -*- coding: utf-8 -*-

import dataclasses
import json
import typing as t

import janome.charfilter as charfilter  # type: ignore
import janome.tokenfilter as tokenfilter  # type: ignore
from janome.analyzer import Analyzer  # type: ignore
from janome.tokenizer import Token, Tokenizer  # type: ignore

from .utils import RGB

__all__ = [
    "Emotion",
    "Evaluator",
]


@dataclasses.dataclass
class Emotion:
    raw_text: str
    value: float

    @property
    def label(self):
        """感情値に対応したラベルを返す。"""

        if self.value == -0.1:
            return "なんともいえない.."
        elif self.value < 0:
            return "ネガティブかも？"
        else:
            return "ポジティブ！"

    @property
    def rgb(self):
        """clamp(-1, 1, emotion_value) に対して、赤から緑へのグラデーションを返す。"""

        if self.value == -0.1:
            return RGB(241, 242, 245)

        if self.value < -1:
            weight = 0
        elif self.value < -0.5:
            weight = 0.2
        elif self.value < 0:
            weight = 0.4
        elif self.value < 0.5:
            weight = 0.6
        elif self.value < 1:
            weight = 0.8
        else:
            weight = 1

        coef = round(255 * weight)
        return RGB(255 - coef, coef, 0)


class Evaluator:
    _tokenizer: t.Final = Tokenizer()
    _token_filters: t.Final[list[tokenfilter.TokenFilter]] = [
        tokenfilter.POSKeepFilter(
            [
                "名詞",
                "形容詞",
            ]
        ),
        tokenfilter.POSStopFilter(
            [
                "名詞, 数",
                "名詞, 代名詞",
                "名詞, 非自立",
                "名詞, 接頭",
                "名詞, 接尾",
            ]
        ),
        tokenfilter.LowerCaseFilter(),
    ]
    _char_filters: t.Final[list[charfilter.CharFilter]] = [
        charfilter.UnicodeNormalizeCharFilter(),
    ]
    _analyzer: t.Final = Analyzer(
        char_filters=_char_filters,
        tokenizer=_tokenizer,
        token_filters=_token_filters,
    )

    with open("./model/emotion_model.json", "r") as f:
        model: t.Final[dict[str, float]] = json.load(f)

    _intercept: t.Final[float] = -0.1

    @classmethod
    def _to_wakati(cls, text: str) -> list[str]:
        wakati: list[str] = []
        for token in cls._tokenizer.tokenize(text):
            token = t.cast(Token, token)
            if any(token.part_of_speech.startswith(e) for e in ("動詞", "名詞")):
                wakati.append(token.base_form)
        return wakati

    @classmethod
    def _to_emotion_value(cls, text: str) -> float:
        return (
            sum(
                cls.model.get(token.base_form, 0)
                for token in cls._analyzer.analyze(text)
            )
            + cls._intercept
        )

    @classmethod
    def evaluate(cls, text: str) -> Emotion:
        return Emotion(
            raw_text=text,
            value=cls._to_emotion_value(text),
        )
