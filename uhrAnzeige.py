#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import time

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

        self.setFaktor("si")

        self.show()

    def setFaktor(self, t):
        if t == "si":
            self.halberTagAufZiffernblatt = True
            self.spm = 60
            self.mph = 60
            self.sph = 3600
            self.hpd = 24
            self.sps = 1
        elif t == "dez":
            self.halberTagAufZiffernblatt = False
            self.spm = 100
            self.mph = 100
            self.sph = 10000
            self.hpd = 10
            self.sps = 1/0.864

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
        elif self.__pStyle == self.styles["unix"]:
            self.__unixStyle(paint, event)
        elif self.__pStyle == self.styles["sternzeit"]:
            self.__sternzeitStyle(paint, event)
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
        elif self.__pBGStyle == self.bgStyles["kein"]:
            self.__bgKeinStyle(paint, event)
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

    def setSternzeit(self):
        self.setToolTip("Sternzeit nach StarTrek")
        self.__pStyle = self.styles["sternzeit"]
        self.__sternzeitSekunde = 1000/365.25/24/60/60
        self.__sternzeitRef = time.mktime(time.strptime("01.01.2323", "%d.%m.%Y"))
        self.__sternzeitNow = time.mktime(time.localtime()) - self.__iSeconds - self.__sternzeitRef
        self.on_redraw()

    def setUnix(self):
        self.setToolTip("Sekunden seit der Epoche")
        self.__pStyle = self.styles["unix"]
        self.__unixNow = time.mktime(time.localtime()) - self.__iSeconds
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
        self.__randColor = QtGui.QColor(255, 255,   0)
        self.on_redraw()

    def setBGKein(self):
        self.__pBGStyle = self.bgStyles["kein"]
        self.on_redraw()

    def __analog(self, x):
        """
            Nimmt Sekunden engegen und gibt ein Tupel der Winkel aus:
            Erst Stunden, dann Mintuen, dann Sekunden Winkel
            Dabei sind die Winkel in Winkelmaß angegeben
        """
        if self.halberTagAufZiffernblatt:
            p = 2
        else:
            p = 1
        x = round(x*self.sps)
        if self.__pTicken:
            s = (x%self.spm)/float(self.spm) * 360
            m = ((x//self.spm)%self.mph)/float(self.mph) * 360
            h = ((x//self.sph)%(self.hpd/p))/float(self.hpd/p) * 360
            return h,m,s
        else:
            s = (x%self.spm)/float(self.spm) * 360
            m = ((x/float(self.spm))%self.mph)/float(self.mph) * 360
            h = ((x/float(self.sph))%(self.hpd/p))/float(self.hpd/p) * 360
            return h,m,s

    def __digital(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im Digitaluhr-
            format zurück.
        """
        x = round(x*self.sps)
        return "{0:02d}:{1:02d}:{2:02d}"\
       .format((x//self.sph)%self.hpd,(x//self.spm)%self.mph,x%self.spm)

    def __binary(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im Binäruhr-
            format zurück.
        """
        x = round(x*self.sps)
        return "\n {0:05b}\n{1:06b}\n{2:06b}\n"\
       .format((x//self.sph)%self.hpd,(x//self.spm)%self.mph,x%self.spm)

    def __unix(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im Unix-
            format zurück.
        """
        x = x + self.__unixNow
        return "{0:010d}".format(int(x))

    def __sternzeit(self, x):
        """
            Nimmt Sekunden entgegen und gibt einen String im StarTrek-
            Sternzeit-format zurück. 1 Jahr = 1000 Sternzeiteinheiten
            Sternzeit 0 = 01.01.2323 0:00
        """
        x = x + self.__sternzeitNow
        return "{0: 5.2f}".format(x*self.__sternzeitSekunde)

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

    def __unixStyle(self, paint, event):
        """
            Zeichenfunktion für Unixzeitstempel
        """
        sZeit = self.__unix(self.__iSeconds)
        paint.drawText(event.rect(), QtCore.Qt.AlignCenter, sZeit)

    def __sternzeitStyle(self, paint, event):
        """
            Zeichenfunktion für StarTrek Sternzeit
        """
        sZeit = self.__sternzeit(self.__iSeconds)
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
        i = self.__iSeconds
        laenge1 = self.__size/12
        x1 = self.__size/7*5 - self.__margin
        y1 = self.__size/7*5 - self.__margin
        dx1 = laenge1
        dy1 = laenge1
        boundingBox1 = QtCore.QRect(x1, y1, dx1, dy1)

        laenge2 = laenge1*1.5
        x2 = x1 + laenge1*33/36
        y2 = y1 - laenge1*33/36
        dx2 = laenge2
        dy2 = laenge2
        boundingBox2 = QtCore.QRect(x2, y2, dx2, dy2)

        startAngle = - i*16*66
        spanAngle =  32

        stiftR = QtGui.QPen()
        stiftR.setColor(self.__randColor)
        stiftR.setWidthF(self.__size/60)

        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))

        paint.setPen(stiftR)
        paint.setBrush(self.__bgColor)
        paint.drawChord(self.__bereich, 0, 16 * 360)

        anz = 12

        for phi in [i*360/anz*16+startAngle for i in range(anz+1)]:
            paint.drawPie(boundingBox1, phi, spanAngle)

        for phi in [-i*360/anz*16-startAngle+16*180/anz for i in range(anz+1)]:
            paint.drawPie(boundingBox2, phi, spanAngle)

    def __bgSonneStyle(self, paint, event):
        i = self.__iSeconds
        radius = self.__size/6*2
        mitte = QtCore.QPointF(self.__bereich.center())
        x = mitte.x() - radius
        y = mitte.y() - radius
        dx = radius * 2
        dy = radius * 2
        boundingBox = QtCore.QRect(x, y, dx, dy)
        boundingBox2= QtCore.QRect(x+x/2+dx/5/2, y+dy/5/2, dx*4/5, dy*4/5)

        stiftR = QtGui.QPen()
        stiftR.setColor(self.__randColor)
        stiftR.setWidthF(self.__size/1000)

        paint.setBrush(QtGui.QBrush(QtCore.Qt.SolidPattern))

        paint.setPen(stiftR)
        paint.setBrush(self.__bgColor)
        paint.drawChord(self.__bereich, 0, 16 * 360)

        tageszeit = self.__iSeconds / 3600 % 24
        if tageszeit > 6 and tageszeit < 18:
        # Sonne
            stiftR.setWidthF(self.__size/15)
            anz = 64
            startAngle = self.__iSeconds*65%128
            spanAngle =  32
            paint.setBrush(self.__randColor)
            for phi in [i*360/anz*16+startAngle for i in range(anz+1)]:
                paint.drawPie(boundingBox, phi, spanAngle)
        else:
        #Mond
            paint.setBrush(self.__randColor)
            paint.drawChord(boundingBox, 0, 16 * 360)

            stiftR.setColor(self.__bgColor)
            paint.setPen(stiftR)
            paint.setBrush(self.__bgColor)
            paint.drawChord(boundingBox2, 0, 16 * 360)

    def __bgKeinStyle(self, paint, event):
        pass
