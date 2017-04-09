#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import time
sys.path.append("../source")
from methods import astar_pinyin, build_language_model
from utils import load_pinyin, load_language_model
import re

MODEL = True

if __name__ == '__main__':
    input_file_name = '../data/input.txt'
    output_file_name = '../data/output.txt'
    if len(sys.argv) >= 3:
        input_file_name = sys.argv[1]
        output_file_name = sys.argv[2]
        print("[INFO] Input file name: '%s', output file name '%s'"
              % (input_file_name, output_file_name))
    else:
        print("[INFO] Use default input file name: '%s', output file name '%s'"
              % (input_file_name, output_file_name))

    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')
    token_set, pydict = load_pinyin('../data/pinyin.txt',
                                    '../data/tokens.txt')

    if not MODEL:
        build_language_model(token_set,
                             ['../corpus/2016-01.txt', '../corpus/2016-02.txt',
                              '../corpus/2016-03.txt', '../corpus/2016-04.txt',
                              '../corpus/2016-05.txt', '../corpus/2016-06.txt',
                              '../corpus/2016-07.txt', '../corpus/2016-08.txt',
                              '../corpus/2016-09.txt', '../corpus/2016-10.txt',
                              '../corpus/2016-11.txt'],
                             ngram=4, significance=0.95)

    model = load_language_model(ngram=4, significance=0.95)

    pattern = re.compile(r'[a-z]+')

    tot = 0
    for line in input_file:
        tot = tot + 1
    input_file.close()
    input_file = open(input_file_name, 'r')
    cur = 0
    for line in input_file:
        tokens = re.findall(pattern, line)
        time_epoch = -time.time()
        ans, log_prob = astar_pinyin(tokens, pydict, model, ngram=4)
        time_epoch += time.time()
        cur = cur + 1
        print('[INFO] Searching..., solved %d out of %d, using time %.3f s'
              % (cur, tot, time_epoch))
        output_file.write(ans.encode('utf-8'))

    output_file.close()
    input_file.close()
