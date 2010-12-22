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
    self.probesList = {}
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
  
  def getAllProbes(self):
    """
    Возвращает список всех съемов из списка.
    """
    return self.probesList

  def getCheckedProbes(self, id):
    """
    Возвращает список съемов пациента, сохранённых для обработки
    """
    # Если данный пациент присутствует 
    if self.probesList.has_key(id):
      # Возвращаем его съемы, сохранённые для обработки
      return self.probesList[id]
    else:
      # Иначе возвращаем пустой словарь
      return {}

  def reSetProbes(self, id, probes):
    """
    Переустанавливает список съемов пациента. Вызывать только после
    getCheckedProbes
    """
    # Очищаем съемы пациента
    self.probesList[id] = {}
    # Сохраняем все переданные съемы пациента
    for (date, prim) in probes:
      self.probesList[id][date] = prim

if __name__ == '__main__':
  pass