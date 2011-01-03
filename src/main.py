#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
# Главное окно
from MainForm import Ui_MainWindow
# Класс доступа к обрабатываемой БД
import DBInterface as db
# Класс хранения списка съемов для обработки
import ExportProbes as pr
from datetime import datetime
import platform
import os

__version__ = "0.0.2b"

class Main(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.ui=Ui_MainWindow()
    self.ui.setupUi(self)
    # Объявляем слоты
    # Выход из программы
    self.ui.actionExit.triggered.connect(self.close)
    # Открыть БД
    self.ui.actionDBOpen.triggered.connect(self.openDB)
    # Закрыть БД
    self.ui.actionDBClose.triggered.connect(self.closeDB)
    # Отобразить съемы пациента
    self.ui.trePatients.itemClicked.connect(self.listProbes)
    # Экспорт
    self.ui.actionExport.triggered.connect(self.exportProbes)
    # Вывести окошко 'О программе'
    self.ui.actAboutShow.triggered.connect(self.helpAbout)
    self.statusBar().showMessage(u'Готов')

  def openDB(self):
    '''
    Открыть БД и отобразить список пациентов
    '''
    # Создаём новый список экспортных пациентов
    self.patLst = pr.ExportProbes()
    # Получаем имя базы
    filename = QtGui.QFileDialog.getOpenFileName(self, u'Выберете файл базы данных', QtCore.QDir.homePath(), u"Базы данных (*.gdb *.GDB)")
    # Борьба с кодировками (TODO вынести в отдельный класс)
    if platform.system() == ('Windows' or 'Microsoft'):
      filename = unicode(filename).encode('cp1251')
    else:
      filename = str(filename)
    # Подключаемся к базе
    global base
    base = db.DBAccess(filename)
    # Получаем список пациентов
    patients = base.getAllPatients()
    # Выводим его 
    for id in patients.keys():
      # Порядок полей: ID, ФИО, дата рождения, пол
      item = QtGui.QTreeWidgetItem( [ str(id), patients[id][0], str(patients[id][1]), patients[id][2] ] )
      item.setCheckState(0,QtCore.Qt.Unchecked)
      self.ui.trePatients.addTopLevelItem(item)
    self.statusBar().showMessage(u'База данных загружена. Найдено '+str(len(patients))+u' пациентов.')
    
  def closeDB(self):
    '''
    Закрыть БД
    '''
    # Очищаем элементы формы
    self.ui.treProbes.clear()
    self.ui.trePatients.clear()
    # Удаляем список экспортных пациентов
    del self.patLst
    self.statusBar().showMessage(u'Готов')
    
  def listProbes(self, patient):
    '''
    Отобразить съемы выбранного пациента
    '''
    #--------------------------------------------------
    # 1 часть: обработка и сохранение старых данных
    #--------------------------------------------------
    
    # В случае, если отображение происходит не первый раз
    id = self.patLst.getID()
    if id != None:
      # создаем временный список чекнутых съемов
      tmpLst = []
      # Сохраняем список чекнутых съемов на экспорт
      for itemN in xrange(self.ui.treProbes.topLevelItemCount()):
        item = self.ui.treProbes.topLevelItem(itemN)
        if item.checkState(0):
          tmpLst.extend([[str(item.text(0)), item.text(1)]])
      # Сохраняем список чекнутых
      self.patLst.reSetProbes(id, tmpLst)
      # Перезагружаем виджет со списком экспорта
      self.refreshExportList()
    
    #--------------------------------------------------
    # 2 часть: вывод новых данных
    #--------------------------------------------------
    
    # Получаем Id текущего пациента из виджета списка пациентов
    id = patient.text(0)
    # Сохранить Id текущего пациента в список экспортных пациентов для
    # последующего формирования элементов списка
    self.patLst.putID(id)
    # Очищаем лист съемов
    self.ui.treProbes.clear()
    # Запрашиваем из базы все съемы пациента с данным Id
    probes = base.getPatientInfo(id)
    # Получаем список съемов, уже присутствующих в списке экспорта
    chkLst = self.patLst.getCheckedProbes(id)
    # Выводим полученные данные в виджет вывода съемов 
    for date in probes.keys():
      item = QtGui.QTreeWidgetItem( [ date.strftime('%Y-%m-%d %H:%M:%S'), probes[date] ] )
      # Если съем присутствует в списке на экспорт
      if chkLst.has_key(date.strftime('%Y-%m-%d %H:%M:%S')):
        # Отмечаем его галочкой
        item.setCheckState(0,QtCore.Qt.Checked)
      else:
        # Иначе снимаем галочку
        item.setCheckState(0,QtCore.Qt.Unchecked)
      self.ui.treProbes.addTopLevelItem(item)
    
  def refreshExportList(self):
    '''
    Перезагрузить список экспортных съемов.
    '''
    # Очищаем виджет экспортных съёмов
    self.ui.treExportProbes.clear()
    # Получаем список съемов, приготовленнных к экспорту
    exportLst = self.patLst.getAllProbes()
    # Выводим экспортные съёмы
    for patient in exportLst.keys():
      for date in exportLst[patient].keys():
        item = QtGui.QTreeWidgetItem([patient, base.getPatientName(patient), date, exportLst[patient][date] ])
        self.ui.treExportProbes.addTopLevelItem(item)

  def exportProbes(self):
    '''
    Экспортирование съемов
    '''
    if platform.system() == ('Windows' or 'Microsoft'):
      dirName = unicode(QtGui.QFileDialog.getExistingDirectory(self, u'Выберете дирректорию сохранения')).encode('cp1251')
    else:
      dirName = str(QtGui.QFileDialog.getExistingDirectory(self, u'Выберете дирректорию сохранения'))
    # Получаем список съемов, приготовленнных к экспорту
    exportLst = self.patLst.getAllProbes()
    for patient in exportLst.keys():
      for date in exportLst[patient].keys():
        #fileName = dirName + base.getPatientName(patient) + '_'+date
        trueDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
        dateStr = trueDate.strftime('%Y-%m-%d-%H-%M-%S')
        if platform.system() == ('Windows' or 'Microsoft'):
          patientName = base.getPatientName(patient).encode('cp1251')
        else:
          patientName = str(base.getPatientName(patient))
        fileName = os.path.join(dirName, patientName + '_' + dateStr + '.txt')
        tmpFile = open(fileName, "w")
        lMatr, rMatr = base.getMatrix(patient, date)
        for i in xrange(35):
          for j in xrange(24):
            tmpFile.write(str(lMatr[i][j]))
            tmpFile.write('; ')
          tmpFile.write('\n')
        for i in xrange(35):
          for j in xrange(24):
            tmpFile.write(str(rMatr[i][j]))
            tmpFile.write('; ')
          tmpFile.write('\n')        
        tmpFile.close()
    self.statusBar().showMessage(u'Экспорт прошёл успешно')

  
  def helpAbout(self):
    '''
    Отобразить окошко About
    '''
    QtGui.QMessageBox.about(self, "About Converter",
                            u"""<b>MEGI Converter</b> v %s
                            <p>Copyright &copy; 2010 Neurocyb.
                            All rights reserved.
                            <p>Приложение для конвертирования БД МЭГИ в
                            открытые форматы.
                            <p>Python %s - Qt %s - PyQt %s on %s
                            """ % (__version__, platform.python_version(),
                            QtCore.QT_VERSION_STR, QtCore.PYQT_VERSION_STR,
                            platform.system() ) 
                            )

def main():
  app = QtGui.QApplication(sys.argv)
  window=Main()
  window.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
