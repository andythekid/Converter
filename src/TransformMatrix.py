#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ReMatrix:
  """
  Класс, покоящийся здесь, является выродком реверс-инженеринга и крайне
  не рекомендуется к изменению. Вы предупреждены.
  """
  global ROWS
  global COLUMNS
  global gSpecialDouble
  global DoubleArray
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
    
    # Считаем амплитуды двух матриц
    self.leftMatrix = self.CalcAmplitude(pervoMatrix)
    self.rightMatrix = self.CalcAmplitude(pervoMatrix)
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
    self.rezMatrix = range(ROWS)
    for i in range(ROWS):
      self.rezMatrix[i] = range(COLUMNS)
    # Размещаем значения normAmplMatrx в правильном порядке и заносим в rezMatrix
    for j in range(ROWS, -1, -1):
      for i in range(14, -1, -1):
        pass
      for i in range(COLUMNS, 14, -1):
        pass
    return self.rezMatrix
      
  
  def CalcAmplitude(self, pervoMatrix):
    """
    Расчет значений амплитуд сегментарной матрицы 
    """
    for row in range(ROWS):
      for col in range(COLUMNS):
        DataIndex = self.GetDataFromTable(row, col)
        gSpecialDouble-=DataIndex
        self.Amplitudes[row][col] = (float(pervoMatrix[DataIndex]) * (1.0 - gSpecialDouble) + float(pervoMatrix[DataIndex + 1]) * gSpecialDouble) * 0.001388888888888889   / DoubleArray[row] * (72.0 - col)
    return self.Amplitudes
  
  def GetDataFromTable(self, rowIndex, columnIndex):
    FloatTuple = (27.005051, 26.236269, 25.489374, 24.763741, 24.058765, 23.373859, 
    22.70845, 22.061985, 21.433924, 20.823742, 20.23093, 19.654995, 19.095455, 18.551844, 
    18.023708, 17.510609, 17.012115, 16.527815, 16.057299, 15.60018, 15.156073, 14.724608, 
    14.305428, 13.89818)
    gSpecialDouble = FloatTuple[columnIndex] / float(1 << (rowIndex / 5))
    gSpecialDouble = gSpecialDouble - (gSpecialDouble * 0.5) * float(rowIndex % 5) * 0.2
    gSpecialDouble = gSpecialDouble * 163.84
    return long(gSpecialDouble)
  
  