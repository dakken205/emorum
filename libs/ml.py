# -*- coding: utf-8 -*-

import pandas as pd

from janome.tokenizer import Tokenizer
from janome.analyzer import Analyzer
from janome.charfilter import UnicodeNormalizeCharFilter
from janome.tokenfilter import POSKeepFilter, POSStopFilter, LowerCaseFilter


tokenizer = Tokenizer()
token_filters = [
    POSKeepFilter(['名詞',
                   '形容詞',
                   ]),
    POSStopFilter(['名詞, 数',
                   '名詞, 代名詞',
                   '名詞, 非自立',
                   '名詞, 接頭',
                   '名詞, 接尾',
                   ]),
    LowerCaseFilter()
]
char_filters = [UnicodeNormalizeCharFilter()]
stopwords = []
analyzer = Analyzer(char_filters=char_filters,
                    tokenizer=tokenizer,
                    token_filters=token_filters)


def token2wakati(tokens):
    return ' '.join(t.base_form for t in tokens)


def TextScore(document):
    total = 0
    for e in token2wakati(analyzer.analyze(document)).split():
        if e in Dic.keys():
            total += Dic[e]
    return total


df = pd.read_csv("./model/emotion_model.csv")

Dic = dict(df[['name', 'score']].values)
