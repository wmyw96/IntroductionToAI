#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import os
import time
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
                + '/source')
from methods import astar_pinyin, build_language_model, calc_log_prob
from utils import load_pinyin, load_language_model
import re

MODEL = True

if __name__ == '__main__':
    abs_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
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

    checkAns = False
    if len(sys.argv) >= 4:
        checkAns = True
        ans_file_name = sys.argv[3]
        ans_file = open(ans_file_name, 'r')
        ans_str = []
        for line in ans_file:
            ans_str.append(line[:-1].decode('utf-8'))

    input_file = open(input_file_name, 'r')
    output_file = open(output_file_name, 'w')

    token_set, pydict = load_pinyin(abs_path + '/data/pinyin.txt',
                                    abs_path + '/data/tokens.txt')

    if not MODEL:
        file_list = ['/corpus/2016-01.txt', '/corpus/2016-02.txt',
                     '/corpus/2016-03.txt', '/corpus/2016-04.txt',
                     '/corpus/2016-05.txt', '/corpus/2016-06.txt',
                     '/corpus/2016-07.txt', '/corpus/2016-08.txt',
                     '/corpus/2016-09.txt', '/corpus/2016-10.txt',
                     '/corpus/2016-11.txt']
        filenames = []
        for filename in file_list:
            filenames.append(abs_path + filename)
        build_language_model(token_set, filenames,
                             ngram=4, significance=0.95)

    model = load_language_model(abs_path, ngram=3, significance=0.95)

    pattern = re.compile(r'[a-z]+')

    tot = 0
    for line in input_file:
        tot = tot + 1
    input_file.close()
    input_file = open(input_file_name, 'r')
    cur = 0

    tot_len = 0.0
    tot_cor = 0.0

    for line in input_file:
        tokens = re.findall(pattern, line)
        time_epoch = -time.time()
        ans, log_prob = astar_pinyin(tokens, pydict, model, ngram=3)
        time_epoch += time.time()
        cur = cur + 1
        print('[INFO] Searching..., solved %d out of %d, using time %.3f s'
              % (cur, tot, time_epoch))
        output_file.write(ans.encode('utf-8'))
        output_file.write('\n')

        if checkAns:
            cur_len = 0.0
            cur_cor = 0.0
            print(ans_str[cur - 1])
            print(ans)
            for i in range(len(ans_str[cur - 1])):
                cur_len += 1.0
                if i >= len(ans):
                    continue
                if ans_str[cur - 1][i] == ans[i]:
                    cur_cor += 1.0
            tot_len += cur_len
            tot_cor += cur_cor
            print('Test #%d: accuracy %.2f, all accuracy %.2f'
                  % (cur, cur_cor / cur_len, tot_cor / tot_len))

    if checkAns:
        print('Total accuracy %.2f' % (tot_cor / tot_len))

    output_file.close()
    input_file.close()
