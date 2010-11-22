#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ReMatrix:
  """
  Класс, покоящийся здесь, является выродком реверс-инженеринга и крайне
  не рекомендуется к изменению. Вы предупреждены.
  """
  global ROWS
  global COLUMNS
#  global gSpecialDouble
#  global Amplitudes
  
  ROWS = 35     # количество строк
  COLUMNS = 24  # количество столбцов
  
  
  def __init__(self, pervoMatrix):
    """
    Конструктор - единственная используемая извне функция. Принимает сырой
    список, полученный из поля fft, возвращает две правильные сегментарные 
    матрицы.
    """
    # Разбиваем список на 2 части, левую и правую.
    self.leftMatrix = pervoMatrix[:840]
    self.rightMatrix = pervoMatrix[840:]
    # Создаём массив амплитуд  
    self.Amplitudes = [[None for x in xrange(ROWS)] for y in xrange(COLUMNS)] #@UnusedVariable
    # Расчет амплитуд двух матриц
    self.leftMatrix = self.CalcAmplitude(self.leftMatrix)
    self.rightMatrix = self.CalcAmplitude(self.rightMatrix)
    # Переставляем значения матриц
    self.leftMatrix = self.ShuffleMatrix(self.leftMatrix)
    self.rightMatrix = self.ShuffleMatrix(self.rightMatrix)
    # Возвращаем правильные матрицы
    return self.leftMatrix, self.rightMatrix
  
  def ShuffleMatrix(self, normAmplMatrx):
    """
    Расстановка значений матрицы в правильном порядке
    """
    # Создаём результирующую матрицу
    self.rezMatrix = [[None for x in xrange(ROWS)] for y in xrange(COLUMNS)] #@UnusedVariable
    # Размещаем значения normAmplMatrx в правильном порядке и заносим в rezMatrix
    for j, k in zip(xrange(ROWS-1,-1,-1), xrange(ROWS)):
      for i, m in zip(xrange(14,-1,-1), xrange(14)):
#        self.rezMatrix[m][k] = normAmplMatrx[i][j]
        print normAmplMatrx[i][j],
      for i, m in zip(xrange(COLUMNS-1,13,-1), xrange(14, COLUMNS)):
#        self.rezMatrix[m][k] = normAmplMatrx[i][j]
        print normAmplMatrx[i][j],
      print
#    return self.rezMatrix
      
  
  def CalcAmplitude(self, pervoMatrix):
    """
    Расчет значений амплитуд сегментарной матрицы 
    """
    self.gSpecialDouble = 0.0
    for row in xrange(ROWS):
      for col in xrange(COLUMNS):
        DataIndex = self.GetDataFromTable(row, col)
        self.gSpecialDouble-=DataIndex
        self.Amplitudes[row][col] = (float(pervoMatrix[DataIndex]) * (1.0 - self.gSpecialDouble) + float(pervoMatrix[DataIndex + 1]) * self.gSpecialDouble) * 0.001388888888888889 * (72.0 - col)
    return self.Amplitudes
  
  def GetDataFromTable(self, rowIndex, columnIndex):
    FloatTuple = (27.005051, 26.236269, 25.489374, 24.763741, 24.058765, 23.373859, 
    22.70845, 22.061985, 21.433924, 20.823742, 20.23093, 19.654995, 19.095455, 18.551844, 
    18.023708, 17.510609, 17.012115, 16.527815, 16.057299, 15.60018, 15.156073, 14.724608, 
    14.305428, 13.89818)
    self.gSpecialDouble = FloatTuple[columnIndex] / float(1 << (rowIndex / 5))
    self.gSpecialDouble = self.gSpecialDouble - (self.gSpecialDouble * 0.5) * float(rowIndex % 5) * 0.2
    self.gSpecialDouble = self.gSpecialDouble * 163.84
    return long(self.gSpecialDouble)
  
  