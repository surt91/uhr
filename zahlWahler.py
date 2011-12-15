#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class ZahlWahler(QtGui.QDialog):
    def __init__(self, default):
        super().__init__()

        self.initUI(default)

    def initUI(self, default):
        lcd = QtGui.QLCDNumber(self)
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld.setRange(1,100)
        sld.setTracking(True)

        sld.setValue(default)
        lcd.display(default)
        self.wert = default
        self.freq = default

        sld.valueChanged.connect(lcd.display)
        sld.valueChanged.connect(self.setVal)

        self.btn = QtGui.QPushButton('&Setzen!', self)
        self.btn.clicked.connect(self.sendFreq)
        self.btn.setToolTip('Klicke hier um die neue Frequenz abzuschicken')
        self.btn.setMaximumSize(self.btn.sizeHint())

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(lcd)
        vbox1.addWidget(sld)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(self.btn)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Frequenz Auswahl')

        self.show()


    def setVal(self, x):
        self.wert = x

    def sendFreq(self):
        self.emit(QtCore.SIGNAL('signalFreqChanged'), self.wert)
        self.close()
