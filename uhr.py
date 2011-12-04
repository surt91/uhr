#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
from PyQt4 import QtGui, QtCore

class Stoppuhr(QtGui.QWidget):

    def __init__(self):
        super(Stoppuhr, self).__init__()

        self.initUI()

    def initUI(self):
        QtGui.QToolTip.setFont(QtGui.QFont('SansSerif', 10))

        # Fenstereigenschaften
        self.center()
        self.setWindowTitle('Stoppuhr')
        self.setWindowIcon(QtGui.QIcon('icon.png'))
        self.setToolTip('Dies ist eine Stoppuhr')

        # Timer
        self.x = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self._time_update)

        # Anzeige
        self.anzeige = QtGui.QLabel('0000:00:00', self)
        self.anzeige.setToolTip('Zeitformat: hhhh:mm:ss')

        #Start- und Stoppknopf
        self.btn = QtGui.QPushButton('Start!', self)
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

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def uhr_reset(self):
        self.x = 0
        self.uhr_update()

    def uhr_toggle(self):
        if self.btn.isChecked():
            self.timer.start(1000)
            self.btn.setText("Stopp!")
            self.btn_reset.setDisabled(True)
        else:
            self.timer.stop()
            self.btn.setText("Start!")
            self.btn_reset.setDisabled(False)

    def _time_update(self):
        self.x += 1
        self.uhr_update()

    def uhr_update(self):
        x = self.x
        text = "{1:02d}:{1:02d}:{2:02d}:{3:02d}".format((x//86400),(x//3600)%24,(x//60)%60,x%60)
        self.anzeige.setText(text)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = Stoppuhr()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
