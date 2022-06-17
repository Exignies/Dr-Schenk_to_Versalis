#!/usr/bin/env python
#coding:utf-8
import ezdxf
from ezdxf.upright import upright_all


#area = ezdxf.math.area(vertices: Iterable[Vertex]) 
#print (area)




doc = ezdxf.readfile("wejscie/13I2622_2022-04-05-09-39-27.dxf").rotate_x(90)
msp = doc.modelspace()

msp.add_line((0, 0), (1, 0), dxfattribs={"layer": "MyLayer"})


#doc2 = ezdxf.math.basic_transformation((100, 0, 0), (1, 1, 1), 90) #→ Matrix44
#print(doc)


doc.saveas("doc_mtext.dxf")
