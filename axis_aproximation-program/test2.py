import NXOpen
import NXOpen.UF
from logs_and_save.logs import log, errorLog, errorExit
import traceback
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log
import time
import NXOpen.Annotations
import NXOpen.Drawings
import measure_area as MA

def showSection(workPart, axisorigin, origin, base_matrix):
    dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    dynamicSectionBuilder.ShowClip = True
    dynamicSectionBuilder.SetPlane(axisorigin, origin, base_matrix)
    dynamicSectionBuilder.Commit()

def main():
    # #for testing only
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    base_matrixZ = NXOpen.Matrix3x3()
    origin = NXOpen.Point3d(-20.894713851001704, 37.93716931488205, 20.066063724344648)
    base_matrixZ = NXOpen.Matrix3x3()
    axisorigin = NXOpen.Point3d(0.0, 0.0, 0.0)

    base_matrixZ.Xx = 0.002376946988311951
    base_matrixZ.Xy = -0.44256303930778496
    base_matrixZ.Xz = 0.8967342451148336
    base_matrixZ.Yx = 0.5796605538363047
    base_matrixZ.Yy = 0.7313219150735455
    base_matrixZ.Yz = 0.3593910110998197
    base_matrixZ.Zx = -0.8148545836216443
    base_matrixZ.Zy = 0.5189472157857848
    base_matrixZ.Zz = 0.25827464989614946
    axies = "Z"
    showSection(workPart, axisorigin, origin, base_matrixZ)
    MA.create_spline(workPart)
    MA.create_extrude(workPart)
    centroid = MA.centroid(workPart,theSession)
    MA.reamove_extrude_and_splines(theSession, workPart)

if __name__ == '__main__':
    a = main()

# import math
# import NXOpen
# import measure_area as MA

# theSession = NXOpen.Session.GetSession()
# workPart = theSession.Parts.Work

# MA.reamove_extrude_and_splines(theSession,workPart)