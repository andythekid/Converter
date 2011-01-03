#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

'''
Created on 03.01.2011

@author: Andrey Volkov
@contact: evil.bobby@gmail.com
'''

def convert(string):
  '''
  Преобразует переданную unicode-подобную строку в кодироку, используемую 
  в текущей файловой системе.
  '''
  # Получаем кодировку используемой файловой системы
  sysEnc = sys.getfilesystemencoding()
  # Возвращаем строку в системной кодировке
  return unicode(string).encode(sysEnc)
        