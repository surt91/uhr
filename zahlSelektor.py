#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class ZahlSelektor(QtGui.QDialog):
    def __init__(self, default):
        super().__init__()

        self.initUI(default)

    #~ def __del__(self):
        #~ print("kaputt")

    def initUI(self, default):
        lcd = QtGui.QLCDNumber(self)
        sld = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        sld.setRange(1,100)
        sld.setTracking(True)

        sld.setValue(default)
        lcd.display(default)
        self.__wert = default

        sld.valueChanged.connect(lcd.display)
        sld.valueChanged.connect(self.__setVal)

        btn = QtGui.QPushButton('&Setzen!', self)
        btn.clicked.connect(self.__sendVal)
        btn.setToolTip('Klicke hier um die neue Frequenz abzuschicken')
        btn.setMaximumSize(btn.sizeHint())

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addWidget(lcd)
        vbox1.addWidget(sld)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(btn)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        #~ self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Frequenz Auswahl')

        self.show()

    def __setVal(self, x):
        self.__wert = x

    def __sendVal(self):
        self.emit(QtCore.SIGNAL('signalFreqChanged'), self.__wert)
        self.close()
