#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 20.01.2011

@author: Andrey Volkov
@contact: evil.bobby@gmail.com
"""

def MaxMin(segMatrx):
  """
  Функция вычисления аналога "динамического диапазона".
  Вычисляет разницу между максимальным и минимальным значениями
  каждой строчки матрицы.
  Возвращает одномерный массив полученных разниц.
  """
  # Создаём результирующую матрицу
  rezMatrix = [None for x in xrange(len(segMatrx))] #@UnusedVariable
  for func in xrange(len(segMatrx)):
    # Присваиваем минимуму и максимуму начальные значения
    min = segMatrx[func][0]
    max = segMatrx[func][0]
    # Находим минимум и максимум для строки
    for ampl in xrange(len(segMatrx[func])):
      if max < segMatrx[func][ampl]:
        max = segMatrx[func][ampl]
      if min > segMatrx[func][ampl]:
        min = segMatrx[func][ampl]
    # Заносим разницу max-min в результирующую матрицу
    rezMatrix[func] = max - min
  # Возвращаем результат
  return rezMatrix
    