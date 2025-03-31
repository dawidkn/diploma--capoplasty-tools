import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log,errorLog, errorExit
import time
import NXOpen.Annotations
import NXOpen.Drawings
import NXOpen.Display
from additonal_functions import msgBox as MB
import sys


def createCSYS(workPart, origin, centroid, point1):

    datumCsysBuilder1 = workPart.Features.CreateDatumCsysBuilder(NXOpen.Features.Feature.Null)
    
    xform1 = workPart.Xforms.CreateXform(origin, point1, centroid, NXOpen.SmartObject.UpdateOption.WithinModeling, 1.0)

    cartesianCoordinateSystem1 = workPart.CoordinateSystems.CreateCoordinateSystem(xform1, NXOpen.SmartObject.UpdateOption.WithinModeling)
    datumCsysBuilder1.Csys = cartesianCoordinateSystem1
    datumCsysBuilder1.DisplayScaleFactor = 1.25
    nXObject1 = datumCsysBuilder1.Commit()

def offset_point(point1, point2, d):
    p1= (point1.X, point1.Y, point1.Z)
    p2= (point2.X, point2.Y, point2.Z)
    dx = p2[0] - p1[0]
    dy = p2[1] - p1[1]
    dz = p2[2] - p1[2]

    lenght = math.sqrt(dx**2 + dy**2 + dz**2)

    if lenght == 0:
        raise ValueError("p1 and p2 are the same point")

    ux = dx / lenght
    uy = dy / lenght
    uz = dz / lenght

    x = p1[0] + ux * d
    y = p1[1] + uy * d
    z = p1[2] + uz * d
    newPoint = NXOpen.Point3d(x, y, z)
    

    return newPoint

def subtractCyl(workPart, target, tool,Flag=0):
    booleanBuilder1 = workPart.Features.CreateBooleanBuilderUsingCollector(NXOpen.Features.BooleanFeature.Null)
    
    
    booleanBuilder1.Tolerance = 0.01
    
    booleanBuilder1.Operation = NXOpen.Features.Feature.BooleanType.Subtract
    scCollector3 = workPart.ScCollectors.CreateCollector() 
    selectionIntentRuleOptions1 = workPart.ScRuleFactory.CreateRuleOptions() 
    selectionIntentRuleOptions1.SetSelectedFromInactive(False)
    bodyDumbRule1 = None
    # log("target",f"target: {target}")

    if Flag == 1:
        booleanBuilder1.CopyTools = True

    bodies32 = [NXOpen.Body.Null] * 1 #target
    bodies32[0] = target
    bodyDumbRule1 = workPart.ScRuleFactory.CreateRuleBodyDumb(bodies32, True, selectionIntentRuleOptions1)

    bodies22 = [NXOpen.Body.Null] * 1 #tool
    bodies22[0] = tool
    bodyDumbRule2 = workPart.ScRuleFactory.CreateRuleBodyDumb(bodies22, True, selectionIntentRuleOptions1)
    
    selectionIntentRuleOptions1.Dispose()
    rules1 = [None] * 1 
    rules1[0] = bodyDumbRule1
    scCollector3.ReplaceRules(rules1, False)

    booleanBuilder1.TargetBodyCollector = scCollector3
    scCollector4 = workPart.ScCollectors.CreateCollector()
    selectionIntentRuleOptions2 = workPart.ScRuleFactory.CreateRuleOptions()
    selectionIntentRuleOptions2.SetSelectedFromInactive(False)
    selectionIntentRuleOptions2.Dispose()
    rules2 = [None] * 1 
    rules2[0] = bodyDumbRule2
    scCollector4.ReplaceRules(rules2, False)
    
    booleanBuilder1.ToolBodyCollector = scCollector4
    nXObject1 = booleanBuilder1.Commit()

def distance_btw_points(point1, point2):
    x1, y1, z1 = point1.X, point1.Y, point1.Z
    x2, y2, z2 = point2.X, point2.Y, point2.Z
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def createPoint(workPart, midPoint, point1, point2, point3, centroid):
    # line1 = workPart.Curves.CreateLine(p1,p2)
    mPoint = workPart.Points.CreatePoint(midPoint)
    mPoint.SetVisibility(NXOpen.SmartObjectVisibilityOption.Visible)
    p1 = workPart.Points.CreatePoint(point1)
    p1.SetVisibility(NXOpen.SmartObjectVisibilityOption.Visible)
    p2 = workPart.Points.CreatePoint(point2)
    p2.SetVisibility(NXOpen.SmartObjectVisibilityOption.Visible)
    p3 = workPart.Points.CreatePoint(point3)
    p3.SetVisibility(NXOpen.SmartObjectVisibilityOption.Visible)
    c1 = workPart.Points.CreatePoint(centroid)
    c1.SetVisibility(NXOpen.SmartObjectVisibilityOption.Visible)

    mainVector = workPart.Curves.CreateLine(centroid,midPoint)
    line1 = workPart.Curves.CreateLine(midPoint,point1)
    line2 = workPart.Curves.CreateLine(midPoint,point2)
    line3 = workPart.Curves.CreateLine(midPoint,point3)


    return mPoint, p1, p2, p3, c1

def createCylinder(workPart, centroid, mainP, diameter, height, flag): #flag = 1 direction in plus, 0 in minus
    cylinderBuilder1 = workPart.Features.CreateCylinderBuilder(NXOpen.Features.Feature.Null)
    cylinderBuilder1.Diameter.SetFormula(f"{diameter}")
    
    cylinderBuilder1.Height.SetFormula(f"{height}")
    direction1=0
    if flag == 1:
        direction1 = workPart.Directions.CreateDirection(centroid, mainP, NXOpen.SmartObject.UpdateOption.WithinModeling)
    else:
        direction1 = workPart.Directions.CreateDirection(mainP,centroid, NXOpen.SmartObject.UpdateOption.WithinModeling)

    axis1 = cylinderBuilder1.Axis
    
    axis1.Direction = direction1
    
    axis1.Point = NXOpen.Point.Null
    
    axis1.Evaluate()
    axis1.Point = mainP
    cylinderBuilder1.Commit()

def insertCreation(workPart, maxarea, origin, point1, point2, point3, centroid):
    d = 2*((maxarea/math.pi)**0.5)#diameter of head in max area
    # log("radius",f"R: {r}")
    dist = distance_btw_points(origin, centroid)
    mainP, p1,p2,p3, centroid1 = createPoint(workPart, origin, point1, point2, point3, centroid)
    # createCSYS(workPart, mainP, p1, centroid1)
    # createCSYS(workPart, mainP, p2, centroid1)
    # createCSYS(workPart, mainP, p3, centroid1)
    height = dist
    createCylinder(workPart, centroid1, mainP, 5, 10,1)   #in plus inner deriling hole
    createCylinder(workPart, centroid1, mainP, 5, 5,0)    #in minus inner deriling hole

    createCylinder(workPart, centroid1, mainP, 10, 10,1)   #in plus outer deriling hole
    # createCylinder(workPart, centroid1, mainP, 10, 4,0)    #in minus outer deriling hole

    offP = workPart.Points.CreatePoint(offset_point(origin, centroid, 4))
    # createCylinder(workPart, centroid1, offP, d+2, height-5,0) #inner hole cover head
    createCylinder(workPart, centroid1, mainP, d+7, height*1.5,0) #outer hole cover head
    # log("distance",f"Distance between points: {dist}")
    # createCylinder(workPart, centroid1, mainP, d*1.3, 5,1) #case


    bodies = workPart.Bodies
    bodies1 = []
    for body in bodies:
        bodies1.append(body)

    subtractCyl(workPart, bodies1[3], bodies1[1])
    # subtractCyl(workPart, bodies1[4], bodies1[2],1)
    subtractCyl(workPart, bodies1[4], bodies1[0],1)
    # subtractCyl(workPart, bodies1[6], bodies1[5])
    # subtractCyl(workPart, bodies1[6], bodies1[1])
    subtractCyl(workPart, bodies1[4], bodies1[2])

def main():
    # #for testing only
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    base_matrixZ = NXOpen.Matrix3x3()
    origin = NXOpen.Point3d(-59.12313515186192, 38.02730223717464, 11.558153675204407)
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
    
    centroid = NXOpen.Point3d(-35.492352226834214, 22.977832979386864,4.068188828216064)
    point1 = NXOpen.Point3d(15.51085339097, -1.52670270907, 29.92847719730)
    point2 = NXOpen.Point3d(-27.762636844344186, -22.978031685468817, -21.82689591032134)
    point3 = NXOpen.Point3d(-1.48718066838, 3.80671253247, -18.64946786324)
    maxarea = 2133.1795786153034

    insertCreation(workPart, maxarea, origin, point1, point2, point3, centroid)
if __name__ == '__main__':
    a = main()
   