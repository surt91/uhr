#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from uhrAnzeige import *
from uhrFunktion import *

#TODO: Dokumentation aller Funktionen

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
        self.display = QtGui.QHBoxLayout()
        self.display.addWidget(self.a)
        self.vbox = QtGui.QVBoxLayout()
        self.vbox.addStretch(1)
        self.vbox.addWidget(self.btn)
        self.vbox.addWidget(self.btn_reset)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addLayout(self.display)
        self.layout.addLayout(self.vbox)

        self.setLayout(self.layout)

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
        self.a.redraw(self.iSeconds)

class Uhrzeit(Uhr, QtGui.QWidget):
    def __init__(self):
        import time
        super().__init__()

        now=time.localtime()
        now = now[3]*3600+now[4]*60+now[5]

        self.a = UhrAnzeige()
        self.setTime(now)
        self.startUhr()

        self.initUI()

    def initUI(self):
        self.setToolTip('Dies ist eine Uhr')

        # Layout
        self.display = QtGui.QHBoxLayout()
        self.display.addWidget(self.a)
        self.setLayout(self.display)

        self.show()

    def getAnzeige(self):
        return self.a

    def on_update(self):
        super().on_update()
        self.a.redraw(self.iSeconds)

class UhrWindow(QtGui.QMainWindow):
    styles = { "last" : 0,
                "binary":1,    "digital":2,
                "analogArc":3, "analogBahnhof":4}
    funcs  = { "uhrzeit":0,   "stoppuhr":1}
    def __init__(self):
        super().__init__()

        self.style  = self.styles["digital"]
        self.func   = self.funcs["uhrzeit"]

        self.ticken = False

        self.initUI()

    # TODO: Uhr in Fenster zentrieren
    def initUI(self):
        # Fenstereigenschaften
        self.center()
        self.setWindowTitle('Uhr')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.setFunc()
        self.setStyle()
        self.makeMenu()

        self.show()

    def setStyle(self, style = styles["last"]):
        if style == self.styles["last"]:
            style = self.style
        else:
            self.style = style
        if self.style == self.styles["binary"]:
            self.a.setBinary()
        elif self.style == self.styles["digital"]:
            self.a.setDigital()
        elif self.style == self.styles["analogArc"]:
            self.a.setAnalogArc()
        elif self.style == self.styles["analogBahnhof"]:
            self.a.setAnalogBahnhof()
        else:
            raise AttributeError

    def setFunc(self):
        if self.func == self.funcs["uhrzeit"]:
            self.setUhrzeit()
        elif self.func == self.funcs["stoppuhr"]:
            self.setStoppuhr()
        else:
            raise AttributeError

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def makeMenu(self):
        # Menüeinträge
        iconBinary = QtGui.QIcon('binary.png')
        setBinaryAction = QtGui.QAction(iconBinary, '&Binary', self)
        setBinaryAction.setShortcut('b')
        setBinaryAction.setStatusTip('Binär Uhr')
        setBinaryAction.setCheckable(True)
        setBinaryAction.triggered.connect(self.setBinary)
        iconDigital = QtGui.QIcon('digital.png')
        setDigitalAction = QtGui.QAction(iconDigital, '&Digital', self)
        setDigitalAction.setShortcut('d')
        setDigitalAction.setStatusTip('Digital Uhr')
        setDigitalAction.setCheckable(True)
        setDigitalAction.triggered.connect(self.setDigital)

        iconAnalog = QtGui.QIcon('analog.png')
        setAnalogArcAction = QtGui.QAction(iconAnalog, '&Arc', self)
        setAnalogArcAction.setShortcut('a')
        setAnalogArcAction.setCheckable(True)
        setAnalogArcAction.triggered.connect(self.setAnalogArc)
        setAnalogBahnhofAction = QtGui.QAction(iconAnalog, 'Ba&hnhof', self)
        setAnalogBahnhofAction.setShortcut('h')
        setAnalogBahnhofAction.setCheckable(True)
        setAnalogBahnhofAction.triggered.connect(self.setAnalogBahnhof)

        toggleTickenAction = QtGui.QAction('&Ticken', self)
        toggleTickenAction.setShortcut('t')
        toggleTickenAction.setCheckable(True)
        toggleTickenAction.triggered.connect(self.toggleTicken)

        uhrDarstellung = QtGui.QActionGroup(self)
        setDigitalAction.setChecked(True)
        uhrDarstellung.addAction(setBinaryAction)
        uhrDarstellung.addAction(setDigitalAction)
        uhrDarstellung.addAction(setAnalogArcAction)
        uhrDarstellung.addAction(setAnalogBahnhofAction)


        iconStoppuhr = QtGui.QIcon('stoppuhr.png')
        setStoppuhrAction = QtGui.QAction(iconStoppuhr, '&Stoppuhr', self)
        setStoppuhrAction.setShortcut('s')
        setStoppuhrAction.setStatusTip('Stoppuhr')
        setStoppuhrAction.setCheckable(True)
        setStoppuhrAction.triggered.connect(self.setStoppuhr)
        iconUhrzeit = QtGui.QIcon('uhrzeit.png')
        setUhrzeitAction = QtGui.QAction(iconUhrzeit, '&Uhr', self)
        setUhrzeitAction.setShortcut('u')
        setUhrzeitAction.setStatusTip('Uhrzeit')
        setUhrzeitAction.setCheckable(True)
        setUhrzeitAction.triggered.connect(self.setUhrzeit)

        iconExit = QtGui.QIcon('exit.png')
        exitAction = QtGui.QAction(iconExit, '&Exit', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)

        uhrFkt = QtGui.QActionGroup(self)
        setUhrzeitAction.setChecked(True)
        uhrFkt.addAction(setUhrzeitAction)
        uhrFkt.addAction(setStoppuhrAction)

        menubar = QtGui.QMenuBar(self)
        menuFkt = menubar.addMenu('Funktion')
        menuDar = menubar.addMenu('Darstellung')
        menuDar.addAction(setDigitalAction)
        menuDar.addAction(setBinaryAction)
        menuAna = menuDar.addMenu("Analog")
        menuAna.addAction(setAnalogArcAction)
        menuAna.addAction(setAnalogBahnhofAction)
        menuAna.addSeparator()
        menuAna.addAction(toggleTickenAction)
        menuFkt.addAction(setUhrzeitAction)
        menuFkt.addAction(setStoppuhrAction)
        menuFkt.addAction(exitAction)

        self.setMenuBar(menubar)

    def setBinary(self):
        self.setStyle(self.styles["binary"])

    def setDigital(self):
        self.setStyle(self.styles["digital"])

    def setAnalogArc(self):
        self.setStyle(self.styles["analogArc"])

    def setAnalogBahnhof(self):
        self.setStyle(self.styles["analogBahnhof"])

    def setStoppuhr(self):
        self.func = self.funcs["stoppuhr"]
        self.disp = Stoppuhr()
        self.a = self.disp.getAnzeige()
        self.setCentralWidget(self.disp)
        self.setStyle()

    def setUhrzeit(self):
        self.func = self.funcs["uhrzeit"]
        self.disp = Uhrzeit()
        self.a = self.disp.getAnzeige()
        self.setCentralWidget(self.disp)
        self.setStyle()

    def toggleTicken(self):
        self.ticken = not self.ticken
        self.disp.a.setTicken(self.ticken)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = UhrWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
