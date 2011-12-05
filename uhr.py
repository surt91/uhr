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

class UhrAnzeige(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(100,50)

        self.show()

    def on_redraw(self):
        self.update()

    def paintEvent(self, event):
        paint = QtGui.QPainter(self)
        paint.eraseRect(self.geometry())
        paint.setPen(QtGui.QColor(255, 255, 255))
        paint.setFont(QtGui.QFont('Monospace', 10))
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, self.sText)

class AnalogUhrAnzeige(UhrAnzeige):
    # TODO: drehende Zahnräder hinter Loch in Uhrblatt
    import math
    def __init__(self):
        super().__init__()

        self.setToolTip("Die Winkel der Zeiger:\n\
                        rot*60/2Pi   -> Sekunden\n\
                        klein*60/2Pi -> Minuten\n\
                        dick*24/2Pi  -> Stunden")

    def redraw(self, iSeconds):
        #~ sZeit = self.digital(iSeconds)
        #~ self.anzeige.setText(sZeit)
        self.update()
        pass

    def analog(self, x):
        """
            Nimmt Sekunden engegen und gibt eine Liste der Winkel aus:
            Erst Stunden, dann Mintuen, dann Sekunden Winkel
        """
        s = (x%60)/60. * 2 * math.pi
        m = ((x/60)%60)/60. * 2 * math.pi
        h = ((x/3600)%24)/24. * 2 * math.pi
        return [h,m,s]

class DigitalUhrAnzeige(UhrAnzeige):
    def __init__(self):
        super().__init__()

        self.setToolTip("hh:mm:ss")

    def redraw(self, iSeconds):
        sZeit = self.digital(iSeconds)
        self.sText = sZeit
        self.on_redraw()

    def digital(self, x):
        return "{0:02d}:{1:02d}:{2:02d}"\
                                   .format((x//3600)%24,(x//60)%60,x%60)

class BinaryUhrAnzeige(UhrAnzeige):
    def __init__(self):
        super().__init__()

        self.setToolTip("<pre>  hhhh\nmmmmmm\nssssss<\pre>")

    def redraw(self, iSeconds):
        sZeit = self.binary(iSeconds)
        self.sText = sZeit
        self.on_redraw()

    def binary(self, x):
        return "  {0:04b}\n{1:06b}\n{2:06b}"\
                        .format((x//3600)%24,(x//60)%60,x%60)

class Stoppuhr(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.a = DigitalUhrAnzeige()
        self.a.redraw(0)
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
        self.display = QtGui.QHBoxLayout()
        self.display.addWidget(self.a)
        self.layout = QtGui.QHBoxLayout()
        self.layout.addLayout(self.display)
        self.layout.addWidget(self.btn)
        self.layout.addWidget(self.btn_reset)
        self.layout.addStretch(1)

        self.setLayout(self.layout)

        self.show()

    def on_update(self):
        self.a.redraw(self.iSeconds)

    def setDigital(self):
        self.display.removeWidget(self.a)
        del self.a
        self.a = DigitalUhrAnzeige()
        self.display.addWidget(self.a)
        self.c.redraw.emit()

    def setBinary(self):
        self.display.removeWidget(self.a)
        del self.a
        self.a = BinaryUhrAnzeige()
        self.display.addWidget(self.a)
        self.c.redraw.emit()

    def setAnalog(self):
        self.display.removeWidget(self.a)
        del self.a
        self.a = AnalogUhrAnzeige()
        self.display.addWidget(self.a)
        self.c.redraw.emit()

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
