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

    def setTime(self, x):
        self.iSeconds = x

    def startUhr(self):
        self.timer.start(1000)

    def stopUhr(self):
        self.timer.stop()

    #~ def on_update(self):
        #~ self.update()
        #~ pass

    def on_update(self):
        self.a.redraw(self.iSeconds)

    def setDigital(self):
        self.a.__del__()
        self.display.removeWidget(self.a)
        del self.a
        self.a = DigitalUhrAnzeige()
        self.display.addWidget(self.a)
        self.c.redraw.emit()

    def setBinary(self):
        self.a.__del__()
        self.display.removeWidget(self.a)
        del self.a
        self.a = BinaryUhrAnzeige()
        self.display.addWidget(self.a)
        self.c.redraw.emit()

    def setAnalog(self):
        self.a.__del__()
        self.display.removeWidget(self.a)
        del self.a
        self.a = AnalogUhrAnzeige()
        self.display.addWidget(self.a)
        self.c.redraw.emit()

class UhrAnzeige(Uhr, QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.bDestroy = False

        self.setMinimumSize(100,100)

        self.show()

    def __del__(self):
        self.bDestroy = True
        self.update()

    def on_redraw(self):
        self.update()

    def paintEvent(self, event):
        size = min(self.height(), self.width())
        self.resize(size,size)

        paint = QtGui.QPainter(self)
        paint.setPen(QtGui.QColor(255, 255, 255))
        paint.setFont(QtGui.QFont('Monospace'))
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        if self.bDestroy:
            paint.eraseRect(self.geometry())
        else:
            self.drawZeit(paint, event)

    def drawZeit(self, paint, event):
        pass

class AnalogUhrAnzeige(UhrAnzeige):
    # TODO: drehende Zahnräder hinter Loch in Uhrblatt

    def __init__(self):
        super().__init__()

        self.setToolTip("Die Winkel der Zeiger:\n\
                        rot*60/2Pi   -> Sekunden\n\
                        klein*60/2Pi -> Minuten\n\
                        dick*24/2Pi  -> Stunden")

        self.styles = {"arc":0}
        self.pStyle = self.styles["arc"]

    def redraw(self, iSeconds):
        self.iSeconds = iSeconds
        # TODO:
        self.on_redraw()

    def drawZeit(self, paint, event):
        if self.pStyle == self.styles["arc"]:
            self.arcStyle(paint, event)
        #~ elif

    def arcStyle(self, paint, event):
        h,m,s = self.analog(self.iSeconds)

        bgColor = QtGui.QColor(255, 255, 255)

        startSAngle = - s -16 + 90*16
        spanSAngle =  32
        zeigerSColor = QtGui.QColor(255, 0, 0)

        startMAngle = - m - 32 + 90*16
        spanMAngle =  64
        zeigerMColor = QtGui.QColor(30, 30, 30)

        startHAngle = - h - 32 + 90*16
        spanHAngle =  64
        zeigerHColor = QtGui.QColor(0, 0, 0)

        breit = self.width()
        hoch  = self.height()

        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))

        paint.setPen(bgColor)
        paint.setBrush(bgColor)
        paint.drawPie(0,0, breit, hoch, 0, 16 * 360)

        paint.setPen(zeigerHColor)
        paint.setBrush(zeigerHColor)
        paint.drawPie(breit/6, hoch/6, breit*2/3, hoch*2/3, startHAngle, spanHAngle)

        paint.setPen(zeigerMColor)
        paint.setBrush(zeigerMColor)
        paint.drawPie(0,0, breit, hoch, startMAngle, spanMAngle)

        paint.setPen(zeigerSColor)
        paint.setBrush(zeigerSColor)
        paint.drawPie(0, 0, breit, hoch, startSAngle, spanSAngle)

    def analog(self, x):
        """
            Nimmt Sekunden engegen und gibt ein Tupel der Winkel aus:
            Erst Stunden, dann Mintuen, dann Sekunden Winkel
            Dabei sind die Winkel in 16tel Winkelmaß angegeben
        """
        s = (x%60)/60. * 360 *16
        m = ((x/60.)%60)/60. * 360 *16
        h = ((x/3600.)%12)/12. * 360 *16
        return h,m,s

class DigitalUhrAnzeige(UhrAnzeige):
    def __init__(self):
        super().__init__()

        self.setToolTip("hh:mm:ss")

    def redraw(self, iSeconds):
        sZeit = self.digital(iSeconds)
        self.sText = sZeit
        self.on_redraw()

    def drawZeit(self, paint, event):
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, self.sText)

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

    def drawZeit(self, paint, event):
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, self.sText)

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

    def uhr_toggle(self):
        if self.btn.isChecked():
            self.startUhr()
            self.btn.setText("Stopp!")
            self.btn_reset.setDisabled(True)
        else:
            self.stopUhr()
            self.btn.setText("Start!")
            self.btn_reset.setDisabled(False)

class Uhrzeit(Uhr, QtGui.QWidget):
    def __init__(self):
        import time
        super().__init__()

        self.a = DigitalUhrAnzeige()
        self.a.redraw(0)
        self.startUhr()
        now=time.localtime()
        now = now[3]*3600+now[4]*60+now[5]
        print(now)
        self.setTime(now)
        self.initUI()

    def initUI(self):
        self.setToolTip('Dies ist eine Uhr')

        # Layout
        self.display = QtGui.QHBoxLayout()
        self.display.addWidget(self.a)
        self.setLayout(self.display)

        self.show()

class UhrWindow(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # Fenstereigenschaften
        self.center()
        self.setWindowTitle('Stoppuhr')
        self.setWindowIcon(QtGui.QIcon('icon.png'))

        self.setUhrzeit()

        self.setCentralWidget(self.disp)

        # Menüeinträge
        iconBinary = QtGui.QIcon('binary.png')
        setBinaryAction = QtGui.QAction(iconBinary, '&Binary', self)
        setBinaryAction.setShortcut('b')
        setBinaryAction.setStatusTip('Binär Uhr')
        setBinaryAction.triggered.connect(self.disp.setBinary)
        iconDigital = QtGui.QIcon('digital.png')
        setDigitalAction = QtGui.QAction(iconDigital, '&Digital', self)
        setDigitalAction.setShortcut('d')
        setDigitalAction.setStatusTip('Digital Uhr')
        setDigitalAction.triggered.connect(self.disp.setDigital)
        iconAnalog = QtGui.QIcon('analog.png')
        setAnalogAction = QtGui.QAction(iconAnalog, '&Analog', self)
        setAnalogAction.setShortcut('a')
        setAnalogAction.setStatusTip('Analoge Uhr')
        setAnalogAction.triggered.connect(self.disp.setAnalog)

        iconStoppuhr = QtGui.QIcon('stoppuhr.png')
        setStoppuhrAction = QtGui.QAction(iconAnalog, '&Stoppuhr', self)
        setStoppuhrAction.setShortcut('s')
        setStoppuhrAction.setStatusTip('Stoppuhr')
        setStoppuhrAction.triggered.connect(self.setStoppuhr)

        iconUhrzeit = QtGui.QIcon('uhrzeit.png')
        setUhrzeitAction = QtGui.QAction(iconAnalog, '&Uhr', self)
        setUhrzeitAction.setShortcut('u')
        setUhrzeitAction.setStatusTip('Uhrzeit')
        setUhrzeitAction.triggered.connect(self.setUhrzeit)

        menubar = self.menuBar()
        menuFkt = menubar.addMenu('Funktion')
        menuDar = menubar.addMenu('Darstellung')
        menuDar.addAction(setDigitalAction)
        menuDar.addAction(setBinaryAction)
        menuDar.addAction(setAnalogAction)
        menuFkt.addAction(setUhrzeitAction)
        menuFkt.addAction(setStoppuhrAction)

        self.show()

    def center(self):
        qr = self.frameGeometry()
        cp = QtGui.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def setStoppuhr(self):
        #~ try:
            #~ del self.disp
        #~ except:
            #~ pass
        self = Stoppuhr()
        self.setCentralWidget(self.disp)

    def setUhrzeit(self):
        #~ try:
            #~ del self.disp
        #~ except:
            #~ pass
        self.disp = Uhrzeit()
        #~ self.setCentralWidget(self.disp)

def main():
    app = QtGui.QApplication(sys.argv)
    ex = UhrWindow()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
