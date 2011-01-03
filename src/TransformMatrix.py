#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 21.11.2010

@author: Andrey Volkov
@contact: evil.bobby@gmail.com
@attention: Класс, покоящийся здесь, является выродком реверс-инженеринга 
и крайне не рекомендуется к изменению.
"""

class ReMatrix:
  """
  Класс для перевода сырых бинарных данных, считанных из БД МЭГИ в два
  2-х мерных массива, реализованных через 2-х мерные списки, представляющих
  собой сегментарные матрицы левого и правого полушарий головного мозга. 
  """
  
  # Объявление глобальных переменных
  global ROWS
  global COLUMNS
  
  ROWS = 35     # количество строк
  COLUMNS = 24  # количество столбцов
  
  def __init__(self, pervoMatrix):
    """
    Конструктор. Принимает сырой список unsigned short-ов, полученный из поля fft, 
    производит все расчеты.
    """
    # Разбиваем список на 2 части, левую и правую.
    self.leftMatrix = pervoMatrix[:16384]
    self.rightMatrix = pervoMatrix[16384:]
    # Расчет амплитуд двух матриц
    self.leftMatrix = self.CalcAmplitude(self.leftMatrix)
    self.rightMatrix = self.CalcAmplitude(self.rightMatrix)
    # Переставляем значения матриц
    self.leftMatrix = self.ShuffleMatrix(self.leftMatrix)
    self.rightMatrix = self.ShuffleMatrix(self.rightMatrix)
    
  def getSegMatrx(self):
    """
    Возвращает расчитанные матрицы
    """
    return self.leftMatrix, self.rightMatrix
  
  def ShuffleMatrix(self, normAmplMatrx):
    """
    Расстановка значений матрицы в правильном порядке
    """
    # Создаём результирующую матрицу
    self.rezMatrix = [[None for x in xrange(COLUMNS)] for y in xrange(ROWS)] #@UnusedVariable
    # Размещаем значения normAmplMatrx в правильном порядке и заносим в rezMatrix
    for i, m in zip(xrange(ROWS-1,-1,-1), xrange(ROWS)):
      for j, k in zip(xrange(14,-1,-1), xrange(15)):
        self.rezMatrix[m][k] = normAmplMatrx[i][j]
      for j, k in zip(xrange(COLUMNS-1,14,-1), xrange(15, COLUMNS)):
        self.rezMatrix[m][k] = normAmplMatrx[i][j]
    return self.rezMatrix
      
  
  def CalcAmplitude(self, pervoMatrix):
    """
    Расчет значений амплитуд сегментарной матрицы 
    """
    self.gSpecialDouble = 0.0
    # Создаём массив амплитуд  
    Amplitudes = [[None for x in xrange(COLUMNS)] for y in xrange(ROWS)] #@UnusedVariable
    for row in xrange(ROWS):
      for col in xrange(COLUMNS):
        DataIndex = self.GetDataFromTable(row, col)
        self.gSpecialDouble-=DataIndex
        Amplitudes[row][col] = (float(pervoMatrix[DataIndex]) * (1.0 - self.gSpecialDouble) + float(pervoMatrix[DataIndex + 1]) * self.gSpecialDouble) * 0.001388888888888889 * (72.0 - col)
    return Amplitudes
  
  def GetDataFromTable(self, rowIndex, columnIndex):
    """
    Странная функция. Получает из массива сырых unsigned short-ов некое ЧИСЛО.
    Необходима для дальнейшего расчета амплитуд.
    """
    FloatTuple = (27.005051, 26.236269, 25.489374, 24.763741, 24.058765, 23.373859, 
    22.70845, 22.061985, 21.433924, 20.823742, 20.23093, 19.654995, 19.095455, 18.551844, 
    18.023708, 17.510609, 17.012115, 16.527815, 16.057299, 15.60018, 15.156073, 14.724608, 
    14.305428, 13.89818)
    self.gSpecialDouble = FloatTuple[columnIndex] / float(1 << (rowIndex / 5))
    self.gSpecialDouble = self.gSpecialDouble - (self.gSpecialDouble * 0.5) * float(rowIndex % 5) * 0.2
    self.gSpecialDouble = self.gSpecialDouble * 163.84
    return long(self.gSpecialDouble)
  
  