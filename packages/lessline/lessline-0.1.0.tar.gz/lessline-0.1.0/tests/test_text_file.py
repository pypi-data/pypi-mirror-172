#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from lessline.text_file import read, write


def test_read():
    file = './tests/data/text_file/read.txt'
    text_orig = 'Hello word!\nThis is lessline!'
    text = read(file)
    assert text_orig == text


def test_write_with_file_not_exists():
    file = './tests/data/text_file/write_with_file_not_exists.txt'
    text_orig = 'Hello word!\nThis is lessline!'
    if os.path.exists(file):
        os.remove(file)
        print('File removed:', file)
    write(text_orig, file)
    with open(file) as f:
        text = f.read()
    assert text_orig == text


def test_write_with_file_existed():
    file = './tests/data/text_file/write_with_file_existed.txt'
    text_orig = 'Hello word!\nThis is lessline!'
    with open(file, mode='w') as f:
        f.write('hello')
    if os.path.exists(file):
        print('File existed:', file)
    write(text_orig, file)
    with open(file) as f:
        text = f.read()
    assert text_orig == text
