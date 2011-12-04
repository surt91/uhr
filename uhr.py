#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class Communicate(QtCore.QObject):
    redraw = QtCore.pyqtSignal()

class Uhr():
    #~ def __init__(self):
        #~ pass

    def uhr_reset(self):
        self.x = 0
        self.c.redraw.emit()

    def _time_update(self):
        self.x += 1
        self.c.redraw.emit()

    def uhr_binary(self, x):
        return "  {1:04b}\n{2:06b}\n{3:06b}".format((x//86400),(x//3600)%24,(x//60)%60,x%60)

    def uhr_digital(self, x):
        return "{0:02d}:{1:02d}:{2:02d}:{3:02d}".format((x//86400),(x//3600)%24,(x//60)%60,x%60)

    def toggleBinary(self):
        if self.binary:
            self.binary = False
        else:
            self.binary = True
        self.c.redraw.emit()


class Stoppuhr(Uhr,QtGui.QWidget):
    def __init__(self):
        super(Stoppuhr, self).__init__()

        self.c = Communicate()
        self.c.redraw.connect(self.uhr_draw)

        self.binary = False

        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        self.setToolTip('Dies ist eine Stoppuhr')

        # Timer
        self.x = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._time_update)

        # Anzeige
        self.anzeige = QtGui.QLabel('0000:00:00', self)
        self.anzeige.setToolTip('Zeitformat: hhhh:mm:ss')

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
        #~ self.setCentralWidget(hbox)

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

    def uhr_draw(self):
        if self.binary:
            zeit = self.uhr_binary(self.x)
        else:
            zeit = self.uhr_digital(self.x)
        self.anzeige.setText(zeit)

class UhrWindow(QtGui.QMainWindow):
    def __init__(self):
        super(UhrWindow, self).__init__()

        self.initUI()

    def initUI(self):
        # Fenstereigenschaften
        self.center()
        self.setWindowTitle('Stoppuhr')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        stoppuhr = Stoppuhr()
        self.setCentralWidget(stoppuhr)

        toggleBinaryAction = QtGui.QAction(QtGui.QIcon('binary.png'), '&Binary', self)
        toggleBinaryAction.setShortcut('b')
        toggleBinaryAction.setStatusTip('Schalte Anzeige zwischen binary und digital um')
        toggleBinaryAction.triggered.connect(stoppuhr.toggleBinary)

        menubar = self.menuBar()
        menu = menubar.addMenu('Modus')
        menu.addAction(toggleBinaryAction)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

def main():
    app = QtGui.QApplication(sys.argv)
    #~ ex = Stoppuhr()
    ex = UhrWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
