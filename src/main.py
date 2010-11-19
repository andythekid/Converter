#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from MainForm import Ui_MainWindow
import DBInterface as db

class Main(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.ui=Ui_MainWindow()
    self.ui.setupUi(self)
    self.statusBar().showMessage(u'Готов')
    self.ui.actionExit.triggered.connect(self.close)
    self.ui.actionDBOpen.triggered.connect(self.openDB)
    self.ui.trePatients.itemClicked.connect(self.clickedItem)

  def openDB(self):
    '''
    Открыть БД и отобразить список пациентов
    '''
    # Получаем имя базы
    filename = QtGui.QFileDialog.getOpenFileName(self, u'Выберете файл базы данных', QtCore.QDir.homePath(), u"Базы данных (*.gdb *.GDB)")
    # Подключаемся к базе
    global base
    base = db.DBAccess(str(filename))
    # Получаем список пациентов
    patients = base.getAllPatients()
    # Выводим его 
    for id in patients.keys():
      item = QtGui.QTreeWidgetItem( [ str(id), patients[id][0], str(patients[id][1]), str(patients[id][2]) ] )
      item.setCheckState(0,QtCore.Qt.Unchecked)
      self.ui.trePatients.addTopLevelItem(item)
    self.statusBar().showMessage(u'База данных загружена. Найдено '+str(len(patients))+u' пациентов.')
    
  def clickedItem(self, item):
    # Получаем Id текущего пациента
    id = item.text(0)
    # Запрашиваем из базы все съемы пациента с данным Id
    probes = base.getPatientInfo(id)
    # Очищаем лист съемов
    self.ui.treProbes.clear()
    # Выводим полученные съемы 
    for dates in probes.keys():
      item = QtGui.QTreeWidgetItem( [ str(dates), probes[dates][0] ] )
      item.setCheckState(0,QtCore.Qt.Unchecked)
      self.ui.treProbes.addTopLevelItem(item)


def main():
  app = QtGui.QApplication(sys.argv)
  window=Main()
  window.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
