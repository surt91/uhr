#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore
import time

class Uhr():
    def __init__(self):
        super().__init__()

        self.__fPeriod = 1

        self.signalTick = QtCore.SIGNAL('signalTicked')
        self.connect(self, self.signalTick, self.on_update)

        # Timer
        self.__iSeconds = 0
        self.__timer = QtCore.QTimer()
        self.__timer.timeout.connect(self.__time_update)

        self.__running = False

        self.setFreq(1)

    def uhr_reset(self):
        """
            Setzt die Uhr auf 0 Sekunden zurück
        """
        self.__iSeconds = 0
        self.emit(self.signalTick)

    def __time_update(self):
        """
            Wird von einem Timer aufgerufen; zählt die Sekunden hoch und
            stößt ein NeuZeichnen an
        """
        self.__iSeconds += self.__fPeriod
        self.emit(self.signalTick)

    def setTime(self, x):
        """
            Setzt die Zeit auf x Sekunden
        """
        self.__iSeconds = x
        self.emit(self.signalTick)

    def setTimeNow(self):
        now=time.localtime()
        now = now[3]*3600+now[4]*60+now[5]
        self.setTime(now)

    def setFreq(self, f):
        """
            Setzt die die Frequenz in Hz
        """
        self.__fFreq = f
        if self.__running:
            self.stopUhr()
            self.startUhr()
        else:
            self.stopUhr()
        self.emit(self.signalTick)

    def setSecLength(self, T):
        """
            Setzt die Sekundenlänge in SI Sekunden
        """
        self.__fFreq = 1/T
        self.__fPeriod = T
        if self.__running:
            self.stopUhr()
            self.startUhr()
        else:
            self.stopUhr()
        self.emit(self.signalTick)

    def getFreq(self):
        """
            gibt die aktuelle Frequenz aus
        """
        return self.__fFreq

    def getSeconds(self):
        """
            gibt die Sekundenzahl zurück
        """
        return self.__iSeconds

    def startUhr(self):
        """
            Startet den Timer; die Uhr tickt nach dieser Funktion
        """
        self.__running = True
        self.__timer.start(1000/self.__fFreq)

    def stopUhr(self):
        """
            Stoppt den Timer; die Uhr hält an
        """
        self.__running = False
        self.__timer.stop()

    def on_update(self):
        pass
