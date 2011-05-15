#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 20.01.2011

@author: Andrey Volkov
@contact: evil.bobby@gmail.com
"""

ROWS = 35     # количество строк
COLUMNS = 24  # количество столбцов

segments = ['C1', 'C2-3', 'C4-5', 'C6', 'C7-8',
            'Th1', 'Th2', 'Th3-4', 'Th5', 'Th6',
            'Th7', 'Th8-9', 'Th10', 'Th11', 'Th12',
            'L1', 'L2', 'L3', 'L4', 'L5',
            'S1', 'S2', 'S3-4', 'K-S5']

def pearson (x, y):
  """
  Вычисление коэффициентов корреляции по Пирсону
  """
  n = len(x)
  vals = range(n)
  # Простые суммы
  sumx = sum ([float(x[i]) for i in vals])
  sumy = sum ([float(y[i]) for i in vals])
  # Суммы квадратов
  sumxSq = sum ([x[i] ** 2.0 for i in vals])
  sumySq = sum ([y[i] ** 2.0 for i in vals])
  # Сумма произведений 
  pSum = sum ([x[i] * y[i] for i in vals])
  # Вычисляем коэффициент корреляции Пирсона 
  num = pSum - (sumx * sumy / n)
  den = ((sumxSq - pow (sumx, 2) / n) * (sumySq - pow (sumy, 2) / n)) ** .5
  if den == 0: return 0
  r = num / den
  return r

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

def CorrelationSegI(lMatr, rMatr):
  """
  Расчёт корреляции левой и правой веток функций по сегментам
  """
  # Создаём результирующую матрицу
  rezMatrix = [None for x in xrange(ROWS)] #@UnusedVariable
  # Расчитываем коэффициенты корреляции по сегментам
  for func in xrange(ROWS):
    rezMatrix[func] = pearson(lMatr[func], rMatr[func])
  # Переворачиваем список, чтобы он начинался с F1-1
  rezMatrix.reverse()
  return rezMatrix


def Segment(Matrix):
  """
  Получение значений сегментов
  """

  # Объявляем пустой словарь результирующих элементов
  rezult = {}
  # Проходим по сегментам
  for s in xrange(len(segments)):
    tmp = []
    # Каждое значение функции сегмента
    for i in xrange(0, 35):
      # Добавляем во временный массив
      tmp.append(Matrix[i][s])
    tmp.reverse()
    # Присваиваем ключу с названием сегмента временный массив
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
  VI = S1 / (S2 + 0.01)
  return VI

def StressIndex(lMatr, rMatr):
  """
  Расчёт Индекса Напряжения
  """
  # Создаём словарь вида
  # 'Имя функции': [номер функции, вес]
  funcs = {
           'F3-1':[ 10, 0.5],
           'F3-2':[ 11, 0.8],
           'F3-3':[ 12, 1.0],
           'F3-4':[ 13, 1.3],
           'F3-5':[ 14, 1.6],
           'F4-1':[ 15, 1.8],
           'F4-2':[ 16, 2.0]
           }
  # Расчитываем MaxMin для каждого полушария
  lMaxMin = MaxMin(lMatr)
  rMaxMin = MaxMin(rMatr)
  # Расчитываем корреляцию
  corr = CorrelationSegI(lMatr, rMatr)
  # Расчёт ИН
  summ = 0
  for key in funcs.keys():
    c = corr[funcs[key][0]]
    m = lMaxMin[funcs[key][0]]
    Pi = funcs[key][1]
    summ = summ + c * m * Pi
  SI = summ / 7.0
  if SI < 0: SI = SI + 0.2
  return SI

