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
    self.processingProbe = None
        
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
  
  def putProcesingProbe(self, probe):
    """
    Сохранить съем из списка экспорта для обработки
    """
    self.processingProbe = probe
  
  def getProcessingProbe(self):
    """
    Извлеч съем из списка экспорта для обработки
    """
    return self.processingProbe
  
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

  def changeProbeStatus(self, id, probe, prim):
    """
    Добавляет/убирает указанный съем в/из списка экспорта
    """
    # Если пациент существует
    if self.probesList.has_key(id):
      # Если существует съём
      if self.probesList[id].has_key(probe):
        # Удаляем съём
        del self.probesList[id][probe]
      # Если съёма не существует
      else:
        # Добавляем съём
        self.probesList[id][probe] = prim
    # Если пациента не существует
    else:
      # Добавляем нового пациента
      self.probesList[id] = {}
      # Добавляем новый съём
      self.probesList[id][probe] = prim

  def reSetProbes(self, id, probes):
    """
    Переустанавливает список съемов пациента. 
    """
    # Очищаем съемы пациента
    self.probesList[id] = {}
    # Сохраняем все переданные съемы пациента
    if probes != None:
      for date in probes.keys():
        self.probesList[id][date] = probes[date]

if __name__ == '__main__':
  pass