#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from uhrAnzeige  import *
from uhrFunktion import *

class Uhrzeit(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.a = UhrAnzeige()
        self.setTimeNow()
        self.startUhr()

        self.initUI()

    def initUI(self):
        self.setToolTip('Dies ist eine Uhr')

        # Layout
        display = QtGui.QHBoxLayout()
        display.addWidget(self.a)
        self.setLayout(display)

        self.show()

    def getAnzeige(self):
        return self.a

    def on_update(self):
        super().on_update()
        try:
            self.a.redraw(self.getSeconds())
        except:
            pass
