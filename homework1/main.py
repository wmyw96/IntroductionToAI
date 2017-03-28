#!/usr/bin/env python
# -*- coding: utf-8 -*-

from methods import astar_pinyin, build_language_model
from utils import load_pinyin, load_language_model
import re

MODEL = True

if __name__ == '__main__':
    input_file = open('data/input.txt', 'r')
    token_set, pydict = load_pinyin('data/pinyin.txt', 'data/tokens.txt')

    if not MODEL:
        build_language_model(token_set, ['corpus/2016-01.txt', 'corpus/2016-02.txt', 'corpus/2016-03.txt',
                                         'corpus/2016-04.txt', 'corpus/2016-05.txt', 'corpus/2016-04.txt',
                                         'corpus/2016-07.txt', 'corpus/2016-08.txt', 'corpus/2016-09.txt',
                                         'corpus/2016-10.txt', 'corpus/2016-11.txt'], ngram=1)

    model = load_language_model(ngram=2, significance=0.95)

    pattern = re.compile(r'[a-z]+')
    for line in input_file:
        tokens = re.findall(pattern, line)
        ans = astar_pinyin(tokens, model)
        print(ans)

