#!/usr/bin/env python
# -*- coding: utf-8 -*-

def read(file, encoding='utf-8'):
	with open(file, encoding=encoding) as f:
		return f.read()
