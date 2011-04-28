#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt #@UnresolvedImport
# Главное окно
from MainForm import Ui_MainWindow
# Класс доступа к обрабатываемой БД
import DBInterface as db
# Класс хранения списка съемов для обработки
import ExportProbes as pr
import MathFunc
from datetime import datetime
# Платформозависимые функции-обёртки
import PlatformUtils as pu
import platform
import os

__version__ = "0.1.4"

class Main(QtGui.QMainWindow):
  def __init__(self):
    QtGui.QMainWindow.__init__(self)
    self.ui = Ui_MainWindow()
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
    # Чекнуть пациента
    # Внимание!!! - Не очевидно.
    # Во в момент срабатывания itemChanged так же срабатывает
    # и itemClicked, однако itemChanged всегда отрабатывает
    # раньше
    self.ui.trePatients.itemChanged.connect(self.selectAllPatientProbes)
    # Чекнуть единичный съем пациента
    self.ui.treProbes.itemChanged.connect(self.selectProbe)
    # Выбрать всех
    self.ui.actSelectAll.triggered.connect(self.selectAllProbes)
    # Экспорт
    self.ui.actionExport.triggered.connect(self.exportProbes)
    # Вывести окошко 'О программе'
    self.ui.actAboutShow.triggered.connect(self.helpAbout)
    # Щелчёк по съему в окне экспорта
    self.ui.treExportProbes.itemClicked.connect(self.selectExportPatient)
    # Помечаем съем в окне экспорта
    self.ui.treExportProbes.itemChanged.connect(self.markExportPatient)
    # Кнопка "Очистить" в окне экспорта
    self.ui.btnClearProbes.clicked.connect(self.clearExport)
    # Кнопка сохранения изображения графика
    self.ui.butSaveImage.clicked.connect(self.saveImage)
    # Кнопка экспорта данных графика
    self.ui.butGarphExport.clicked.connect(self.exportGarph)
    # Построение графика MaxMin
    self.ui.actMaxMin.triggered.connect(self.plotMaxMin)
    # Постоение графика вегетативного индекса
    self.ui.actVI.triggered.connect(self.plotVegetIndex)
    # Разворачиваем на весь экран
    self.showMaximized()
    self.statusBar().showMessage(u'Готов')

  def openDB(self):
    '''
    Открыть БД и отобразить список пациентов
    '''
    # Подчищаем старые данные
    self.closeDB()
    # Создаём новый список экспортных пациентов
    self.patLst = pr.ExportProbes()
    # Получаем имя базы в системной кодировке
    filename = pu.convert(QtGui.QFileDialog.getOpenFileName(self,
                                                            u'Выберете файл базы данных',
                                                            QtCore.QDir.homePath(),
                                                            u"Базы данных (*.gdb *.GDB)"))
    if filename != '':
      # Подключаемся к базе
      global base
      try:
        base = db.DBAccess(filename)
        # Получаем список пациентов
        patients = base.getAllPatients()
        # Выводим его
        for id in patients.keys():
          # Порядок полей: ID, ФИО, дата рождения, пол
          item = QtGui.QTreeWidgetItem([ str(id), patients[id][0], str(patients[id][1]), patients[id][2] ])
          item.setCheckState(0, QtCore.Qt.Unchecked)
          self.ui.trePatients.addTopLevelItem(item)
        self.statusBar().showMessage(u'База данных загружена. Найдено ' + str(len(patients)) + u' пациентов.')
      except UnicodeDecodeError:
        self.statusBar().showMessage(u'Ошибка: слишком длинный путь до базы данных.')

  def closeDB(self):
    '''
    Закрыть БД
    '''
    # Очищаем элементы формы
    self.ui.treProbes.clear()
    self.ui.trePatients.clear()
    self.ui.treExportProbes.clear()
    # Очищаем список экспортных пациентов
    self.patLst = None
    self.statusBar().showMessage(u'База данных закрыта')

  def listProbes(self, patient):
    '''
    Отобразить съемы выбранного пациента
    '''
    # Получаем Id текущего пациента из виджета списка пациентов
    id = patient.text(0)
    # Сохранить Id текущего пациента в список экспортных пациентов для
    # последующего формирования элементов списка
    self.patLst.putID(id)
    # Очищаем лист съемов
    self.ui.treProbes.clear()
    # Запрашиваем из базы все съемы пациента с данным Id
    probes = base.getPatientInfoDate(id)
    # Получаем список съемов, уже присутствующих в списке экспорта
    chkLst = self.patLst.getCheckedProbes(id)
    # Выводим полученные данные в виджет вывода съемов
    for date in probes.keys():
      item = QtGui.QTreeWidgetItem([ date, str(len(probes[date])) ])
      childNum = 0
      allDateCheck = True
      for probe in probes[date].keys():
        item.addChild(QtGui.QTreeWidgetItem([ probe, probes[date][probe] ]))
        # Если съем присутствует в списке на экспорт
        if chkLst.has_key(probe):
          # Отмечаем его галочкой
          item.child(childNum).setCheckState(0, QtCore.Qt.Checked)
        else:
          # Иначе снимаем галочку
          item.child(childNum).setCheckState(0, QtCore.Qt.Unchecked)
          # И отмечаем всю дату как не выбранную
          allDateCheck = False
        childNum += 1
      self.ui.treProbes.addTopLevelItem(item)
      if allDateCheck:
        item.setCheckState(0, QtCore.Qt.Checked)
      else:
        item.setCheckState(0, QtCore.Qt.Unchecked)

  def selectAllProbes(self):
    """
    Отметить всех пациентов из списка пациентов, как приготовленных
    на экспорт.
    """
    self.statusBar().showMessage(u'Внимание: при больших размерах БД операция может занять длительное время.')
    # Получаем список всех пациентов
    for itemN in xrange(self.ui.trePatients.topLevelItemCount()):
      # Получаем единичный съём
      item = self.ui.trePatients.topLevelItem(itemN)
      # Отмечаем его галочкой
      item.setCheckState(0, QtCore.Qt.Checked)
      # Внимание!!! Далее - не очевидно.
      # после отмечания галочкой происходит срабатывания сигнала
      # trePatients.itemChanged и вызывается его обработчик.

  def selectAllPatientProbes(self, patient):
    """
    Отметить все съемы данного пациента, как приготовленные на экспорт.
    """
    # Получаем ID пациента
    id = patient.text(0)
    # Если галочку установили
    if patient.checkState(0):
      # Запрашиваем из базы все съемы пациента с данным Id
      probes = base.getPatientInfo(id)
      # Заносим все съёмы пациента в список экспорта
      self.patLst.reSetProbes(id, probes)
    # Если галочку сняли
    else:
      # Очищаем список экспорта данного пациента
      self.patLst.reSetProbes(id, None)
    # Перезагружаем виджет со списком экспорта
    self.refreshExportList()

  def selectProbe(self, probe):
    # Если элемент является съёмом
    if probe.childCount() == 0:
      # Получаем ID текущего пациента
      id = self.patLst.getID()
      # Меняем статус съема (выбран/не выбран)
      self.patLst.changeProbeStatus(id, str(probe.text(0)), probe.text(1))
      # Перезагружаем виджет со списком экспорта
      self.refreshExportList()
    # Если элемент является группой съёмов
    else:
      state = probe.checkState(0)
      for i in xrange(probe.childCount()):
        probe.child(i).setCheckState(0, state)

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
    # Запрашиваем дирректорию сохраниения съемов в системной кодировке
    dirName = pu.convert(QtGui.QFileDialog.getExistingDirectory(self,
                                                                u'Выберете дирректорию сохранения'))
    if dirName != '':
      # Получаем список съемов, приготовленнных к экспорту
      exportLst = self.patLst.getAllProbes()
      # Для каждого пациента в списке экспортных съемов
      for patient in exportLst.keys():
        # Для каждого съема конкретного пациента
        for date in exportLst[patient].keys():
          # Получаем дату съема
          trueDate = datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
          # преобразуем её в строку особого вида
          dateStr = trueDate.strftime('%Y-%m-%d-%H-%M-%S')
          # Получаем Ф.И.О пациента в нужной кодировке
          patientName = pu.convert(base.getPatientName(patient))
          # Суммируем полученные ранее переменные в полное имя файла
          fileName = os.path.join(dirName, patientName + '_' + dateStr + '.txt')
          # Открываем файл на запись
          tmpFile = open(fileName, "w")
          # Получаем матрицы съема
          lMatr, rMatr = base.getMatrix(patient, date)
          # Пишем матрицы по очереди в файл (Формат Новосибирска)
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
          # Закрываем файл
          tmpFile.close()
      # Информируем пользователя
      self.statusBar().showMessage(u'Экспорт прошёл успешно')

  def selectExportPatient(self, probe):
    '''
    Выбрать съем из списка экспорта для обработки
    '''
    # Извлекаем id и дату из выбранного съема
    id = probe.text(0)
    date = probe.text(2)
    # Сохраняем съем в patLst
    self.patLst.putProcesingProbe((id, str(date)))

  def markExportPatient(self, probe):
    '''
    Пометить/(снять метку) съем из списка экспорта для обработки
    '''
    pass

  def saveImage(self):
    '''
    Сохранение графика в изображение
    '''
    # Вставить проверку открытой вкладки
    # Получаем имя изображения в системной кодировке
    filename = QtGui.QFileDialog.getSaveFileName(self,
                                                 u'Выберете файл изображения',
                                                 QtCore.QDir.homePath(),
                                                 u"Изображение (*.png *.PNG)")
    if filename != '':
      Qt.QPixmap.grabWidget(self.ui.qwtGraphPlot).save(filename, 'PNG')
      # Информируем пользователя
      self.statusBar().showMessage(u'Изображение сохранено')

  def exportGarph(self):
    '''
    Сохранение данных графика во внешний файл
    '''
    pass

  def clearExport(self):
    '''
    Очистка списка экспорта
    '''
    self.ui.treExportProbes.clear()
    # Создаём новый список экспортных пациентов
    self.patLst = pr.ExportProbes()

  def plotMaxMin(self):
    '''
    Постоение графика Max-min
    '''
    # Очищаем поле вывода графика
    self.ui.qwtGraphPlot.clear()
    # Присваиваем графику название
    self.ui.qwtGraphPlot.setTitle(u'Max-Min')
    self.ui.qwtGraphPlot.setCanvasBackground(Qt.Qt.white)
    # grid
    self.ui.grid = Qwt.Qwt.QwtPlotGrid()
    self.ui.pen = Qt.QPen(Qt.Qt.DotLine)
    self.ui.pen.setColor(Qt.Qt.black)
    self.ui.pen.setWidth(1)
    self.ui.grid.setPen(self.ui.pen)
    self.ui.grid.attach(self.ui.qwtGraphPlot)
    # legend
    legend = Qwt.QwtLegend()
    legend.setFrameStyle(Qt.QFrame.Box)
    #legend.setItemMode(QwtLegend.ClickableItem)
    self.ui.qwtGraphPlot.insertLegend(legend, Qwt.QwtPlot.BottomLegend)
    # Получаем информацию съема
    probe = self.patLst.getProcessingProbe()
    # Если съем не выбран
    if probe == None:
      # Выводим предупреждение
      self.statusBar().showMessage(u'Пациент не выбран')
    # В случае, если съем присутствует
    else:
      # Получаем матрицы съема
      lMatr, rMatr = base.getMatrix(probe[0], probe[1])
      # Расчитываем MaxMin для каждого полушария
      lMaxMin = MathFunc.MaxMin(lMatr)
      rMaxMin = MathFunc.MaxMin(rMatr)
      # Построение графика левого полушария
      curve = Qwt.QwtPlotCurve(u'Левое полушарие')
      curve.attach(self.ui.qwtGraphPlot)
      curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
      curve.setPen(Qt.QPen(Qt.Qt.black, 2))
      curve.setData(range(1, 36), lMaxMin)
      # Построение графика правого полушария
      curve = Qwt.QwtPlotCurve(u'Правое полушарие')
      curve.attach(self.ui.qwtGraphPlot)
      curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
      curve.setPen(Qt.QPen(Qt.Qt.black, 2, Qt.Qt.DotLine))
      curve.setData(range(1, 36), rMaxMin)
      # Выводим график
      self.ui.qwtGraphPlot.replot()

  def plotVegetIndex(self):
    pass

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
                            platform.system())
                            )

def main():
  app = QtGui.QApplication(sys.argv)
  window = Main()
  window.show()
  sys.exit(app.exec_())

if __name__ == '__main__':
  main()
