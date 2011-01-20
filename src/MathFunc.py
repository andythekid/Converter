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

def VegetIndex(lMaxMin, rMaxMin):
  """
  Расчет вегетативного индекса.
  Вход: результат функций MaxMin для левого и правого полушарий.
  Выход: ВИ
  """
  # Создаём пустой список разностных функций
  mod = [None for x in xrange(len(lMaxMin))] #@UnusedVariable
  # Для каждого Fi берём разность левого и правого полушария по модулю 
  for i in xrange(len(lMaxMin)):
    mod[i] = abs(lMaxMin[i] - rMaxMin[i])
  # Разбиваем разностный список на 2 равные части, исключая 18 элемент (F4-3)
  # Для каждой половины считаем сумму разностных функций
  S1 = 0
  for i in xrange(17):
    S1 += mod[i]
  S2 = 0
  for i in xrange(18, 35):
    S2 += mod[i]
  # Расчёт вегетативного индекса как отношения сумм разностных функций
  # симпатической и парасимпатической систем.
  VI = S1/(S2 + 0.01)
  return VI
      
