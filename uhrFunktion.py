#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class Communicate(QtCore.QObject):
    tick = QtCore.pyqtSignal()

class Uhr():
    def __init__(self):
        super().__init__()

        self.c = Communicate()
        self.c.tick.connect(self.on_update)

        # Timer
        self.iSeconds = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._time_update)

    def uhr_reset(self):
        self.iSeconds = 0
        self.c.tick.emit()

    def _time_update(self):
        self.iSeconds += 1
        self.c.tick.emit()

    def setTime(self, x):
        self.iSeconds = x
        self.c.tick.emit()

    def startUhr(self):
        self.timer.start(1000)

    def stopUhr(self):
        self.timer.stop()

    def on_update(self):
        pass
