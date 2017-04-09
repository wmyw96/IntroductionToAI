#!/usr/bin/env python
# -*- coding: utf-8 -*-

from methods import astar_pinyin, build_language_model
from utils import load_pinyin, load_language_model
from methods import calc_log_prob
import re

MODEL = True

if __name__ == '__main__':
    input_file = open('data/input.txt', 'r')
    token_set, pydict = load_pinyin('data/pinyin.txt', 'data/tokens.txt')

    if not MODEL:
        build_language_model(token_set,
                             ['corpus/2016-01.txt', 'corpus/2016-02.txt',
                              'corpus/2016-03.txt', 'corpus/2016-04.txt',
                              'corpus/2016-05.txt', 'corpus/2016-06.txt',
                              'corpus/2016-07.txt', 'corpus/2016-08.txt',
                              'corpus/2016-09.txt', 'corpus/2016-10.txt',
                              'corpus/2016-11.txt'],
                             ngram=4, significance=0.95)

    model = load_language_model(ngram=4, significance=0.95)

    pattern = re.compile(r'[a-z]+')

    #print(calc_log_prob('清华大学计算机系'.decode('utf-8'), model, ngram=2))
    #print(calc_log_prob('氢化大学计算机系'.decode('utf-8'), model, ngram=2))
    #print(calc_log_prob('比起你年轻时的魅力'.decode('utf-8'), model, ngram=2))
    #print(calc_log_prob('有在偷懒吗'.decode('utf-8'), model, ngram=4))
    print(calc_log_prob('拟的世界会变得更精彩'.decode('utf-8'), model, ngram=4))
    print(calc_log_prob('你的世界会变得更精彩'.decode('utf-8'), model, ngram=4))
    #print(calc_log_prob('黄昏与月光一起升起来'.decode('utf-8'), model, ngram=2))
    '''for line in input_file:
        tokens = re.findall(pattern, line)
        ans, log_prob = astar_pinyin(tokens, pydict, model, ngram=4)
        print(ans)
        print(log_prob)'''
