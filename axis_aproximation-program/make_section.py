#this file prepare only base sections on x y z

import math
import NXOpen
import NXOpen.Display
import time
from measure_area import main as measure
from logs_and_save.logs import log

def make_sec(workPart) : 


    dynamicSectionBuilder1 = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    
    dynamicSectionBuilder1.ShowClip = True

    sectionArea = [0,0,0]

    axisorigin = NXOpen.Point3d(0.0, 0.0, 0.0)
    origin = NXOpen.Point3d(0.0, 0.0, 0.0)
    rotationmatrix1 = NXOpen.Matrix3x3()
    
    rotationmatrix1.Xx = 0.0
    rotationmatrix1.Xy = 1.0
    rotationmatrix1.Xz = 0.0
    rotationmatrix1.Yx = 0.0
    rotationmatrix1.Yy = 0.0
    rotationmatrix1.Yz = 1.0
    rotationmatrix1.Zx = 1.0
    rotationmatrix1.Zy = 0.0
    rotationmatrix1.Zz = 0.0
    dynamicSectionBuilder1.SetPlane(axisorigin, origin, rotationmatrix1)

    
    nXObject1 = dynamicSectionBuilder1.Commit()
    sectionArea[0] = measure()

    
    rotationmatrix1.Xx = 0.0
    rotationmatrix1.Xy = 0.0
    rotationmatrix1.Xz = 1.0
    rotationmatrix1.Yx = 1.0
    rotationmatrix1.Yy = 0.0
    rotationmatrix1.Yz = 0.0
    rotationmatrix1.Zx = 0.0
    rotationmatrix1.Zy = 1.0
    rotationmatrix1.Zz = 0.0

    dynamicSectionBuilder1.SetPlane(axisorigin, origin, rotationmatrix1)
    nXObject1 = dynamicSectionBuilder1.Commit()
    sectionArea[1] = measure()


    rotationmatrix1.Xx = 0.0
    rotationmatrix1.Xy = 1.0
    rotationmatrix1.Xz = 0.0
    rotationmatrix1.Yx = -1.0
    rotationmatrix1.Yy = 0.0
    rotationmatrix1.Yz = 0.0
    rotationmatrix1.Zx = 0.0
    rotationmatrix1.Zy = 0.0
    rotationmatrix1.Zz = 1.0

    dynamicSectionBuilder1.SetPlane(axisorigin, origin, rotationmatrix1)
    nXObject1 = dynamicSectionBuilder1.Commit()
    sectionArea[2] = measure()

    
    dynamicSectionBuilder1.ShowClip = False
    log("sections area:", sectionArea)
