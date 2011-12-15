#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class Communicate(QtCore.QObject):
    tick = QtCore.pyqtSignal()

class Uhr():
    def __init__(self):
        super().__init__()

        self.__c = Communicate()
        self.__c.tick.connect(self.on_update)

        # Timer
        self.__iSeconds = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.__time_update)

        self.setFreq(1)

    def uhr_reset(self):
        """
            Setzt die Uhr auf 0 Sekunden zurück
        """
        self.__iSeconds = 0
        self.__c.tick.emit()

    def __time_update(self):
        """
            Wird von einem Timer aufgerufen; zählt die Sekunden hoch und
            stößt ein NeuZeichnen an
        """
        self.__iSeconds += 1
        self.__c.tick.emit()

    def setTime(self, x):
        """
            Setzt die Zeit auf x Sekunden
        """
        self.__iSeconds = x
        self.__c.tick.emit()

    def setFreq(self, f):
        """
            Setzt die die Frequenz in Hz
        """
        self.__fFreq = f
        self.__c.tick.emit()

    def getSeconds(self):
        """
            gibt die Sekundenzahl zurück
        """
        return self.__iSeconds

    def startUhr(self):
        """
            Startet den Timer; die Uhr tickt nach dieser Funktion
        """
        self.timer.start(1000/self.__fFreq)

    def stopUhr(self):
        """
            Stoppt den Timer; die Uhr hält an
        """
        self.timer.stop()

    def on_update(self):
        pass
