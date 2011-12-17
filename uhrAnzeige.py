#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
from PyQt4 import QtGui, QtCore

class UhrAnzeige(QtGui.QWidget):
    def __init__(self):
        super().__init__()

        self.setTicken(False)
        self.setRegenbogen(False)

        self.__iSeconds = 0

        self.setMinimumSize(100,100)

        self.colorDict = {"bg"   : QtGui.QColor(255, 255, 255),
                          "s"    : QtGui.QColor(255,   0,   0),
                          "m"    : QtGui.QColor(  0,   0,   0),
                          "h"    : QtGui.QColor(  0,   0,   0),
                          "rand" : QtGui.QColor(  0,   0,   0),
                          "text" : QtGui.QColor(255, 255, 255)}

        self.setColor(self.colorDict)

        self.show()

    def redraw(self, iSeconds):
        self.__iSeconds = iSeconds
        if self.__pRegenbogen:
            self.__changeColorRegenbogen(iSeconds)
        self.on_redraw()

    def on_redraw(self):
        self.update()

    def getColor(self):
        return self.colorDict

    def setColor(self, colors):
        #inititalisisiere Farben
        self.__bgColor   = colors["bg"]
        self.__hColor    = colors["h"]
        self.__mColor    = colors["m"]
        self.__sColor    = colors["s"]
        self.__randColor = colors["rand"]
        self.__textColor = colors["text"]

    def __changeColorRegenbogen(self, x):
        now = self.colorDict
        for n in ["h","m","s","text"]:
            r = now[n].red()
            g = now[n].green()
            b = now[n].blue()
            r,g,b = self.__regenbogenNextColor(r, g, b, 6)
            now[n].setRed(r)
            now[n].setGreen(g)
            now[n].setBlue(b)
        self.setColor(now)

    def __regenbogenNextColor(self, r, g, b, geschwindigkeit = 1):
        if   r == 255 and g  < 255 and b == 0:
            g += 1 * geschwindigkeit
        elif g == 255 and b  < 255 and r == 0:
            b += 1 * geschwindigkeit
        elif b == 255 and r  < 255 and g == 0:
            r += 1 * geschwindigkeit
        elif r <= 255 and g == 255 and b == 0:
            r -= 1 * geschwindigkeit
        elif g <= 255 and b == 255 and r == 0:
            g -= 1 * geschwindigkeit
        elif b <= 255 and r == 255 and g == 0:
            b -= 1 * geschwindigkeit
        else:
            r = 255
            g = 0
            b = 0

        [r,g,b]=[255 if i>255-geschwindigkeit else 0 if i < -1+geschwindigkeit else i%256 for i in [r,g,b]]

        return r, g, b

    def setTicken(self, b):
        """
            Schaltet ein Property, dass einstellt, ob der Minuten/Stunden-
            Zeiger sich kotinuierlich oder diskret bewegen.

            b: boolean
        """
        self.__pTicken = b
        self.on_redraw()

    def setRegenbogen(self, b):
        """
            Schaltet ein Property, dass einstellt, ob der Minuten/Stunden-
            Zeiger ihre Farbe mit der Zeit ändern sollen.

            b: boolean
        """
        self.__pRegenbogen = b
        try:
            self.colorDict["h"]    = QtGui.QColor(255,   0,   0)
            self.colorDict["m"]    = QtGui.QColor(  0, 255,   0)
            self.colorDict["s"]    = QtGui.QColor(  0,   0, 255)
            self.colorDict["text"] = QtGui.QColor(255,   0,   0)
        except:
            pass
        self.on_redraw()

    def paintEvent(self, event):
        self.__size = min(self.height(), self.width())
        self.__margin = self.__size / 100
        self.__bereich = QtCore.QRect(self.__margin, self.__margin, self.__size - 2*self.__margin, self.__size - 2*self.__margin)

        paint = QtGui.QPainter(self)
        paint.setPen(self.__textColor)
        paint.setFont(QtGui.QFont('Monospace', self.__size/7))
        paint.setRenderHint(QtGui.QPainter.Antialiasing)
        paint.eraseRect(self.geometry())
        self.__drawZeit(paint, event)

    def __drawZeit(self, paint, event):
        """
            Überprüft das pStyle Property, welcher Style geählt ist und
            startet die entsprechende Zeichenfunktion
        """
        if self.__pStyle == self.styles["analogArc"]:
            self.__arcStyle(paint, event)
        elif self.__pStyle == self.styles["analogBahnhof"]:
            self.__bahnhofStyle(paint, event)
        elif self.__pStyle == self.styles["digital"]:
            self.__digitalStyle(paint, event)
        elif self.__pStyle == self.styles["binary"]:
            self.__binaryStyle(paint, event)
        else:
            raise AttributeError

    def __drawBackground(self, paint, event):
        """
            Überprüft das pBGStyle Property, welcher Style gewählt ist und
            startet die entsprechende Zeichenfunktion
        """
        if self.__pBGStyle == self.bgStyles["plain"]:
            self.__bgPlainStyle(paint, event)
        elif self.__pBGStyle == self.bgStyles["zahnrad"]:
            self.__bgZahnradStyle(paint, event)
        elif self.__pBGStyle == self.bgStyles["sonne"]:
            self.__bgSonneStyle(paint, event)
        else:
            raise AttributeError

    def setDigital(self):
        self.setToolTip("hh:mm:ss")
        self.__pStyle = self.styles["digital"]
        self.on_redraw()

    def setBinary(self):
        self.setToolTip("<pre>  hhhh\nmmmmmm\nssssss<\pre>")
        self.__pStyle = self.styles["binary"]
        self.on_redraw()

    def setAnalogArc(self):
        self.__pStyle = self.styles["analogArc"]
        self.__setAnalogTooltip()
        self.on_redraw()

    def setAnalogBahnhof(self):
        self.__pStyle = self.styles["analogBahnhof"]
        self.__setAnalogTooltip()
        self.on_redraw()

    def __setAnalogTooltip(self):
        self.setToolTip("Die Winkel der Zeiger:\n\
                        rot*60/2Pi   -> Sekunden\n\
                        klein*60/2Pi -> Minuten\n\
                        dick*24/2Pi  -> Stunden")

    def setBGPlain(self):
        self.__pBGStyle = self.bgStyles["plain"]
        self.on_redraw()

    def setBGZahnrad(self):
        self.__pBGStyle = self.bgStyles["zahnrad"]
        self.on_redraw()

    def setBGSonne(self):
        self.__pBGStyle = self.bgStyles["sonne"]
        self.on_redraw()

    def __analog(self, x):
        """
            Nimmt Sekunden engegen und gibt ein Tupel der Winkel aus:
            Erst Stunden, dann Mintuen, dann Sekunden Winkel
            Dabei sind die Winkel in Winkelmaß angegeben
        """
        if self.__pTicken:
            s = (x%60)/60. * 360
            m = ((x//60)%60)/60. * 360
            h = ((x//3600)%12)/12. * 360
            return h,m,s
        else:
            s = (x%60)/60. * 360
            m = ((x/60.)%60)/60. * 360
            h = ((x/3600.)%12)/12. * 360
            return h,m,s

    def __digital(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im Digitaluhr-
            format zurück.
        """
        return "{0:02d}:{1:02d}:{2:02d}"\
                                   .format((x//3600)%24,(x//60)%60,x%60)

    def __binary(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im Binäruhr-
            format zurück.
        """
        return "\n {0:05b}\n{1:06b}\n{2:06b}\n"\
                                   .format((x//3600)%24,(x//60)%60,x%60)

    def __digitalStyle(self, paint, event):
        """
            Zeichenfunktion für Digitaluhr
        """
        sZeit = self.__digital(self.__iSeconds)
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, sZeit)

    def __binaryStyle(self, paint, event):
        """
            Zeichenfunktion für Binäruhr
        """
        sZeit = self.__binary(self.__iSeconds)
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, sZeit)

    def __bahnhofStyle(self, paint, event):
        """
            Zeichenfunktion für Bahnhofsuhr
        """
        self.__drawBackground(paint, event)

        h,m,s = self.__analog(self.__iSeconds)

        mitte = QtCore.QPointF(self.__bereich.center())
        lange = self.__size/2 - self.__margin
        nullUhr = QtCore.QPointF(lange,0)

        stiftS = QtGui.QPen()
        stiftM = QtGui.QPen()
        stiftH = QtGui.QPen()

        stiftS.setColor(self.__sColor)
        stiftM.setColor(self.__mColor)
        stiftH.setColor(self.__hColor)

        stiftS.setWidthF(self.__size/150)
        stiftM.setWidthF(self.__size/150)
        stiftH.setWidthF(self.__size/75)

        sekundenZeiger1 = QtCore.QLineF(mitte, nullUhr)
        sekundenZeiger1.setAngle(-s + 90)
        dx = sekundenZeiger1.dx() * 0.8
        dy = sekundenZeiger1.dy() * 0.8
        radius = self.__size/30
        x = sekundenZeiger1.length()
        sekundenZeiger1.setLength(0.8 * x - radius)

        sekundenZeiger2 = QtCore.QLineF(mitte, nullUhr)
        sekundenZeiger2.setAngle(-s + 90)
        p1 = sekundenZeiger2.p2()
        p2 = sekundenZeiger2.p1()
        sekundenZeiger2.setP1(p1)
        sekundenZeiger2.setP2(p2)
        sekundenZeiger2.setLength(0.2 * x - radius)

        minutenZeiger = QtCore.QLineF(mitte, nullUhr)
        minutenZeiger.setAngle(-m + 90)
        minutenZeiger.setLength(0.9 * minutenZeiger.length())

        stundenZeiger = QtCore.QLineF(mitte, nullUhr)
        stundenZeiger.setAngle(-h + 90)
        stundenZeiger.setLength(0.6 * stundenZeiger.length())

        paint.setPen(stiftH)
        paint.drawLine(stundenZeiger)

        paint.setPen(stiftM)
        paint.drawLine(minutenZeiger)

        paint.setPen(stiftS)
        paint.drawLine(sekundenZeiger1)
        paint.drawLine(sekundenZeiger2)

        paint.drawArc(self.__size/2+(dx-radius), self.__size/2+(dy-radius),\
                        2*radius, 2*radius, 0, 16 * 360)

    def __arcStyle(self, paint, event):
        """
            Zeichenfunktion für minimalistische "Winkeluhr"
        """
        self.__drawBackground(paint, event)

        h,m,s = self.__analog(self.__iSeconds)
        s *= 16
        m *= 16
        h *= 16

        startSAngle = - s -16 + 90*16
        spanSAngle =  32

        startMAngle = - m - 32 + 90*16
        spanMAngle =  64

        startHAngle = - h - 32 + 90*16
        spanHAngle =  64

        paint.setPen(self.__hColor)
        paint.setBrush(self.__hColor)
        paint.drawPie(  self.__size/6, self.__size/6,\
                        self.__size*2/3, self.__size*2/3,\
                        startHAngle, spanHAngle)

        paint.setPen(self.__mColor)
        paint.setBrush(self.__mColor)
        paint.drawPie(self.__bereich, startMAngle, spanMAngle)

        paint.setPen(self.__sColor)
        paint.setBrush(self.__sColor)
        paint.drawPie(self.__bereich, startSAngle, spanSAngle)

    def __bgPlainStyle(self, paint, event):
        stiftR = QtGui.QPen()
        stiftR.setColor(self.__randColor)
        stiftR.setWidthF(self.__size/75)

        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))

        paint.setPen(stiftR)
        paint.setBrush(self.__bgColor)
        paint.drawChord(self.__bereich, 0, 16 * 360)

    def __bgZahnradStyle(self, paint, event):
        pass

    def __bgSonneStyle(self, paint, event):
        pass
