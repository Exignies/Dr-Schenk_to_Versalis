#!/usr/bin/env python
#coding:utf-8
from xml.dom.minidom import Attr
import ezdxf
import os
import numpy as np
from ezdxf.math import OCS
from ezdxf.math import Vec3
import math
#from ezdxf.upright import upright_all



def vectors (ms):
    # Obliczanie kąta orginału
    vector = []
    for i in ms.query('TEXT'):
        vector.append(i.dxf.insert)
    v1 = vector[0]
    v2 = vector[1]
    print(v1)
    print(v2)
    return v1, v2


""""
stare
def abvector(Xv1, Xv2):
    # oblicza a i b lini przciętej przez 2 punkty
    a = (Xv2[1]-Xv1[1])/(Xv2[0]-Xv1[0])
    b = Xv1[1]-(a*Xv1[0])
    print("wsp a: %s i wsp b: %s" %(a, b) )
    return a, b
"""

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

    if bD < 0:
        print(katD)
        katD = 180 - katD
        print("db |X1-X2| < 0")

    
    print("deg katd: %s" %(katD) )
    
    # Lv
    if Lv1[1] >= Lv2[1]: # czy nie zamieniono miejscami punktów
        aL = Lv1[1] - Lv2[1]
        bL = Lv1[0] - Lv2[0]
        print("lv1(y) >= lv2(y)") 
    else:
        aL = Lv2[1] - Lv1[1]
        bL = Lv2[0] - Lv1[0]
        print("lv1(y) < lv2(y)")
    if bL >= 0:
        katL = aL/bL
        print("dl |X1-X2| >= 0")
    else:
        katL = 180 - (aL/(-bL))

    katL = math.atan(katL)
    katL = math.degrees(katL)
    print("deg katL: %s" %(katL) )

    # obliczanie roznicy w katach
    if katD >= katL:
        kat = -(katD - katL)
        print("DODATNI ")
    else:
        kat = katD - katL
        print("ujemny")
    print("deg kat: %s" %(kat) )
    return kat


# xxxxxxxxxx

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

    #XXXXXXXXXXXX





def open(DRplik, LVplik):
    # Otwieranie pliku DrSchenk i LVersalis
    os.chdir(r"//10.52.80.61/departments/Technology/Private/KROJOWNIA SKÓRY/Makra/Dr Schenk")
    docDR = ezdxf.readfile("wejscie/" + str(DRplik))
    docLV = ezdxf.readfile("wejscie/" + str(LVplik))
    mspLV = docLV.modelspace()
    mspDR = docDR.modelspace()

    return docDR, docLV, mspDR, mspLV


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




DRplik = "13I2622_2022-04-20-15-06-26.dxf"
LVplik = "13I2622_2022-04-20-15-06-26.dxf"

docDR, docLV, mspDR, mspLV = open(DRplik, LVplik)

DRv1, DRv2 = vectors(mspDR)
LVv1, LVv2 = vectors(mspLV)



#angle = abvector(DRv1, DRv2, LVv1, LVv2)
#print("Kąt Dr   %s" %(angle))
angle = 25
angle = math.radians(angle) #zamiana na radiany

angle2 = -22
angle2 = math.radians(angle2) #zamiana na radiany
print("Kąt Dr rad   %s" %(angle2))

rotate(mspDR, angle)
rotate(mspLV, angle2)

docDR.saveas("13I2622_2022-04-20-15-06-26_dv.dxf")
docLV.saveas("13I2622_2022-04-20-15-06-26_lv.dxf")
print("Koniec")