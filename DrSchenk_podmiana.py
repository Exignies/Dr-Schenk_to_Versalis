#!/usr/bin/env python
#coding:utf-8

import ezdxf
import os
#import numpy as np
import math




def wsptargets (ms):
    # Wyciąganie wsp targetów
    vector = []
    for i in ms.query('TEXT'):
        vector.append(i.dxf.insert)
    v1 = vector[0]
    v2 = vector[1]
    print(v1)
    print(v2)
    return v1, v2


def abvector(Dv1, Dv2, Lv1, Lv2):
    # oblicza przeciwprostokątną a i przyprostokątna b kąta

    # Dv
    if Dv1[1] >= Dv2[1]: # czy nie zamieniono miejscami punktów
        aD = Dv1[1] - Dv2[1]
        bD = Dv1[0] - Dv2[0]
        print("dv1(y) >= dv2(y) Y większe OK")
        print(aD)
        print(bD)
    else:
        aD = Dv2[1] - Dv1[1]
        bD = Dv2[0] - Dv1[0]
        print("dv1(y) < dv2(y) NOK")
        print(aD)
        print(bD)        

    katD = abs(aD)/abs(bD)
    print("tangens %s" %(katD))
    katD = math.atan(katD)
    katD= math.degrees(katD)

    if Dv1[0] > Dv2[0]:
        katD = 180 - katD
        print("db X1 > X2,  X2 mniejszy, 180 - kat")

    
    print("deg katd: %s" %(katD) )

    # Lv
    if Lv1[1] >= Lv2[1]: # czy nie zamieniono miejscami punktów
        aL = Lv1[1] - Lv2[1]
        bL = Lv1[0] - Lv2[0]
        print("lv1(y) >= lv2(y) Y większe OK") 
    else:
        aL = Lv2[1] - Lv1[1]
        bL = Lv2[0] - Lv1[0]
        print("lv1(y) < lv2(y) NOK")

    katL = abs(aL)/abs(bL)
    print("tangens %s" %(katL))
    katL = math.atan(katL)
    katL= math.degrees(katL)

    if Lv1[0] > Lv2[0]:
        katL = 180 - katL
        print("bL X1 > X2,  X2 mniejszy, 180 - kat")
    
    print("deg katL: %s" %(katL) )

    # obliczanie roznicy w katach
    kat = katD - katL
    """"
    if katD >= katL:
        kat = -(katD - katL)
        print("DODATNI ")
    else:
        kat = katD - katL
        print("ujemny")
    """
    print("deg kat: %s" %(kat) )
    return kat




def open(DRplik, LVplik):
    # Otwieranie pliku DrSchenk i LVersalis
    os.chdir(r"//10.52.80.61/departments/Technology/Private/KROJOWNIA SKÓRY/Makra/Dr Schenk")
    docDR = ezdxf.readfile("wejscie/" + str(DRplik))
    docLV = ezdxf.readfile("wejscie/" + str(LVplik))
    mspLV = docLV.modelspace()
    mspDR = docDR.modelspace()

    return docDR,mspDR, mspLV


def rotate(mspDR, angle1):
    # Obrót pliku (w radianach)
    for e in mspDR:
        #print("Original " + str(e.dxf.color))
            if e.dxf.color == 5:
                e.rgb = (255,0,0)
                e.dxf.color = 1
            #print(str(e.rgb) + str(e.dxf.color))
                e.rotate_z(angle1)
            else:
                e.dxf.color = 5
                e.rgb = (0,0,255)
            #print(e.rgb)
                e.rotate_z(angle1)




DRplik = "13I2622_2022-04-20-15-06-26_dv2.dxf"
LVplik = "13I2622_2022-04-20-15-06-26_lv.dxf"

docDR, mspDR, mspLV = open(DRplik, LVplik)

DRv1, DRv2 = wsptargets(mspDR)
LVv1, LVv2 = wsptargets(mspLV)


angle = abvector(DRv1, DRv2, LVv1, LVv2)
print("Kąt Dr   %s" %(angle))


rotate(mspDR, math.radians(angle))

docDR.saveas("docDR_mtext.dxf")
print("Koniec")