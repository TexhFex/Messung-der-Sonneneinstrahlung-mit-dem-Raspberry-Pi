###!/usr/bin/env python

import sys
import time
import glob
import os
import csv
import Adafruit_ADS1x15                         #https://learn.adafruit.com/raspberry-pi-analog-to-digital-converters/ads1015-slash-ads1115
import datetime     
import Def
from subprocess import call
from sys import argv
from colorama import Fore, Back, Style

pfad = "/sys/bus/w1/devices/"
sensor_ordner = glob.glob(pfad + "28-0000054884ac")[0]
sensor_daten_pfad = sensor_ordner + "/w1_slave"


address_1 = 0x48
adc = Adafruit_ADS1x15.ADS1015()
bus=1  

error = 0
time.sleep(1.0)
c = 9                                          #ASCII-Wert 9 fuer TABULATOR, meist fuer Exel gebraucht(naechste Spalte).
maxsd = 30
sonneneinstrahlung = 0
sonneneinstrahlungvorher = 1

Zeitkorrekturfaktor = float(10.009090909090)     #TODO: 1.


#Programm Readytime.py:


forim = 60
forih = 24
forid = 30
mvs = 60
hvt = 24
tvm = 30
ii = 0
sti = 0 
aMi = 0
while ii < 20:
    print(" ")              #Clear place
    ii = ii + 1
l = datetime.datetime.now()
dateiname = l.strftime("%d" + "" + "%m" + "" + "%Y" + "_" +  "%H" + "" + "%M" +  "" + "%S")
print(Fore.RED) 
print(Back.GREEN) 
print(Style.DIM)
print("Programm: Wetterstation.py wird ausgefuehrt:")
print(Style.RESET_ALL) 

sleepingtime = 60
anzahlMessungen = 1400

print(Fore.YELLOW)

sleepingtime = int(input("Zeitintervall in [s] der Messungen: "))
sleepingtime = Def.sleepingtimedef(sleepingtime) 

anzahlMessungen = float(input("Anzahl der Messungen: "))
anzahlMessungen = Def.anzahlMessungendef(anzahlMessungen)


maxsd = int(input("Maximale Sonneneinstrahlungsdifferenz (Normal: 20): "))
maxsd = Def.maxsddef(maxsd)

print("")

diad = int(input("Diagnosedaten: "))
diad = Def.diaddef(diad)

print("")

e = datetime.datetime.now()
nowYear = float(e.strftime("%Y"))
nowmonth = int(e.strftime("%m"))
nowday = int(e.strftime("%d"))
nowhour = int(e.strftime("%H"))
nowminute = int(e.strftime("%M"))
nowsecund = int(e.strftime("%S"))
sleepingtimere = sleepingtime + 1
durationminutes = int(round(sleepingtimere * anzahlMessungen / 60))
readyY = float(nowYear)
readyMo = nowmonth
readym = durationminutes + nowminute
readyh = nowhour
readyd = nowday

print(Style.RESET_ALL) 
print("Heute:"),
print(e.strftime(chr(c) + "%d" + "." + "%m" + "." + "%Y" + chr(c) +  "%H" + ":" + "%M" +  ":" + "%S"))
time.sleep(1.0)

#Berechnung ob Schaltjahr

Schaltjahr = int(abs(round(nowYear / 4) - (nowYear / 4)))           #Formel zur Schaltjahrberechnung
if(Schaltjahr > 0):
    if nowmonth in [1,3,5,7,8,10,12]:
         tvm = 31
    if nowmonth in [4,6,9,11]:
         tvm = 30
    if nowmonth in [2]:
         tvm = 29
else:
    if nowmonth in [1,3,5,7,8,10,12]:
        tvm = 31
    if nowmonth in [4,6,9,11]:
        tvm = 30
    if nowmonth in [2]:
        tvm = 28


#Berechnen der Sekunden, Minuten
f1 = datetime.datetime.now()
nowmili1 = float(f1.strftime("%S"))
nowsec1 = float(f1.strftime("%M"))          #1
nowmin1 = float(f1.strftime("%H"))


print(Fore.GREEN) 
print("Berechne Laenge der Messung ...")

print("0%    "),


while forim <= readym:
    if(readym >= mvs):
        readym = readym - mvs
        readyh = readyh + 1

f2 = datetime.datetime.now()
nowmili2 = float(f2.strftime("%S"))
nowsec2 = float(f2.strftime("%M"))
nowmin2 = float(f2.strftime("%H"))
nowmili1m2 = nowmili2 - nowmili1
nowsec1m2 = (nowsec2 - nowsec1)*60
nowmin1m2 = (nowmin2 - nowmin1)* 3600
zrzero = nowmili1m2 + nowsec1m2 + nowmin1m2
print(nowmili1m2 + nowsec1m2 + nowmin1m2),          #"Zeitstoppen" von 1 bis hier
print("Sekunden")   

if(readym == 60):
    readym = readym - mvs
    readyh = readyh + 1

#Berechnen der Stunden
f1 = datetime.datetime.now()
nowmili1 = float(f1.strftime("%S"))         #2
nowsec1 = float(f1.strftime("%M"))
nowmin1 = float(f1.strftime("%H"))
print("97,35% "),

while forih < readyh:
    if(readyh >= hvt):
        readyh = readyh - hvt
        readyd = readyd + 1
f2 = datetime.datetime.now()
nowmili2 = float(f2.strftime("%S"))
nowsec2 = float(f2.strftime("%M"))
nowmin2 = float(f2.strftime("%H"))
nowmili1m2 = nowmili2 - nowmili1
nowsec1m2 = (nowsec2 - nowsec1)*60
nowmin1m2 = (nowmin2 - nowmin1)* 3600
zrone = nowmili1m2 + nowsec1m2 + nowmin1m2
print(nowmili1m2 + nowsec1m2 + nowmin1m2),
print("Sekunden")                               #"Zeitstoppen" von 2 bis hier

#Berechnen der Tage, Monate, Jahre

f1 = datetime.datetime.now()
nowmili1 = float(f1.strftime("%S"))         #3
nowsec1 = float(f1.strftime("%M"))
nowmin1 = float(f1.strftime("%H"))
print("99,65% "),

time.sleep(0.25)
while forid < readyd:
    if(readyd >= tvm):
        readyd = readyd - tvm
        readyMo = readyMo + 1
        if readyMo > 12:
            readyMo = readyMo - 12
            readyY = readyY + 1
            #Sonderrechnung fuer Schaltjahre    
        Schaltjahr = float(abs(round(readyY / 4) - (readyY / 4)))
        if readyMo in [1,3,5,7,8,10,12]:
            tvm = 31
        if readyMo in [4,6,9,11]:
            tvm = 30
        if readyMo in [2]:
            if Schaltjahr > 0:
                tvm = 28
                
            else:
                tvm = 29

f2 = datetime.datetime.now()
nowmili2 = float(f2.strftime("%S"))
nowsec2 = float(f2.strftime("%M"))
nowmin2 = float(f2.strftime("%H"))
nowmili1m2 = nowmili2 - nowmili1
nowsec1m2 = (nowsec2 - nowsec1)*60
nowmin1m2 = (nowmin2 - nowmin1)* 3600
zrtwo = nowmili1m2 + nowsec1m2 + nowmin1m2
print(nowmili1m2 + nowsec1m2 + nowmin1m2),             #"Zeitstoppen" von 3 bis hier
print("Sekunden")
 
print("100%")                
print("Berechnung erfolgreich. (" + str(zrzero + zrone + zrtwo) + " Sekunden)")     #Ausgabe der benoetigten Zeit zum Rechnen(1 + 2 + 3)

print(Style.RESET_ALL) 
time.sleep(0.25)

print(" ")
print("Fertig Um:")
print(str(readyh) + ":" + str(readym))              #Ausgabe der benoetigten Zeit der Messungen
time.sleep(0.25)
print("Am:")
print(str(readyd) + "." + str(readyMo) + "." + str(int(readyY)))
print(Style.RESET_ALL) 

#END
csvname = dateiname + ".csv"
file = file(csvname,'w')
file.write(str('Messung') + chr(c) + str('Datum') + chr(c) + str('Uhrzeit') + chr(c) + str('Watt pro Qm'))
file.write("")

print(" ")
widerstand = 4.7
GAIN = 2/3
spannung = 0
counter=1
errorcounter=1
wattproqm = 1000/0.480
loopi = 0
timei = 1
fehlerzaeler = 0
ydifnorm = sleepingtime 
valuenumbers = int((ydifnorm)/sleepingtime*10)                 #Berechnung der Werte, der Anzahl der Werte und der Schleifen.
schlafzeit = float(sleepingtime / Zeitkorrekturfaktor)
while True:
    
    y = datetime.datetime.now()
    yminuten = y.strftime("%M")
    ysecunden = int(y.strftime("%S")) + (int(yminuten) * 60)
    Sonneneinstrahlungsvalue = [0]*valuenumbers
    while loopi < valuenumbers:
        
        values = [0]*4
        
        for i in range(4):
            values[i] = adc.read_adc(i, gain=GAIN)
        spannung = values[3]*0.003
        stromstaerke = spannung / widerstand
        sonneneinstrahlung = stromstaerke*wattproqm
        error = Def.errorcorrecting(sonneneinstrahlungvorher, sonneneinstrahlung, maxsd)
        if error == 1:
            Sonneneinstrahlungsvalue[loopi] = sonneneinstrahlungvorher
            if diad == 1:
                print("Messungsfehler gefunden")
                print(Sonneneinstrahlungsvalue[loopi])
                fehlerzaeler += 1
        else: 
            Sonneneinstrahlungsvalue[loopi] = sonneneinstrahlung
            sonneneinstrahlungvorher = Sonneneinstrahlungsvalue[loopi]
        loopi += 1
        timei += (sleepingtime / 10)
        time.sleep(schlafzeit)
        yy = datetime.datetime.now()
        yyminuten = yy.strftime("%M")
        yysecunden = int(yy.strftime("%S")) + (int(yyminuten) * 60)
        #print(" | {0:>6} | ".format(*values))
        ydif = yysecunden - ysecunden
     #   print(ydif)
        if diad == 1:
            print(Sonneneinstrahlungsvalue)
        if ydif > ydifnorm :
            loopi = valuenumbers
            print(Fore.RED) 
            print(Back.GREEN) 
            print(Style.DIM)
            print("Time")
            print(Style.RESET_ALL) 
        
        if timei == ydifnorm:
            loopi = ydifnorm
            print(Fore.RED) 
            print(Back.GREEN) 
            print(Style.DIM)
            print("Counter")
            print(Style.RESET_ALL) 
        

    
    loopi = 0
    durchschnittse = sum(Sonneneinstrahlungsvalue) / len(Sonneneinstrahlungsvalue) 
    print(Fore.RED)

    temp = Def.grad_lesen(sensor_daten_pfad)
    print("------------------------|")
    print("Messung:           {0:5.0F}|".format(counter))
    print("W/m2 Durchschnitt: {0:5.0F}|".format(durchschnittse))
    print("Temperatur:         {0:0.1F}|".format(temp))
    print("------------------------|")
    print(Style.RESET_ALL)
    
    if durchschnittse > 2:
        file.write(str('{0:5.0F}: '.format(int(counter))) + chr(c))
        x = datetime.datetime.now()
        file.write(x.strftime("%d" + "." + "%m" + "." + "%Y" + chr(c) +  "%H" + ":" + "%M" +  ":" + "%S" + chr(c)))
        file.write(str('{0:5.0F}'.format(int(durchschnittse))))
        file.write(chr(c) + str('{0:0.1F}'.format(temp)))
        file.write("\n")


    counter = counter + 1
    if counter > anzahlMessungen:
        x = datetime.datetime.now()
        print("------------------------|")
        print(fehlerzaeler)
        print("Ende der Messung:       |")
        print("Uhrzeit:                |")
        print("Vorhergesagt       Jetzt|")
        print(str(readyh) + ":" + str(readym) +  chr(c)  + chr(c)), 
        print(x.strftime("%H" + ":" + "%M" +  ":" + "%S" + "|" + chr(c)))
        print(str(readyd) + "." + str(readyMo) + "." + str(int(readyY)) + "    "), 
        print(x.strftime("%d" + "." + "%m" + "." + "%Y" + "|"))
        print(Fore.RED) 
        print(Back.GREEN) 
        print(Style.DIM)
        print("Coded by Felix Knoll")
        print(Style.RESET_ALL) 
        time.sleep(1.0)
        sys.exit(0)

file.close()        


#TODO:
#1. Zeitkorrekturfaktor messen und einbauen. OK ~ bei 22h Messung 2 min zu kurz(Berechnung) durch Einlesen der Spannung. 
#
#