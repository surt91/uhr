#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class Communicate(QtCore.QObject):
    redraw = QtCore.pyqtSignal()

class Uhr():
    def __init__(self):
        super().__init__()

        self.c = Communicate()
        self.c.redraw.connect(self.on_update)

        # Timer
        self.iSeconds = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._time_update)

    def uhr_reset(self):
        self.iSeconds = 0
        self.c.redraw.emit()

    def _time_update(self):
        self.iSeconds += 1
        self.c.redraw.emit()

    def setTime(self, x):
        self.iSeconds = x
        self.c.redraw.emit()

    def startUhr(self):
        self.timer.start(1000)

    def stopUhr(self):
        self.timer.stop()

    def on_update(self):
        self.a.redraw(self.iSeconds)
#~
    #~ def setDigital(self):
        #~ self.display.removeWidget(self.a)
        #~ self.a.close()
        #~ self.a = DigitalUhrAnzeige()
        #~ self.display.addWidget(self.a)
        #~ self.c.redraw.emit()
#~
    #~ def setBinary(self):
        #~ self.display.removeWidget(self.a)
        #~ self.a.close()
        #~ self.a = BinaryUhrAnzeige()
        #~ self.display.addWidget(self.a)
        #~ self.c.redraw.emit()
#~
    #~ def setAnalog(self):
        #~ self.display.removeWidget(self.a)
        #~ self.a.close()
        #~ self.a = AnalogUhrAnzeige()
        #~ self.display.addWidget(self.a)
        #~ self.c.redraw.emit()
#~
    #~ def setAnalogBahnhof(self):
        #~ self.setAnalog()
        #~ self.a.pStyle = self.a.styles["bahnhof"]
#~
    #~ def setAnalogArc(self):
        #~ self.setAnalog()
        #~ self.a.pStyle = self.a.styles["arc"]
