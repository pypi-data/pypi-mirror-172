#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(file, mode='r', encoding='utf-8'):
	with open(file, mode=mode, encoding=encoding) as f:
		return f.read()

def write(text, file, mode='w', encoding='utf-8'):
	with open(file, mode=mode, encoding=encoding) as f:
		return f.write(text)
