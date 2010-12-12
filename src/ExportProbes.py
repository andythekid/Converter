#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 12.12.2010

@author: Andrey Volkov
@contact: evil.bobby@gmail.com
"""

class ExportProbes:
  """
  Класс используется для хранения списка съемов, предназначенных для 
  экспорта и иной обработки.
  """

  def __init__(self):
    """
    Конструктор. Инициализирует пустой список.
    """
    self.probesList = []
    self.patientID = None
        
  def putID(self, id):
    """
    Сохраняет ID текущего обрабатываемого пациента.
    """
    self.patientID = id
    
  def getID(self):
    """
    Возвращает ID текущего обрабатываемого пациента.
    """
    return self.patientID
  
  def addProbes(self, probe):
    """
    Добавляет переданный съем в список.
    """
    pass
    
  def getProbes(self):
    """
    Возвращает список всех съемов из списка.
    """
    return self.probesList
    
  def delProbes(self, probe):
    """
    Удаляет переданный съем из списка.
    """
    pass
        
if __name__ == '__main__':
  pass