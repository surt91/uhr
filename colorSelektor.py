#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt4 import QtGui, QtCore

class ColorSelektor(QtGui.QDialog):
    def __init__(self, default):
        super().__init__()

        self.__colors = default
        self.initUI()

    def initUI(self):
        self.btnText = QtGui.QPushButton(self)
        self.btnText.clicked.connect(self.__setText)
        self.makeIcon(self.__colors["text"], self.btnText)
        labelText = QtGui.QLabel('Uhrentext', self)

        self.btnBG   = QtGui.QPushButton(self)
        self.btnBG.clicked.connect(self.__setBG)
        self.makeIcon(self.__colors["bg"], self.btnBG)
        labelBG = QtGui.QLabel('Uhrenhintergrund', self)

        self.btnH    = QtGui.QPushButton(self)
        self.btnH.clicked.connect(self.__setH)
        self.makeIcon(self.__colors["h"], self.btnH)
        labelH = QtGui.QLabel('Stundenzeiger', self)

        self.btnM    = QtGui.QPushButton(self)
        self.btnM.clicked.connect(self.__setM)
        self.makeIcon(self.__colors["m"], self.btnM)
        labelM = QtGui.QLabel('Minutenzeiger', self)

        self.btnS    = QtGui.QPushButton(self)
        self.btnS.clicked.connect(self.__setS)
        self.makeIcon(self.__colors["s"], self.btnS)
        labelS = QtGui.QLabel('Sekundenzeiger', self)

        self.btnRand = QtGui.QPushButton(self)
        self.btnRand.clicked.connect(self.__setRand)
        self.makeIcon(self.__colors["rand"], self.btnRand)
        labelRand = QtGui.QLabel('Rand', self)

        hboxText = QtGui.QHBoxLayout()
        hboxText.addWidget(self.btnText)
        hboxText.addWidget(labelText)
        hboxText.addStretch(1)

        hboxBG = QtGui.QHBoxLayout()
        hboxBG.addWidget(self.btnBG)
        hboxBG.addWidget(labelBG)
        hboxBG.addStretch(1)

        hboxH = QtGui.QHBoxLayout()
        hboxH.addWidget(self.btnH)
        hboxH.addWidget(labelH)
        hboxH.addStretch(1)

        hboxM = QtGui.QHBoxLayout()
        hboxM.addWidget(self.btnM)
        hboxM.addWidget(labelM)
        hboxM.addStretch(1)

        hboxS = QtGui.QHBoxLayout()
        hboxS.addWidget(self.btnS)
        hboxS.addWidget(labelS)
        hboxS.addStretch(1)

        hboxRand = QtGui.QHBoxLayout()
        hboxRand.addWidget(self.btnRand)
        hboxRand.addWidget(labelRand)
        hboxRand.addStretch(1)

        btn = QtGui.QPushButton('Anwenden!', self)
        btn.clicked.connect(self.__sendVal)
        btn.setToolTip('Klicke hier um die neuen Farben abzuschicken')
        btn.setMaximumSize(btn.sizeHint())

        vbox1 = QtGui.QVBoxLayout()
        vbox1.addLayout(hboxText)
        vbox1.addLayout(hboxBG)
        vbox1.addLayout(hboxH)
        vbox1.addLayout(hboxM)
        vbox1.addLayout(hboxS)
        vbox1.addLayout(hboxRand)

        vbox2 = QtGui.QVBoxLayout()
        vbox2.addStretch(1)
        vbox2.addWidget(btn)

        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox1)
        hbox.addLayout(vbox2)

        self.setLayout(hbox)

        #~ self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('Farb Auswahl')

        self.show()

    def makeIcon(self, color, button):
        x = QtGui.QPixmap(100,100)
        x.fill(color)
        button.setIcon(QtGui.QIcon(x))

    def __setText(self):
        self.__colors['text'] = self.__setColor()
        self.makeIcon(self.__colors["text"], self.btnText)

    def __setBG(self):
        self.__colors['bg'] = self.__setColor()
        self.makeIcon(self.__colors["bg"], self.btnBG)

    def __setH(self):
        self.__colors['h'] = self.__setColor()
        self.makeIcon(self.__colors["h"], self.btnH)

    def __setM(self):
        self.__colors['m'] = self.__setColor()
        self.makeIcon(self.__colors["m"], self.btnM)

    def __setS(self):
        self.__colors['s'] = self.__setColor()
        self.makeIcon(self.__colors["s"], self.btnS)

    def __setRand(self):
        self.__colors['rand'] = self.__setColor()
        self.makeIcon(self.__colors["rand"], self.btnRand)

    def __setColor(self):
        return QtGui.QColorDialog.getColor()

    def __sendVal(self):
        self.emit(QtCore.SIGNAL('signalColorChanged'), self.__colors)
        self.close()
