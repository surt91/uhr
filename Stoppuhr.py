#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from uhrAnzeige  import *
from uhrFunktion import *

class Stoppuhr(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.a = UhrAnzeige()
        self.a.redraw(0)
        self.initUI()

    def initUI(self):
        self.setToolTip('Dies ist eine Stoppuhr')

        #Start- und Stoppknopf
        self.btn = QtGui.QPushButton('&Start!', self)
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.uhr_toggle)
        self.btn.setToolTip('Klicke hier zum Starten/Stoppen der Uhr')
        self.btn.setMaximumSize(self.btn.sizeHint())

        # Reset
        self.btn_reset = QtGui.QPushButton('Reset', self)
        self.btn_reset.clicked.connect(self.uhr_reset)
        self.btn_reset.setToolTip('Klicke hier zum Zurücksetzten der Uhr')
        self.btn_reset.setMaximumSize(self.btn_reset.sizeHint())

        # Layout
        display = QtGui.QHBoxLayout()
        display.addWidget(self.a)
        vbox = QtGui.QVBoxLayout()
        vbox.addStretch(1)
        vbox.addWidget(self.btn)
        vbox.addWidget(self.btn_reset)
        layout = QtGui.QHBoxLayout()
        layout.addLayout(display)
        layout.addLayout(vbox)

        self.setLayout(layout)

        self.show()

    def uhr_toggle(self):
        if self.btn.isChecked():
            self.startUhr()
            self.btn.setText("Stopp!")
            self.btn_reset.setDisabled(True)
        else:
            self.stopUhr()
            self.btn.setText("Start!")
            self.btn_reset.setDisabled(False)

    def getAnzeige(self):
        return self.a

    def on_update(self):
        super().on_update()
        try:
            self.a.redraw(self.getSeconds())
        except:
            pass

