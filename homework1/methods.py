#!/usr/bin/env python
# -*- coding: utf-8 -*-

import math

def frequency_count(dict, max_count = 100):
    count = [0] * (max_count + 1)
    for key in dict:
        if dict[key] <= max_count:
            count[dict[key]] = count[dict[key]] + 1
    print('============================================================\n' +
          '---- [MESSAGE] frequency_count (<=100), totally %d: ' % len(dict))
    sum = 0
    for i in range(101):
        sum = sum + count[i]
        print('-------- Value %d, count %d, totally %d(till)' % (i, count[i], sum))
    print('============================================================\n')


def model_prone(dict, max_count=100, significance=0.95):
    print('---- [INFO] Model Prone Starting...')
    count = [0] * (max_count + 1)
    for key in dict:
        if dict[key] <= max_count:
            count[dict[key]] += 1
    reject = max_count
    total = 0
    for key in dict:
        total = total + dict[key]
    reserve = total
    for i in range(max_count + 1):
        reserve -= count[i] * i
        if (reserve + 0.0) / total < significance:
            reject = i - 1
            reserve += count[i] * i
            break
    print('---- [INFO] We reject pattern whose count <= %d' % reject)
    model = {}
    for key in dict:
        if dict[key] > reject:
            model[key] = dict[key]
    print('---- [INFO] Model Prone Finished')
    return model


def save_model(model, filename):
    print('---- [INFO] Saving the proned model...')
    outfile = open(filename, 'w')
    for key in model:
        outfile.write('%s,%d\n' % (key.encode('utf-8'), model[key]))
    print('---- [INFO] Model successfully saved')


def build_language_model(token_set, fileList, ngram=2, max_count=100, significance=1.01):
    symbol_file = open('config/symbol.txt')
    symbol_set = (symbol_file.read().decode(encoding='utf-8').split(' '))

    gram_dict = {}

    for filename in fileList:
        file = open(filename, 'r')

        cnt_pages = 0
        print('\n[INFO] (build_language_model) Starting handling file %s' % filename)
        for line in file.readlines():
            out = ''
            str = line.decode(encoding='utf-8')
            for i in range(len(str)):
                item = str[i]
                try:
                    t = ord(item)
                except:
                    print('[ERROR] Can\'t find code for char %s' % item)
                if (ord(item) > 256) and (item in token_set):
                    out = out + item

                    # add to n-gram frequency model
                    if len(out) > ngram:
                        strgram = out[-ngram:]
                        if strgram in gram_dict:
                            gram_dict[strgram] = gram_dict[strgram] + 1
                        else:
                            gram_dict[strgram] = 1
                else:
                    out = ''
            cnt_pages += 1
            if cnt_pages % 1000 == 0:
                print('[INFO] (build_language_model) File %s process: Already %d articles' % (filename, cnt_pages))
        print('[INFO] (build_language_model) File %s solved, totally %d articles. %d %d-gram' % \
                (filename, cnt_pages, len(gram_dict), ngram))

    frequency_count(gram_dict, max_count)
    model = model_prone(gram_dict, max_count, significance)
    save_model(model, 'model/%d-gram_sig_%d.csv' % (ngram, int(significance * 100)))


def check_log(x, y):
    if y == 0:
        raise ValueError('Invalid probibility value')
    if x == 0:
        return -1e9
    # print(y, x)
    return math.log((y + 0.0) / x)


def local_log_prob(text, model, ngram):
    if len(text) < ngram:
        ngram = len(text)
    text = text[-ngram:]
    # print(text)
    if (ngram == 1):
        return check_log(model[ngram - 1][text], 1)
    if text in model[ngram - 1]:
        return check_log(model[ngram - 2][text[:-1]], model[ngram - 1][text])
    else:
        return -1e9


def calc_log_prob(text, model, ngram):
    log_prob = 0
    for i in range(len(text)):
        log_prob += local_log_prob(text[:i+1], model, ngram)
    return log_prob


def astar_pinyin(pinyin, pydict, model, ngram=2, iters=1000000):
    head = 0
    queue = ['']
    open_set = set([''])
    state_value = {'': 0}

    for key in pydict:
        def cmp1(x, y):
            try:
                a = model[0][x]
            except:
                a = 0
            try:
                b = model[0][y]
            except:
                b = 0
            if a < b:
                return -1
            if a == b:
                return 0
            if a > b:
                return 1
        pylist = pydict[key]
        sortedlist = sorted(pylist, cmp=cmp1)
        pydict[key] = []
        for item in reversed(sortedlist):
            if item in model[0]:
                pydict[key] += [item]

    ans_text = ''
    ans_log_prob = -1e9
    itr = 0
    while itr < iters and head < len(queue):
        cur_text = queue[head]
        head += 1
        # print(cur_text)
        cur_log_prob = state_value[cur_text]
        if len(cur_text) == len(pinyin):
            if cur_log_prob > ans_log_prob:
                ans_log_prob = cur_log_prob
                ans_text = cur_text
        open_set.remove(cur_text)
        if ans_log_prob >= cur_log_prob or len(cur_text) == len(pinyin):
            continue
        idx = len(cur_text)
        for token in pydict[pinyin[idx]]:
            x_text = cur_text + token
            x_log_prob = local_log_prob(x_text, model, ngram) + cur_log_prob
            in_state = x_text in state_value
            in_open_set = x_text in open_set
            if (not in_state) and (not in_open_set):
                open_set.add(x_text)
                queue += [x_text]
                state_value[x_text] = x_log_prob
            if in_state:
                if x_log_prob > state_value[x_text]:
                    state_value[x_text] = x_log_prob
                    if not in_open_set:
                        queue += [x_text]
                        open_set.add(x_text)


    return ans_text, ans_log_prob

