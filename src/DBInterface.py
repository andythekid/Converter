#!/usr/bin/env python
# -*- coding: utf-8 -*-
import kinterbasdb as k #@UnresolvedImport
from datetime import datetime
import struct
import cStringIO

class DBAccess:
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
      self.patDict[id] = [fio.decode('cp1251'), daterojd, sex]
    return self.patDict
  
  def getPatientInfo(self, id):
    """
    Принимает ID пациента, возвращает массив съемов пациента с заданным ID
    """
    SELECT = r"SELECT dates, prim FROM data WHERE id = '" + str(id) + r"'"
    self.curs.execute(SELECT)
    self.probesDict = {}
    for (dates, prim) in self.curs:
      self.probesDict[dates] = prim
    return self.probesDict
    
  def getPervoMatrix(self, id, probe):
    """
    принимает ид пациента и съема, возвращает перво-матрицу съема.
    !!!ВНИМАНИЕ!!! Эта матрица форматированна своим хитроВЫЕБАННЫМ способом, и использовать ее
    в чистом виде нельзя. 
    """
    dateId = datetime.strptime(probe, '%Y-%m-%d %H:%M:%S')
    dateStr = dateId.strftime('%d.%m.%Y, %H:%M:%S.000')
    SELECT = r"SELECT fft FROM data WHERE id = '" + str(id) + r"' AND dates = '" + dateStr + r"'"
    self.curs.execute(SELECT)
    fft = self.curs.fetchone()
    #self.fft = struct.unpack('d', fft)
    file = cStringIO.StringIO(fft[0])
    # TODO Разобраться с передачей параметров в ReMatrix
    a = set()
    while 1:
      buff = file.read(8)
      if not buff:
        break
      ff = struct.unpack('d', buff)
      a.add(ff)
    print len(a)
    
    