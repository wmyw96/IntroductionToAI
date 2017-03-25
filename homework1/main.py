#!/usr/bin/env python
# -*- coding: utf-8 -*-

from methods import astar, build_language_model
from utils import load_pinyin, load_corpus
import re

MODEL = False

if __name__ == '__main__':
    input_file = open('data/input.txt', 'r')
    pydict = load_pinyin('data/pinyin.txt', 'data/tokens.txt')

    if not MODEL:
        build_language_model(['corpus/2016-11.txt'])
    pattern = re.compile(r'[a-z]+')
    corpus = load_corpus('data')
    for line in input_file:
        tokens = re.findall(pattern, line)
        ans = astar(tokens)
        print(ans)

