#!/usr/bin/env python
# -*- coding: utf-8 -*-

def build_language_model(fileList):
    symbol_file = open('config/symbol.txt')
    symbol_set = (symbol_file.read().decode(encoding='utf-8').split(' '))

    for filename in fileList:
        file = open(filename, 'r')

        tot = 0
        for line in file.readlines():
            out = ''
            tot = tot + 1
            str = line.decode(encoding='utf-8')
            for i in range(len(str)):
                item = str[i]
                try:
                    t = ord(item)
                    if (ord(item) > 256) and (item not in symbol_set):
                        out = out + item
                except:
                    print('[ERROR] Can\'t find code for char %s\n' % item)
            print(out)
            if tot > 1000:
                break
 
def astar(tokens):
    return None