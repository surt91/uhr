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
        self.c.redraw.connect(self.uhr_draw)

        # Timer
        self.iSeconds = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._time_update)

    def uhr_reset(self):
        self.iSeconds = 0
        self.c.redraw.emit()

    def _time_update(self):
        self.iSeconds += 1
        self.c.redraw.emit()

    def uhrSetTime(self, x):
        self.iSeconds = x

    def setDigital(self):
        self.bBinary = False
        self.sZeitformat = "dd:hh:mm:ss"
        self.c.redraw.emit()

    def setBinary(self):
        self.bBinary = True
        self.sZeitformat = "<pre>  dddd\n  hhhh\nmmmmmm\nssssss<\pre>"
        self.c.redraw.emit()

class AnalogUhr():
    pass

class TextUhr(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        # Anzeige
        self.anzeige = QtGui.QLabel('', self)
        self.setDigital()

    def uhr_draw(self):
        if self.bBinary:
            sZeit = self.uhr_binary(self.iSeconds)
        else:
            sZeit = self.uhr_digital(self.iSeconds)
        self.anzeige.setText(sZeit)
        self.anzeige.setToolTip(self.sZeitformat)

    def uhr_binary(self, x):
        return "<pre>  {0:04b}\n  {1:04b}\n{2:06b}\n{3:06b}</pre>"\
                        .format((x//86400),(x//3600)%24,(x//60)%60,x%60)

    def uhr_digital(self, x):
        return "{0:02d}:{1:02d}:{2:02d}:{3:02d}"\
                        .format((x//86400),(x//3600)%24,(x//60)%60,x%60)

class Stoppuhr(TextUhr):
    def __init__(self):
        super().__init__()

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
        hbox.addWidget(self.anzeige)
        hbox.addStretch(1)
        hbox.addWidget(self.btn)
        hbox.addWidget(self.btn_reset)

        self.setLayout(hbox)

        self.show()

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

        menubar = self.menuBar()
        menu = menubar.addMenu('Modus')
        menu.addAction(setDigitalAction)
        menu.addAction(setBinaryAction)

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
