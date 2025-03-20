import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log,errorLog, errorExit
import time
import NXOpen.Annotations
import NXOpen.Drawings
import measure_area as MA
import NXOpen.Display
from additonal_functions import msgBox as MB
import sys


def get_normal_from_matrix(originPoint, mat, axis, distance):

    if axis == "X":
        vx, vy, vz = mat.Xx, mat.Xy, mat.Xz  
    elif axis == "Y":
        vx, vy, vz = mat.Yx, mat.Yy, mat.Yz  
    elif axis == "Z":
        vx, vy, vz = mat.Zx, mat.Zy, mat.Zz  
    else:
        raise ValueError("unknown axis. Use 'X', 'Y' or 'Z'.")

    length = (vx**2 + vy**2 + vz**2) ** 0.5
    vx /= length
    vy /= length
    vz /= length

    dx = vx * distance
    dy = vy * distance
    dz = vz * distance

    x = originPoint.X
    y = originPoint.Y
    z = originPoint.Z

    new_x = x + dx
    new_y = y + dy
    new_z = z + dz
    origin = NXOpen.Point3d(new_x, new_y, new_z)  
    return origin

def showSection(workPart, axisorigin, origin, base_matrix):
    dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    dynamicSectionBuilder.ShowClip = True
    dynamicSectionBuilder.SetPlane(axisorigin, origin, base_matrix)
    dynamicSectionBuilder.Commit()

def distance_3d(point1, point2):
    
    x1, y1, z1 = point1.X, point1.Y, point1.Z
    x2, y2, z2 = point2.X, point2.Y, point2.Z
    return math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)

def createHeadAxiesVector(workPart, baseVector1, baseVector2, centroid1):
    def calculate_direction_vector(p1, p2):
        return (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])

    def find_offset_point(p_new, direction_vector, distance):
        vx, vy, vz = direction_vector
        vector_length = math.sqrt(vx**2 + vy**2 + vz**2)
        t = distance / vector_length  
        return (p_new[0] + t * vx, p_new[1] + t * vy, p_new[2] + t * vz)

    p1 = (baseVector1.X, baseVector1.Y, baseVector1.Z)
    p2 = (baseVector2.X, baseVector2.Y, baseVector2.Z)
    p_new = (centroid1.X, centroid1.Y, centroid1.Z)
    distance = 100      


    direction_vector = calculate_direction_vector(p1, p2)
    offset_point = find_offset_point(p_new, direction_vector, distance)

    p1 = NXOpen.Point3d(p_new[0],p_new[1],p_new[2])
    p2 = NXOpen.Point3d(offset_point[0],offset_point[1],offset_point[2])

    line1 = workPart.Curves.CreateLine(p1,p2)

def FindMidPoint(workPart, theSession, RotMatrix, axis, originPoint, axisorigin):
    maxAreaList = []
    baseVector1 = originPoint
    baseVector2 = get_normal_from_matrix(originPoint, RotMatrix, axis, 10)

    while True:
        try:
            showSection(workPart, axisorigin, originPoint, RotMatrix)
            area = MA.main()
            temp = [area,originPoint]
            maxAreaList.append(temp)
            originPoint = get_normal_from_matrix(originPoint,RotMatrix,axis,2)
        except:
            break

    maxArea = max(maxAreaList, key=lambda x: x[0], default="EMPTY")
    log("test", maxArea)
    firstPoint = maxAreaList[0]
    lastPoint = maxAreaList[-1]
    dist1 = distance_3d(maxArea[1], firstPoint[1])
    dist2 = distance_3d(maxArea[1], lastPoint[1])

    #get centroid of mid head
    showSection(workPart, axisorigin, maxArea[1], RotMatrix)
    MA.create_spline(workPart)
    MA.create_extrude(workPart)
    centroid1 = MA.centroid(workPart,theSession)
    MA.reamove_extrude_and_splines(theSession, workPart)
    log("centroid mid", f"{centroid1.X}, {centroid1.Y},{centroid1.Z}")
    createHeadAxiesVector(workPart, baseVector1, baseVector2, centroid1)
    MB.msgBox("FNALY!!", "!!!WE DID IT!!")




def main():
    # #for testing only
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    base_matrixZ = NXOpen.Matrix3x3()
    origin = NXOpen.Point3d(-7.8570405130554013, 29.634013862309477, 15.933669326006257)
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
    FindMidPoint(workPart,theSession, base_matrixZ, axies, origin, axisorigin)
   

if __name__ == '__main__':
    a = main()
   