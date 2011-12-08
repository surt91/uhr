#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from PyQt4 import QtGui, QtCore

class UhrAnzeige(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.setTicken(False)

        self.iSeconds = 0

        self.styles = { "binary":0,    "digital":1,
                        "analogArc":2, "analogBahnhof":3}

        self.setMinimumSize(100,100)

        self.show()

    def redraw(self, iSeconds):
        self.iSeconds = iSeconds
        self.on_redraw()

    def on_redraw(self):
        self.update()

    def setTicken(self, b):
        """
            Schaltet ein Property, dass einstellt, ob der Minuten/Stunden-
            Zeiger sich kotinuierlich oder diskret bewegen.

            b: boolean
        """
        self.pTicken = b
        self.on_redraw()

    def paintEvent(self, event):
        self.size = min(self.height(), self.width())
        self.margin = self.size / 100
        self.bereich = QtCore.QRect(self.margin, self.margin, self.size - 2*self.margin, self.size - 2*self.margin)

        paint = QtGui.QPainter(self)
        paint.setPen(QtGui.QColor(255, 255, 255))
        paint.setFont(QtGui.QFont('Monospace', self.size/7))
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.eraseRect(self.geometry())
        self.drawZeit(paint, event)

    def drawZeit(self, paint, event):
        """
            Überprüft das pStyle Property, welcher Style geählt ist und
            startet die entsprechende Zeichenfunktion
        """
        if self.pStyle == self.styles["analogArc"]:
            self.arcStyle(paint, event)
        elif self.pStyle == self.styles["analogBahnhof"]:
            self.bahnhofStyle(paint, event)
        elif self.pStyle == self.styles["digital"]:
            self.digitalStyle(paint, event)
        elif self.pStyle == self.styles["binary"]:
            self.binaryStyle(paint, event)
        else:
            raise AttributeError

    def setDigital(self):
        self.setToolTip("hh:mm:ss")
        self.pStyle = self.styles["digital"]
        self.on_redraw()

    def setBinary(self):
        self.setToolTip("<pre>  hhhh\nmmmmmm\nssssss<\pre>")
        self.pStyle = self.styles["binary"]
        self.on_redraw()

    def setAnalogArc(self):
        self.pStyle = self.styles["analogArc"]
        self.setAnalog()
        self.on_redraw()

    def setAnalogBahnhof(self):
        self.pStyle = self.styles["analogBahnhof"]
        self.setAnalog()
        self.on_redraw()

    def setAnalog(self):
        self.setToolTip("Die Winkel der Zeiger:\n\
                        rot*60/2Pi   -> Sekunden\n\
                        klein*60/2Pi -> Minuten\n\
                        dick*24/2Pi  -> Stunden")


    def analog(self, x):
        """
            Nimmt Sekunden engegen und gibt ein Tupel der Winkel aus:
            Erst Stunden, dann Mintuen, dann Sekunden Winkel
            Dabei sind die Winkel in Winkelmaß angegeben
        """
        if self.pTicken:
            s = (x%60)/60. * 360
            m = ((x//60)%60)/60. * 360
            h = ((x//3600)%12)/12. * 360
            return h,m,s
        else:
            s = (x%60)/60. * 360
            m = ((x/60.)%60)/60. * 360
            h = ((x/3600.)%12)/12. * 360
            return h,m,s

    def digital(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im Digitaluhr-
            format zurück.
        """
        return "{0:02d}:{1:02d}:{2:02d}"\
                                   .format((x//3600)%24,(x//60)%60,x%60)

    def binary(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im Binäruhr-
            format zurück.
        """
        return "\n {0:05b}\n{1:06b}\n{2:06b}\n"\
                                   .format((x//3600)%24,(x//60)%60,x%60)

    def digitalStyle(self, paint, event):
        """
            Zeichenfunktion für Digitaluhr
        """
        sZeit = self.digital(self.iSeconds)
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, sZeit)

    def binaryStyle(self, paint, event):
        """
            Zeichenfunktion für Binäruhr
        """
        sZeit = self.binary(self.iSeconds)
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, sZeit)

    def bahnhofStyle(self, paint, event):
        """
            Zeichenfunktion für Bahnhofsuhr
        """
        h,m,s = self.analog(self.iSeconds)

        mitte = QtCore.QPointF(self.bereich.center())
        lange = self.size/2 - self.margin
        nullUhr = QtCore.QPointF(lange,0)

        stiftB = QtGui.QPen()
        stiftS = QtGui.QPen()
        stiftM = QtGui.QPen()
        stiftH = QtGui.QPen()

        bgColor = QtGui.QColor(255, 255, 255)
        zeigerSColor = QtGui.QColor(255, 0, 0)
        zeigerMColor = QtGui.QColor(0, 0, 0)
        zeigerHColor = QtGui.QColor(0, 0, 0)

        stiftB.setColor(zeigerHColor)
        stiftS.setColor(zeigerSColor)
        stiftM.setColor(zeigerMColor)
        stiftH.setColor(zeigerHColor)
        stiftH.setJoinStyle(0x40)

        stiftB.setWidthF(self.size/75)
        stiftS.setWidthF(self.size/150)
        stiftM.setWidthF(self.size/150)
        stiftH.setWidthF(self.size/75)

        sekundenZeiger = QtCore.QLineF(mitte, nullUhr)
        sekundenZeiger.setAngle(-s + 90)
        x = sekundenZeiger.length()
        sekundenZeiger.setLength(0.8 * x)
        dx = sekundenZeiger.dx()
        dy = sekundenZeiger.dy()
        sekundenZeiger.setLength(x)

        minutenZeiger = QtCore.QLineF(mitte, nullUhr)
        minutenZeiger.setAngle(-m + 90)
        minutenZeiger.setLength(0.9 * minutenZeiger.length())

        stundenZeiger = QtCore.QLineF(mitte, nullUhr)
        stundenZeiger.setAngle(-h + 90)
        stundenZeiger.setLength(0.6 * stundenZeiger.length())

        paint.setPen(stiftB)
        paint.setBrush(bgColor)
        paint.drawChord(self.bereich, 0, 16 * 360)

        paint.setPen(stiftH)
        paint.drawLine(stundenZeiger)

        paint.setPen(stiftM)
        paint.drawLine(minutenZeiger)

        paint.setPen(stiftS)
        paint.drawLine(sekundenZeiger)
        radius = self.size/30
        paint.drawChord(self.size/2+(dx-radius), self.size/2+(dy-radius), 2*radius, 2*radius, 0, 16 * 360)

    def arcStyle(self, paint, event):
        """
            Zeichenfunktion für minimalistische "Winkeluhr"
        """
        h,m,s = self.analog(self.iSeconds)
        s *= 16
        m *= 16
        h *= 16

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

        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))
        stiftB = QtGui.QPen()
        stiftB.setColor(zeigerHColor)
        stiftB.setWidthF(self.size/120)

        paint.setPen(stiftB)
        paint.setBrush(bgColor)
        paint.drawChord(self.bereich, 0, 16 * 360)

        paint.setPen(zeigerHColor)
        paint.setBrush(zeigerHColor)
        paint.drawPie(self.size/6, self.size/6, self.size*2/3, self.size*2/3, startHAngle, spanHAngle)

        paint.setPen(zeigerMColor)
        paint.setBrush(zeigerMColor)
        paint.drawPie(self.bereich, startMAngle, spanMAngle)

        paint.setPen(zeigerSColor)
        paint.setBrush(zeigerSColor)
        paint.drawPie(self.bereich, startSAngle, spanSAngle)
