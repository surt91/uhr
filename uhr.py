#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class Communicate(QtCore.QObject):
    redraw = QtCore.pyqtSignal()

class Uhr():
    def __init__(self):
        super().__init__()

        self.c = Communicate()
        self.c.redraw.connect(self.on_update)

        # Timer
        self.iSeconds = 0
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self._time_update)

    def uhr_reset(self):
        self.iSeconds = 0
        self.c.redraw.emit()

    def _time_update(self):
        self.iSeconds += 1
        self.c.redraw.emit()

    def uhrSetTime(self, x):
        self.iSeconds = x

    def on_update(self):
        pass

class AnalogUhr():
    pass

class DigitalUhrAnzeige(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        # Anzeige
        self.anzeige = QtGui.QLabel('', self)

        self.anzeige.setToolTip("dd:hh:mm:ss")
        self.redraw(0)

    def redraw(self, iSeconds):
        self.iSeconds = iSeconds
        sZeit = self.digital(iSeconds)
        self.anzeige.setText(sZeit)

    def digital(self, x):
        return "{0:02d}:{1:02d}:{2:02d}:{3:02d}"\
                        .format((x//86400),(x//3600)%24,(x//60)%60,x%60)


class BinaryUhrAnzeige(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        # Anzeige
        self.anzeige = QtGui.QLabel('', self)

        self.anzeige.setToolTip("dd:hh:mm:ss")
        self.redraw(0)

    def redraw(self, iSeconds):
        self.iSeconds = iSeconds
        sZeit = self.binary(iSeconds)
        self.anzeige.setText(sZeit)
        self.anzeige.setToolTip("<pre>  dddd\n  hhhh\nmmmmmm\nssssss<\pre>")

    def binary(self, x):
        return "<pre>  {0:04b}\n  {1:04b}\n{2:06b}\n{3:06b}</pre>"\
                        .format((x//86400),(x//3600)%24,(x//60)%60,x%60)

class Stoppuhr(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.a = DigitalUhrAnzeige()
        self.initUI()

    def initUI(self):
        self.setToolTip('Dies ist eine Stoppuhr')

        #Start- und Stoppknopf
        self.btn = QtGui.QPushButton('&Start!', self)
        self.btn.setCheckable(True)
        self.btn.clicked.connect(self.uhr_toggle)
        self.btn.setToolTip('Klicke hier zum Starten/Stoppen der Uhr')

        # Reset
        self.btn_reset = QtGui.QPushButton('Reset', self)
        self.btn_reset.clicked.connect(self.uhr_reset)
        self.btn_reset.setToolTip('Klicke hier zum Zurücksetzten der Uhr')

        # Layout
        hbox = QtGui.QHBoxLayout()
        hbox.addWidget(self.a.anzeige)
        hbox.addStretch(1)
        hbox.addWidget(self.btn)
        hbox.addWidget(self.btn_reset)

        self.setLayout(hbox)

        self.show()

    def on_update(self):
        self.a.redraw(self.iSeconds)

    def setDigital(self):
        pass

    def setBinary(self):
        pass

    def setAnalog(self):
        pass



    def uhr_toggle(self):
        if self.btn.isChecked():
            self.timer.start(1000)
            self.btn.setText("Stopp!")
            self.btn_reset.setDisabled(True)
        else:
            self.timer.stop()
            self.btn.setText("Start!")
            self.btn_reset.setDisabled(False)

class UhrWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Fenstereigenschaften
        self.center()
        self.setWindowTitle('Stoppuhr')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        stoppuhr = Stoppuhr()
        self.setCentralWidget(stoppuhr)

        # Menüeinträge
        iconBinary = QtGui.QIcon('binary.png')
        setBinaryAction = QtGui.QAction(iconBinary, '&Binary', self)
        setBinaryAction.setShortcut('b')
        setBinaryAction.setStatusTip('Binär Uhr')
        setBinaryAction.triggered.connect(stoppuhr.setBinary)
        iconDigital = QtGui.QIcon('digital.png')
        setDigitalAction = QtGui.QAction(iconDigital, '&Digital', self)
        setDigitalAction.setShortcut('d')
        setDigitalAction.setStatusTip('Digital Uhr')
        setDigitalAction.triggered.connect(stoppuhr.setDigital)
        iconAnalog = QtGui.QIcon('analog.png')
        setAnalogAction = QtGui.QAction(iconAnalog, '&Analog', self)
        setAnalogAction.setShortcut('a')
        setAnalogAction.setStatusTip('Analoge Uhr')
        setAnalogAction.triggered.connect(stoppuhr.setAnalog)

        menubar = self.menuBar()
        menuFkt = menubar.addMenu('Funktion')
        menuDar = menubar.addMenu('Darstellung')
        menuDar.addAction(setDigitalAction)
        menuDar.addAction(setBinaryAction)
        #~ menuDar.addSeperator()
        menuDar.addAction(setAnalogAction)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QtGui.QApplication(sys.argv)
    ex = UhrWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
