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

def abvector(Xv1, Xv2):
    # oblicza a i b lini przciętej przez 2 punkty
    b = 1
    a = 160.07/24.85
    print("test a: %s" %(a) )
    a = math.atan(a)
    print("test tg a: %s" %(a) )
    a = math.degrees(a)
    print("test rad a: %s" %(a) )
    print("wsp a: %s i wsp b: %s" %(a, b) )
    return a, b


# xxxxxxxxxx
def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

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




DRplik = "13I2622_2022-04-14-14-26-28.dxf"
LVplik = "13I2622_2022-04-14-14-26-28_2.dxf"

docDR, mspDR, mspLV = open(DRplik, LVplik)

DRv1, DRv2 = vectors(mspDR)
angle1, bDR = abvector(DRv1, DRv2)
print("Kąt Dr przed : %s" %(angle1))
angle1 = math.atan(angle1)
#angle1 = angle_between(DRv1, DRv2)
print("Kąt Dr: %s" %(angle1))

LVv1, LVv2 = vectors(mspLV)
angle2, bLV = abvector(LVv1, LVv2)
angle2 = math.atan(angle2)
#angle2 = angle_between(LVv1, LVv2)
print("Kąt Lv: %s" %(angle2))
print("Kąt DR - Lv: %s" %((angle1-angle2)))

# zamiana na radiany

#angle1 = math.radians(angle1)
#angle2 = math.radians(angle2)

kat = angle1 - angle2
rotate(mspDR, kat)



docDR.saveas("docDR_mtext.dxf")
print("Koniec")