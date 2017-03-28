#!/usr/bin/env python
# -*- coding: utf-8 -*-

def load_pinyin(pinyin_filename, token_filename):
    token_set = set([])
    token_file = open(token_filename, 'r')
    print('[INFO] loading tokens form file \'%s\' ...' % (token_filename))
    for line in token_file:
        str = line.decode(encoding='gb2312')
        for item in str:
            token_set.add(item)
    print('[INFO] successfully loaded %d tokens.' % len(token_set))

    dict = {}

    print('[INFO] loading pinyin from file \'%s\' ...' % (pinyin_filename))
    pinyin_file = open(pinyin_filename, 'r')
    for line in pinyin_file:
        candidate_token = line[:-2].decode(encoding='gb2312').split(' ')
        py = candidate_token[0]
        candidate_token.pop(0)
        tokens = []
        for item in candidate_token:
            if item in token_set:
                tokens.append(item)
            else:
                print('[WARNING] ignore token %s in pinyin file because it is not in the token file' % item)
        dict[py] = tokens
    print('[INFO] successfully loaded %d pinyins.' % len(dict))

    return token_set, dict

def load_language_model(ngram, significance):
    model = []
    significance = int(significance * 100)
    for i in range(ngram):
        igramdict = {}
        filename = 'model/%d-gram_sig_%d.csv' % (i + 1, significance)
        file = open(filename, 'r')
        for line in file:
            str = line.decode('utf-8')
            cont = str[:-1].split(',')
            igramdict[cont[0]] = int(cont[1])
        model = model + [igramdict]
    return model



