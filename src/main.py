#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore
import PyQt4.Qt as Qt
import PyQt4.Qwt5 as Qwt #@UnresolvedImport
import GraphFunc as gf
# Главное окно
from MainForm import Ui_MainWindow
# Класс доступа к обрабатываемой БД
import DBInterface as db
# Класс хранения списка съемов для обработки
import ExportProbes as pr
import MathFunc
import datetime
# Платформозависимые функции-обёртки
import PlatformUtils as pu
import platform
import os

__version__ = "0.1.5"

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
    # Выбор таба графика
    self.ui.tabWidView.currentChanged.connect(self.changeTab)
    # Щелчёк по съему в окне экспорта
    self.ui.treExportProbes.itemClicked.connect(self.selectExportPatient)
    # Кнопка "Удалить" в окне экспорта
    self.ui.btnDelElem.clicked.connect(self.delExportItems)
    # Кнопка "Очистить" в окне экспорта
    self.ui.btnClearProbes.clicked.connect(self.clearExport)
    # Кнопка сохранения изображения графика
    self.ui.butSaveImage.clicked.connect(self.saveImage)
    # Кнопка экспорта данных графика
    self.ui.butGarphExport.clicked.connect(self.exportGarph)
    # Отображение графиков по щелчку на легенде
    self.ui.qwtSegPlot.legendChecked.connect(self.showCurve)
    # Построение графика MaxMin
    self.ui.actMaxMin.triggered.connect(self.plotMaxMin)
    # Построение графика корреляции по сегментам
    self.ui.actCorrelationFi.triggered.connect(self.plotCorrelationFi)
    # Постоение графика вегетативного индекса
    self.ui.actVI.triggered.connect(self.plotVegetIndex)
    # Разворачиваем на весь экран
    self.showMaximized()
    self.graphTab = 'graph'
    self.groupVI = True
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
    base = None
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
    # selectAllProbes()

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
    # selectAllPatientProbes()

  def selectProbe(self, probe):
    """
    Отметить единичный элемент в дереве съёмов
    """
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
      # Получаем свежеустановленный статус (отмечено/снято)
      state = probe.checkState(0)
      # Для всех потомков поддерева
      for i in xrange(probe.childCount()):
        # Устанавливаем тот же статус
        probe.child(i).setCheckState(0, state)
    # selectProbe()

  def refreshExportList(self):
    '''
    Перезагрузить список экспортных съемов.
    '''
    # Очищаем виджет экспортных съёмов
    self.ui.treExportProbes.clear()
    # Получаем список съемов, приготовленнных к экспорту
    exportLst = self.patLst.getAllProbes()
    # Выводим экспортные съёмы
    if exportLst:
      for patient in exportLst.keys():
        for date in exportLst[patient].keys():
          item = QtGui.QTreeWidgetItem([patient, base.getPatientName(patient), date, exportLst[patient][date] ])
          self.ui.treExportProbes.addTopLevelItem(item)
    # refreshExportList()

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
          trueDate = datetime.datetime.strptime(date, '%Y-%m-%d %H:%M:%S')
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
    # exportProbes()

  def selectExportPatient(self, probe):
    '''
    Выбрать съем из списка экспорта для обработки
    '''
    if self.graphTab == 'seg':
      self.plotSegment()
    elif self.graphTab == 'func':
      pass
    elif self.graphTab == 'graph':
      pass
#    elif self.graphTab == 'matr':    
    # selectExportPatient()

  def saveImage(self):
    '''
    Сохранение графика в изображение
    '''
    if self.graphTab == 'seg':
      plot = self.ui.qwtSegPlot
    elif self.graphTab == 'func':
      plot = self.ui.qwtFuncPlot
    elif self.graphTab == 'graph':
      plot = self.ui.qwtGraphPlot
#    elif self.graphTab == 'matr':
    # Получаем имя изображения в системной кодировке
    filename = QtGui.QFileDialog.getSaveFileName(self,
                                                 u'Выберете файл изображения',
                                                 QtCore.QDir.homePath(),
                                                 u"Изображение (*.png *.PNG)")
    if filename != '':
      Qt.QPixmap.grabWidget(plot).save(filename, 'PNG')
      # Информируем пользователя
      self.statusBar().showMessage(u'Изображение сохранено')

  def exportGarph(self):
    '''
    Сохранение данных графика во внешний файл
    '''
    pass

  def delExportItems(self):
    '''
    Удаление выделенных элементов списка экспорта
    '''
    if not self.ui.treExportProbes.selectedIndexes():
      return
    # Удаляем выбранные итемы
    for index in self.ui.treExportProbes.selectedItems():
      self.patLst.changeProbeStatus(index.text(0), str(index.text(2)), index.text(3))
    # Перезагружаем виджет со списком экспорта
    self.refreshExportList()
  # delExportItems()

  def changeTab(self):
    """
    Смена таба с графиком
    """
    if self.ui.tabWidView.currentIndex() == 1:
      self.graphTab = 'seg'
      self.plotSegment()
    if self.ui.tabWidView.currentIndex() == 2:
      self.graphTab = 'func'
    if self.ui.tabWidView.currentIndex() == 0:
      self.graphTab = 'matr'
    if self.ui.tabWidView.currentIndex() == 3:
      self.graphTab = 'graph'

  #changeTab()

  def showCurve(self, item, on):
    """
    Включить/отключить отображение графика
    """
    if self.graphTab == 'seg':
      plot = self.ui.qwtSegPlot
    elif self.graphTab == 'func':
      plot = self.ui.qwtFuncPlot
    elif self.graphTab == 'graph':
      plot = self.ui.qwtGraphPlot
    else:
      return
    item.setVisible(on)
    widget = plot.legend().find(item)
    if isinstance(widget, Qwt.Qwt.QwtLegendItem):
      widget.setChecked(on)
    plot.replot()

  # showCurve()

  def clearExport(self):
    '''
    Очистка списка экспорта
    '''
    self.ui.treExportProbes.clear()
    # Создаём новый список экспортных пациентов
    self.patLst = pr.ExportProbes()
    # clearExport()


  def plotMaxMin(self):
    '''
    Постоение графика Max-min
    '''
    # Если выделена не однастрока (4 поля)
    if len(self.ui.treExportProbes.selectedIndexes()) != 4:
      self.statusBar().showMessage(u'Пациент не выбран')
      return
    for index in self.ui.treExportProbes.selectedItems():
      # Получаем матрицы съема
      lMatr, rMatr = base.getMatrix(index.text(0), str(index.text(2)))
    # Расчитываем MaxMin для каждого полушария
    lMaxMin = MathFunc.MaxMin(lMatr)
    rMaxMin = MathFunc.MaxMin(rMatr)
    # подготавливаем холст
    gf.preparePlot(self.ui.qwtGraphPlot, u'Max-Min')
    gf.setAxis(self.ui.qwtGraphPlot)
    # markers (Вертикальны разделители)
    gf.plotVFuncMarkers(self.ui.qwtGraphPlot)
    # Построение графика левого полушария
    curve = Qwt.QwtPlotCurve(u'Левое полушарие')
    curve.attach(self.ui.qwtGraphPlot)
    curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
    curve.setPen(Qt.QPen(Qt.Qt.black, 2, Qt.Qt.DotLine))
    curve.setData(range(0, 35), lMaxMin)
    # Построение графика правого полушария
    curve = Qwt.QwtPlotCurve(u'Правое полушарие')
    curve.attach(self.ui.qwtGraphPlot)
    curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
    curve.setPen(Qt.QPen(Qt.Qt.black, 2))
    curve.setData(range(0, 35), rMaxMin)
    # Выводим график
    self.ui.qwtGraphPlot.replot()
    # plotMaxMin()

  def plotCorrelationFi(self):
    """
    Построение графика корреляции левого и правого полушария по сегментам
    """
    # Если выделена не однастрока (4 поля)
    if len(self.ui.treExportProbes.selectedIndexes()) != 4:
      self.statusBar().showMessage(u'Пациент не выбран')
      return
    for index in self.ui.treExportProbes.selectedItems():
      # Получаем матрицы съема
      lMatr, rMatr = base.getMatrix(index.text(0), str(index.text(2)))
    # Получаем матрицу корреляции
    corrMtrx = MathFunc.CorrelationSegI(lMatr, rMatr)
    # подготавливаем холст
    gf.preparePlot(self.ui.qwtGraphPlot, u'Корреляция Seg(L,R)')
    gf.setAxis(self.ui.qwtGraphPlot)
    # markers (Вертикальны разделители)
    gf.plotVFuncMarkers(self.ui.qwtGraphPlot)
    # ось абцисс
    gf.plotAbciss(self.ui.qwtGraphPlot)
    # Построение графика правого полушария
    curve = Qwt.QwtPlotCurve(u'Корреляция Seg(L,R)')
    curve.attach(self.ui.qwtGraphPlot)
    curve.setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
    curve.setPen(Qt.QPen(Qt.Qt.black, 2))
    curve.setData(range(0, 35), corrMtrx)
    # Выводим график
    self.ui.qwtGraphPlot.replot()


  def plotVegetIndex(self):
    """
    Построение вегетативного индекса (ВИ)
    """
    if not self.ui.treExportProbes.selectedIndexes():
      return
    srcVI = []
    rezVI = []
    rezDat = []
    # Перебираем все выделенные item-ы
    for index in self.ui.treExportProbes.selectedItems():
      # Получаем матрицы съема
      lMatr, rMatr = base.getMatrix(index.text(0), str(index.text(2)))
      # Расчитываем MaxMin для каждого полушария
      lMaxMin = MathFunc.MaxMin(lMatr)
      rMaxMin = MathFunc.MaxMin(rMatr)
      # Расчитываем ВИ и заносим его в список исходных ВИ
      VI = MathFunc.VegetIndex(lMaxMin, rMaxMin)
      srcVI.append([index.text(2), VI]) #extend
    # Сортируем по дате
    srcVI.sort()
    # Если выставлена группировка индексов по времени и дате
    if self.groupVI:
      # Номер группы
      group = 0
      # Число индексов в группе
      div = 1
      # Предыдущий обрабатываемый ВИ
      oldVI = 0
      for i in xrange(len(srcVI)):
        # Если первый элемент в массиве
        # то добавляем его в первую группу
        if oldVI == 0:
          rezVI.append(srcVI[i][1])
          rezDat.append(srcVI[i][0])
        else:
          d1 = datetime.datetime.strptime(str(srcVI[i][0]), '%Y-%m-%d %H:%M:%S')
          d2 = datetime.datetime.strptime(str(oldVI[0]), '%Y-%m-%d %H:%M:%S')
          diff = d1 - d2
          # Если разница по времени между съемами >= 7 минут (3 мин на
          # съем и 3 на тупняк между съемами)
          if diff.seconds / 60 >= 7:
            # Делим уже сложенные ВИ на их количество
            rezVI[group] = rezVI[group] / div
            # Формируем красивую дату с числом индексов
            d1 = datetime.datetime.strptime(str(rezDat[group]), '%Y-%m-%d %H:%M:%S')
            rezDat[group] = d1.strftime('%d.%m.%y %H:%M ') + '(' + str(div) + ')'
            # Добавляем текущий индекс в новую группу
            group = group + 1
            rezVI.append(srcVI[i][1])
            rezDat.append(srcVI[i][0])
            div = 1
          # Иначе суммируем текущий индекс с существующей суммой
          else:
            rezVI[group] = rezVI[group] + srcVI[i][1]
            div = div + 1
        oldVI = srcVI[i]
      # Завершающий расчёт
      else:
        # Делим уже сложенные ВИ на их количество
        rezVI[group] = rezVI[group] / div
        # Формируем красивую дату с числом индексов
        d1 = datetime.datetime.strptime(str(rezDat[group]), '%Y-%m-%d %H:%M:%S')
        rezDat[group] = d1.strftime('%d.%m.%y %H:%M ') + '(' + str(div) + ')'
    # Если группировка не выставлена
    else:
      for i in xrange(len(srcVI)):
        rezVI.append(srcVI[i][1])
        d1 = datetime.datetime.strptime(str(srcVI[i][0]), '%Y-%m-%d %H:%M:%S')
        rezDat.append(d1.strftime('%d.%m.%y %H:%M '))
    # Расчёт среднего ВИ (отрисовывается отдельно)
    sum = 0
    for i in xrange(len(rezVI)):
      sum = sum + rezVI[i]
    mean = sum / float(len(rezVI))
    # Расчёт максимального ВИ + 20%(для масштабирования)
    maxVI = 0
    for i in rezVI:
      if i > maxVI:
        maxVI = i
    if maxVI < 2.5:
      maxVI = 2.5
    maxVI = maxVI + maxVI * 0.2
    # Построение графика ВИ
    # подготавливаем холст
    gf.preparePlot(self.ui.qwtGraphPlot, u'Вегетативный индекс', leg = 'no')
    gf.setAxis(self.ui.qwtGraphPlot, 'index', rezDat, rezVI, maxVI)
    # График ВИ
    curve = Qwt.QwtPlotCurve(u'ВИ')
    curve.attach(self.ui.qwtGraphPlot)
    curve.setPen(Qt.QPen(Qt.Qt.black, 20))
    curve.setData(range(len(rezVI)), rezVI)
    curve.setStyle(Qwt.Qwt.QwtPlotCurve.Sticks)
    # Построение границ нормы
    gf.plotNormBorders(self.ui.qwtGraphPlot, 2.5, 0.5, mean)
    # Выводим график
    self.ui.qwtGraphPlot.replot()

  def plotSegment(self):
    """
    Построение по сегментам
    """
    cols = {'C1':Qt.Qt.black, 'C2-3':Qt.Qt.red, 'C4-5':Qt.Qt.blue,
            'C6':Qt.Qt.black, 'C7-8':Qt.Qt.red, 'Th1':Qt.Qt.blue,
            'Th2':Qt.Qt.black, 'Th3-4':Qt.Qt.red, 'Th5':Qt.Qt.blue,
            'Th6':Qt.Qt.black, 'Th7':Qt.Qt.red, 'Th8-9':Qt.Qt.blue,
            'Th10':Qt.Qt.black, 'Th11':Qt.Qt.red, 'Th12':Qt.Qt.blue,
            'L1':Qt.Qt.black, 'L2':Qt.Qt.red, 'L3':Qt.Qt.blue,
            'L4':Qt.Qt.black, 'L5':Qt.Qt.red, 'S1':Qt.Qt.blue,
            'S2':Qt.Qt.black, 'S3-4':Qt.Qt.red, 'K-S5':Qt.Qt.blue}

    # Если выделена не однастрока (4 поля)
    if len(self.ui.treExportProbes.selectedIndexes()) != 4:
      return
    # подготавливаем холст
    gf.preparePlot(self.ui.qwtSegPlot, u'Сегмент', leg = 'check')
    gf.setAxis(self.ui.qwtSegPlot)
    # markers (Вертикальны разделители)
    gf.plotVFuncMarkers(self.ui.qwtSegPlot)
    # Расчёт значений
    for index in self.ui.treExportProbes.selectedItems():
      # Получаем матрицы съема
      lMatr, rMatr = base.getMatrix(index.text(0), str(index.text(2)))
    # Получаем словарь сегментов для каждого полушария
    lSeg = MathFunc.Segment(lMatr)
    rSeg = MathFunc.Segment(rMatr)
    # Создаём словари curve
    curvL = {}
    curvR = {}
    # Строим графики по сементам
    for key in lSeg.keys():
      # Левое полушарие
      curvL[key] = Qwt.QwtPlotCurve(key)
      curvL[key].attach(self.ui.qwtSegPlot)
      curvL[key].setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
      curvL[key].setPen(Qt.QPen(cols[key], 2, Qt.Qt.DotLine))
      curvL[key].setData(range(len(lSeg[key])), lSeg[key])
      self.showCurve(curvL[key], False)
      # Правое полушарие
      curvR[key] = Qwt.QwtPlotCurve(key)
      curvR[key].attach(self.ui.qwtSegPlot)
      curvR[key].setRenderHint(Qwt.QwtPlotItem.RenderAntialiased)
      curvR[key].setPen(Qt.QPen(cols[key], 2))
      curvR[key].setData(range(len(rSeg[key])), rSeg[key])
      self.showCurve(curvR[key], False)
    # Выводим график
    self.showCurve(curvL['C1'], True)
    self.showCurve(curvR['C1'], True)
    self.ui.qwtSegPlot.replot()
  # plotSegment()

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
  # main()

if __name__ == '__main__':
  main()
