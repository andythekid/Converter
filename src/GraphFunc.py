#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''
Created on 15.05.2011

@author: Andrey Volkov
@contact: evil.bobby@gmail.com
'''
import PyQt4.Qwt5 as Qwt
import PyQt4.Qt as Qt

# Именования функций по оси абцисс
funcLabel = [ '1', '2', '3<p>F1', '4', '5',
              '1', '2', '3<p>F2', '4', '5',
              '1', '2', '3<p>F3', '4', '5',
              '1', '2', '3<p>F4', '4', '5',
              '1', '2', '3<p>F5', '4', '5',
              '1', '2', '3<p>F6', '4', '5',
              '1', '2', '3<p>F7', '4', '5' ]

class TextScaleDraw(Qwt.QwtScaleDraw):
  """
  Класс для отрисовки Axis-a Qwt, переданного в форме строки
  """
  def __init__(self, labelStrings, *args):
    """
    Initialize text scale draw with label strings and any other arguments that
    """
    Qwt.QwtScaleDraw.__init__(self, *args)
    self.labelStrings = labelStrings
  # __init__()

  def label(self, value):
    """
    Apply the label at location 'value' .  Since this class is to be used for BarPlots
    or LinePlots, every item in 'value' should be an integer.
    """
    label = Qt.QString(self.labelStrings[int(value)])
    return Qwt.QwtText(label)
  # label()

# TEXTSCALE DRAW END

def preparePlot(plot, name, leg = 'stand'):
  """
  Подготовка холста (очистка, постоение сетки, легенда)
  """
  # Очищаем поле вывода графика
  plot.clear()
  # Присваиваем графику название
  plot.setTitle(name)
  plot.setCanvasBackground(Qt.Qt.white)
  # grid
  grid = Qwt.Qwt.QwtPlotGrid()
  pen = Qt.QPen(Qt.Qt.DotLine)
  pen.setColor(Qt.Qt.black)
  pen.setWidth(1)
  grid.setPen(pen)
  grid.attach(plot)
  # legend
  if leg != 'no':
    legend = Qwt.QwtLegend()
    legend.setFrameStyle(Qt.QFrame.Box)
    if leg == 'stand':
      plot.insertLegend(legend, Qwt.QwtPlot.BottomLegend)
    elif leg == 'check':
      legend.setItemMode(Qwt.Qwt.QwtLegend.CheckableItem)
      plot.insertLegend(legend, Qwt.QwtPlot.RightLegend)

def setAxis(plot, type = 'func', rezDat = 'no', rezInd = 'no', maxInd = 'no'):
  """
  Таки да, устанавливаем Axis
  """
  # Axis
  if type == 'func':
    plot.setAxisScaleDraw(
      Qwt.QwtPlot.xBottom, TextScaleDraw(funcLabel))
    plot.setAxisMaxMajor(Qwt.QwtPlot.xBottom, 35)
    plot.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0)
    plot.setAxisAutoScale(Qwt.Qwt.QwtPlot.yLeft)
  elif type == 'index':
    plot.setAxisScaleDraw(
      Qwt.QwtPlot.xBottom, TextScaleDraw(rezDat))
    plot.setAxisMaxMajor(Qwt.QwtPlot.xBottom, len(rezInd))
    plot.setAxisMaxMinor(Qwt.QwtPlot.xBottom, 0)
    plot.setAxisLabelRotation(Qwt.Qwt.QwtPlot.xBottom, -90.0)
    plot.setAxisLabelAlignment(Qwt.Qwt.QwtPlot.xBottom, Qt.Qt.AlignLeft)
    plot.setAxisScale(Qwt.Qwt.QwtPlot.yLeft, 0, maxInd, 0.5)

def plotAbciss(plot):
  """
  Построение оси абцисс
  """
  m1 = Qwt.Qwt.QwtPlotMarker()
  m1.setValue(0.0, 0.0)
  m1.setLineStyle(Qwt.Qwt.QwtPlotMarker.HLine)
  m1.setLinePen(Qt.QPen(Qt.Qt.black))
  m1.attach(plot)

def plotVFuncMarkers(plot):
  """
  Построение вертикальных разделителей по функциям
  для улучшения визуализации
  """
  # markers (Вертикальны разделители)
  m1 = Qwt.Qwt.QwtPlotMarker()
  m1.setValue(4.0, 0.0)
  m1.setLineStyle(Qwt.Qwt.QwtPlotMarker.VLine)
  m1.setLinePen(Qt.QPen(Qt.Qt.black))
  m1.attach(plot)
  m2 = Qwt.Qwt.QwtPlotMarker()
  m2.setValue(9.0, 0.0)
  m2.setLineStyle(Qwt.Qwt.QwtPlotMarker.VLine)
  m2.setLinePen(Qt.QPen(Qt.Qt.black))
  m2.attach(plot)
  m3 = Qwt.Qwt.QwtPlotMarker()
  m3.setValue(14.0, 0.0)
  m3.setLineStyle(Qwt.Qwt.QwtPlotMarker.VLine)
  m3.setLinePen(Qt.QPen(Qt.Qt.black))
  m3.attach(plot)
  m4 = Qwt.Qwt.QwtPlotMarker()
  m4.setValue(19.0, 0.0)
  m4.setLineStyle(Qwt.Qwt.QwtPlotMarker.VLine)
  m4.setLinePen(Qt.QPen(Qt.Qt.black))
  m4.attach(plot)
  m5 = Qwt.Qwt.QwtPlotMarker()
  m5.setValue(24.0, 0.0)
  m5.setLineStyle(Qwt.Qwt.QwtPlotMarker.VLine)
  m5.setLinePen(Qt.QPen(Qt.Qt.black))
  m5.attach(plot)
  m6 = Qwt.Qwt.QwtPlotMarker()
  m6.setValue(29.0, 0.0)
  m6.setLineStyle(Qwt.Qwt.QwtPlotMarker.VLine)
  m6.setLinePen(Qt.QPen(Qt.Qt.black))
  m6.attach(plot)

def plotNormBorders(plot, max, min, mean):
  """
  построение горизонтальных линий границ нормы
  """
  # Максимум нормы
  m1 = Qwt.Qwt.QwtPlotMarker()
  m1.setValue(0.0, max)
  m1.setLineStyle(Qwt.Qwt.QwtPlotMarker.HLine)
  m1.setLinePen(Qt.QPen(Qt.Qt.red))
  m1.attach(plot)
  # Минимум нормы
  m2 = Qwt.Qwt.QwtPlotMarker()
  m2.setValue(0.0, min)
  m2.setLineStyle(Qwt.Qwt.QwtPlotMarker.HLine)
  m2.setLinePen(Qt.QPen(Qt.Qt.blue))
  m2.attach(plot)
  # Среднее
  m3 = Qwt.Qwt.QwtPlotMarker()
  m3.setValue(0.0, mean)
  m3.setLineStyle(Qwt.Qwt.QwtPlotMarker.HLine)
  m3.setLinePen(Qt.QPen(Qt.Qt.green))
  m3.attach(plot)
