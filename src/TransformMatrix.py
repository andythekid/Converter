#!/usr/bin/env python
# -*- coding: utf-8 -*-

class ReMatrix:
  """
  Класс, покоящийся здесь, является выродком реверс-инженеринга и крайне
  не рекомендуется к изменению. Вы предупреждены.
  """
  ROWS = 35     # количество строк
  COLUMNS = 24  # количество столбцов
  
  global gSpecialDouble
  
  
  def __init__(self, pervoMatrix):
    pass
  
  def ShuffleMatrix(self, normAmplMatrx):
    pass
  
  def CalcAmplitude(self, pervoMatrix):
    pass
  
  def GetDataFromTable(self, rowIndex, columnIndex):
    FloatTuple = (27.005051, 26.236269, 25.489374, 24.763741, 24.058765, 23.373859, 
    22.70845, 22.061985, 21.433924, 20.823742, 20.23093, 19.654995, 19.095455, 18.551844, 
    18.023708, 17.510609, 17.012115, 16.527815, 16.057299, 15.60018, 15.156073, 14.724608, 
    14.305428, 13.89818)
    gSpecialDouble = FloatTuple[columnIndex] / float(1 << (rowIndex / 5))
    gSpecialDouble = gSpecialDouble - (gSpecialDouble * 0.5) * float(rowIndex % 5) * 0.2
    gSpecialDouble = gSpecialDouble * 163.84
    return long(gSpecialDouble)