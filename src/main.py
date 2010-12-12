#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
from MainForm import Ui_MainWindow
import DBInterface as db
import ExportProbes as pr
import platform

__version__ = "0.0.1b"

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
    # Вывести окошко 'О программе'
    self.ui.actAboutShow.triggered.connect(self.helpAbout)
    self.statusBar().showMessage(u'Готов')

  def openDB(self):
    '''
    Открыть БД и отобразить список пациентов
    '''
    # Создаём новый список экспортных пациентов
    global patLst
    patLst = pr.ExportProbes()
    # Получаем имя базы
    filename = QtGui.QFileDialog.getOpenFileName(self, u'Выберете файл базы данных', QtCore.QDir.homePath(), u"Базы данных (*.gdb *.GDB)")
    # Подключаемся к базе
    global base
    base = db.DBAccess(str(filename))
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
    self.statusBar().showMessage(u'Готов')
    
  def listProbes(self, item):
    '''
    Отобразить съемы выбранного пациента
    '''
    # В случае, если отображение происходит не первый раз
    if patLst.getID() != None:
      pass
    # Получаем Id текущего пациента
    id = item.text(0)
    # Сохранить Id текущего пациента в список экспортных пациентов для
    # последующего формирования элементов списка
    patLst.putID(id)
    # Запрашиваем из базы все съемы пациента с данным Id
    probes = base.getPatientInfo(id)
    # Очищаем лист съемов
    self.ui.treProbes.clear()
    # Выводим полученные съемы 
    for dates in probes.keys():
      item = QtGui.QTreeWidgetItem( [ str(dates), probes[dates] ] )
      item.setCheckState(0,QtCore.Qt.Unchecked)
      self.ui.treProbes.addTopLevelItem(item)

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
