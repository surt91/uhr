#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys

from Uhrzeit       import *
from Stoppuhr      import *
from zahlSelektor  import *
from colorSelektor import *

#TODO: Dokumentation aller Funktionen
#TODO: Icons
#TODO: Uhr in Fenster zentrieren
#TODO: Regenbogen so ändern, dass er das Wellenlängen spektrum des Lichts durchläuft

class UhrWindow(QtGui.QMainWindow):
    styles           = {"last"         : 0,
                        "binary"       : 1,
                        "digital"      : 2,
                        "analogArc"    : 3,
                        "analogBahnhof": 4}

    bgStyles         = {"last"         : 0,
                        "plain"        : 1,
                        "zahnrad"      : 2,
                        "sonne"        : 3,
                        "kein"         : 4}

    funcs            = {"uhrzeit"      : 0,
                        "stoppuhr"     : 1}
    def __init__(self):
        super().__init__()

        self.style   = self.styles["digital"]
        self.bgStyle = self.bgStyles["plain"]
        self.func    = self.funcs["uhrzeit"]

        self.ticken = False
        self.regenbogen = False

        self.initUI()

    def initUI(self):
        # Fenstereigenschaften
        self.center()
        self.setWindowTitle('Uhr')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.setFunc()
        self.setStyle()
        self.setBGStyle()
        self.makeMenu()

        self.show()

    def setStyle(self, style = styles["last"]):
        try:
            x = self.a.styles
        except AttributeError:
            self.a.styles = self.styles

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

    def setBGStyle(self, style = bgStyles["last"]):
        try:
            x = self.a.bgStyles
        except AttributeError:
            self.a.bgStyles = self.bgStyles

        if style == self.bgStyles["last"]:
            style = self.bgStyle
        else:
            self.bgStyle = style

        if self.bgStyle == self.bgStyles["plain"]:
            self.a.setBGPlain()
        elif self.bgStyle == self.bgStyles["zahnrad"]:
            self.a.setBGZahnrad()
        elif self.bgStyle == self.bgStyles["sonne"]:
            self.a.setBGSonne()
        elif self.bgStyle == self.bgStyles["kein"]:
            self.a.setBGKein()
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

        iconColor = QtGui.QIcon('color.png')
        setColorAction = QtGui.QAction(iconColor, '&Farbe', self)
        setColorAction.setShortcut('c')
        setColorAction.setCheckable(False)
        setColorAction.triggered.connect(self.setColor)

        iconBGKein = QtGui.QIcon('BGKein.png')
        setBGKeinAction = QtGui.QAction(iconBGKein, 'keiner', self)
        setBGKeinAction.setCheckable(False)
        setBGKeinAction.triggered.connect(self.setBGKein)

        iconBGPlain = QtGui.QIcon('BGPlain.png')
        setBGPlainAction = QtGui.QAction(iconBGPlain, 'einfarbig', self)
        setBGPlainAction.setCheckable(False)
        setBGPlainAction.triggered.connect(self.setBGPlain)

        iconBGZahnrad = QtGui.QIcon('BGZahnrad.png')
        setBGZahnradAction = QtGui.QAction(iconBGZahnrad, 'Zahnrad', self)
        setBGZahnradAction.setCheckable(False)
        setBGZahnradAction.triggered.connect(self.setBGZahnrad)

        iconBGSonne = QtGui.QIcon('BGSonne.png')
        setBGSonneAction = QtGui.QAction(iconBGSonne, 'Sonne', self)
        setBGSonneAction.setCheckable(False)
        setBGSonneAction.triggered.connect(self.setBGSonne)

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

        setFreqAction = QtGui.QAction('&Frequenz', self)
        setFreqAction.setShortcut('f')
        setFreqAction.setCheckable(False)
        setFreqAction.triggered.connect(self.setFreq)

        toggleRegenbogenAction = QtGui.QAction('Regenbogenzeiger', self)
        toggleRegenbogenAction.setShortcut('r')
        toggleRegenbogenAction.setCheckable(True)
        toggleRegenbogenAction.triggered.connect(self.toggleRegenbogen)

        uhrFkt = QtGui.QActionGroup(self)
        setUhrzeitAction.setChecked(True)
        uhrFkt.addAction(setUhrzeitAction)
        uhrFkt.addAction(setStoppuhrAction)

        # Menüs
        menubar = QtGui.QMenuBar(self)
        menuFkt = menubar.addMenu('Funktion')
        menuDar = menubar.addMenu('Darstellung')
        menuSch = menubar.addMenu('Schnickschnack')

        menuFkt.addAction(setUhrzeitAction)
        menuFkt.addAction(setStoppuhrAction)
        menuFkt.addAction(exitAction)

        menuDar.addAction(setDigitalAction)
        menuDar.addAction(setBinaryAction)
        menuAna = menuDar.addMenu("Analog")
        menuAna.addAction(setAnalogArcAction)
        menuAna.addAction(setAnalogBahnhofAction)
        menuAna.addSeparator()
        menuAna.addAction(toggleTickenAction)
        menuAna.addSeparator()
        menuAna.addAction(setBGKeinAction)
        menuAna.addAction(setBGPlainAction)
        menuAna.addAction(setBGZahnradAction)
        menuAna.addAction(setBGSonneAction)
        menuDar.addSeparator()
        menuDar.addAction(setColorAction)

        menuSch.addAction(setFreqAction)
        menuSch.addAction(toggleRegenbogenAction)

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
        self.setBGStyle()

    def setUhrzeit(self):
        self.func = self.funcs["uhrzeit"]
        self.disp = Uhrzeit()
        self.a = self.disp.getAnzeige()
        self.setCentralWidget(self.disp)
        self.setStyle()
        self.setBGStyle()

    def toggleTicken(self):
        self.ticken = not self.ticken
        self.disp.a.setTicken(self.ticken)

    def toggleRegenbogen(self):
        self.regenbogen = not self.regenbogen
        self.disp.a.setRegenbogen(self.regenbogen)

    def setFreq(self):
        freqChooser = ZahlSelektor(self.disp.getFreq())
        self.connect(freqChooser, QtCore.SIGNAL('signalFreqChanged'), self.disp.setFreq)
        freqChooser.exec_()

    def setColor(self):
        colorChooser = ColorSelektor(self.a.getColor())
        self.connect(colorChooser, QtCore.SIGNAL('signalColorChanged'), self.a.setColor)
        colorChooser.exec_()

    def setBGKein(self):
        self.setBGStyle(self.bgStyles["kein"])

    def setBGPlain(self):
        self.setBGStyle(self.bgStyles["plain"])

    def setBGZahnrad(self):
        self.setBGStyle(self.bgStyles["zahnrad"])

    def setBGSonne(self):
        self.setBGStyle(self.bgStyles["sonne"])

def main():
    app = QtGui.QApplication(sys.argv)
    ex = UhrWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
