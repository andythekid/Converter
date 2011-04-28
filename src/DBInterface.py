#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Created on 19.11.2010

@author: Andrey Volkov
@contact: evil.bobby@gmail.com
"""

# Извлечение чистых данных сегментарной матрицы
import TransformMatrix as tm
import kinterbasdb as k #@UnresolvedImport
from datetime import datetime
import array

class DBAccess:
  """
  Класс - обертка для удобного доступа к БД посредством kinterbasedb
  """
  
  def __init__(self, DBFileName):
    """
    Конструктор. Принимает в качестве аргумента имя файла базы данных
    и устанавливает с ней соединение 
    """ 
    self.con = k.connect(
      host=None, database=DBFileName,
      user='sysdba', password='masterkey',
      dialect=3, charset='WIN1251'
    )
    customTPB = ( k.isc_tpb_shared )
    # Explicitly start a transaction with the custom TPB:
    self.con.begin(tpb=customTPB)
    self.curs = self.con.cursor()

  def searchPatient(self, patientName):
    """
    Производит поиск пациента с обозначенными параметрами и возвращает список
    id найденных пациентов
    """
    SELECT = r"SELECT id, fio, sex FROM card WHERE lower(fio) LIKE '%" + self.strUtfToCp(patientName.lower()) + r"%'"
    self.curs.execute(SELECT)
    for (id, fio, sex) in self.curs:
      print '%s     %s      %s.' % (id, self.strCpToUtf(fio), sex)
      
  def getAllPatients(self):
    """
    Возвращает массив всех пациентов базы 
    """
    # Делаем выборку всех записей из таблицы CARD
    SELECT = r"SELECT id, fio, daterojd, sex FROM card"
    self.curs.execute(SELECT)
    # Создаем пустой словарь
    self.patDict = {}
    # Заносим в словарь извлеченные данные. ID пациента - ключ
    for (id, fio, daterojd, sex) in self.curs:
      if sex == 0:
        strSex = u'М'
      else:
        strSex = u'Ж'
      self.patDict[id] = [fio.decode('cp1251'), daterojd, strSex]
    return self.patDict
  
  def getPatientName(self, id):
    """
    Возвращает ФИО пациента по id
    """
    SELECT = r"SELECT fio FROM card WHERE id = '" + str(id) + r"'"
    self.curs.execute(SELECT)
    fio = self.curs.fetchone()
    return fio[0].decode('cp1251')
    
  
  def getPatientInfo(self, id):
    """
    Принимает ID пациента, возвращает массив съемов пациента с заданным ID
    """
    SELECT = r"SELECT dates, prim FROM data WHERE id = '" + str(id) + r"'"
    self.curs.execute(SELECT)
    self.probesDict = {}
    for (dates, prim) in self.curs:
      if prim == None:
        self.probesDict[dates.strftime('%Y-%m-%d %H:%M:%S')] = " "
      else:
        self.probesDict[dates.strftime('%Y-%m-%d %H:%M:%S')] = prim.decode('cp1251')
    return self.probesDict
    
  def getPatientInfoDate(self, id):
    """
    Принимает ID пациента, возвращает массив съемов пациента с заданным ID, разбитый по дате
    """
    SELECT = r"SELECT dates, prim FROM data WHERE id = '" + str(id) + r"'"
    self.curs.execute(SELECT)
    self.probesDict = {}
    for (dates, prim) in self.curs:
      # Если не существует подсловаря с нужной датой 
      if not self.probesDict.has_key(dates.strftime('%Y-%m-%d')):
        # Создаём его
        self.probesDict[dates.strftime('%Y-%m-%d')] = {}
      if prim == None:
        self.probesDict[dates.strftime('%Y-%m-%d')][dates.strftime('%Y-%m-%d %H:%M:%S')] = " "
      else:
        self.probesDict[dates.strftime('%Y-%m-%d')][dates.strftime('%Y-%m-%d %H:%M:%S')] = prim.decode('cp1251')
    return self.probesDict
    
  def getMatrix(self, id, probe):
    """
    Принимает ид пациента и съема, возвращает матрицы левого и правого полушарий.
 
    """
    # Преобразуем переданную строку даты в дату
    dateId = datetime.strptime(probe, '%Y-%m-%d %H:%M:%S')
    # Переформатрируем дату в формат, воспринимаемый БД
    dateStr = dateId.strftime('%d.%m.%Y, %H:%M:%S.000')
    # Производим запрос к БД
    SELECT = r"SELECT fft FROM data WHERE id = '" + str(id) + r"' AND dates = '" + dateStr + r"'"
    self.curs.execute(SELECT)
    # Получаем тьюпл, содержащий хекс матрицы в 0-м элементе
    fft = self.curs.fetchone()
    # Преобразуем хекс в список unsigned short
    ff = array.array('H')
    ff.fromstring(str(fft[0]))
    # Получаем готовые матрицы
    matrix = tm.ReMatrix(ff.tolist())
    leftMatrix, rightMatrix = matrix.getSegMatrx()
    return leftMatrix, rightMatrix
