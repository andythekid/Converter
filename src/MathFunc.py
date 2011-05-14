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
  # Переворачиваем список, чтобы он начинался с F1-1
  rezMatrix.reverse()
  # Возвращаем результат
  return rezMatrix

def Segment(Matrix):
  """
  Получение значений сегментов
  """
  segments = ['C1', 'C2-3', 'C4-5', 'C6', 'C7-8',
              'Th1','Th2', 'Th3-4', 'Th5', 'Th6',
              'Th7', 'Th8-9', 'Th10', 'Th11', 'Th12',
              'L1', 'L2', 'L3', 'L4', 'L5',
              'S1', 'S2', 'S3-4', 'K-S5']
  # Объявляем пустой словарь результирующих элементов
  rezult = {}
  for s in xrange(len(segments)):
    tmp = []
    for i in xrange(0, 35):
      tmp.append(Matrix[i][s])
    tmp.reverse()
    rezult[segments[s]] = tmp
  return rezult

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

