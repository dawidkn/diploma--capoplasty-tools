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

def create_rotation_matrix(axis, angle_deg):

    angle_rad = math.radians(angle_deg)
    cos_theta = math.cos(angle_rad)
    sin_theta = math.sin(angle_rad)

    rotation_matrix = NXOpen.Matrix3x3()

    if axis.upper() == 'X':
        rotation_matrix.Xx, rotation_matrix.Xy, rotation_matrix.Xz = 1.0, 0.0, 0.0
        rotation_matrix.Yx, rotation_matrix.Yy, rotation_matrix.Yz = 0.0, cos_theta, -sin_theta
        rotation_matrix.Zx, rotation_matrix.Zy, rotation_matrix.Zz = 0.0, sin_theta, cos_theta
    elif axis.upper() == 'Y':

        rotation_matrix.Xx, rotation_matrix.Xy, rotation_matrix.Xz = cos_theta, 0.0, sin_theta
        rotation_matrix.Yx, rotation_matrix.Yy, rotation_matrix.Yz = 0.0, 1.0, 0.0
        rotation_matrix.Zx, rotation_matrix.Zy, rotation_matrix.Zz = -sin_theta, 0.0, cos_theta
    elif axis.upper() == 'Z':
        rotation_matrix.Xx, rotation_matrix.Xy, rotation_matrix.Xz = cos_theta, -sin_theta, 0.0
        rotation_matrix.Yx, rotation_matrix.Yy, rotation_matrix.Yz = sin_theta, cos_theta, 0.0
        rotation_matrix.Zx, rotation_matrix.Zy, rotation_matrix.Zz = 0.0, 0.0, 1.0
    else:
        raise ValueError("Unknow axies. Use'X', 'Y' or 'Z'.")

    return rotation_matrix

def multiply_matrices(m1: NXOpen.Matrix3x3, m2: NXOpen.Matrix3x3) -> NXOpen.Matrix3x3:

    result = NXOpen.Matrix3x3()

    result.Xx = m1.Xx*m2.Xx + m1.Xy*m2.Yx + m1.Xz*m2.Zx
    result.Xy = m1.Xx*m2.Xy + m1.Xy*m2.Yy + m1.Xz*m2.Zy
    result.Xz = m1.Xx*m2.Xz + m1.Xy*m2.Yz + m1.Xz*m2.Zz

    result.Yx = m1.Yx*m2.Xx + m1.Yy*m2.Yx + m1.Yz*m2.Zx
    result.Yy = m1.Yx*m2.Xy + m1.Yy*m2.Yy + m1.Yz*m2.Zy
    result.Yz = m1.Yx*m2.Xz + m1.Yy*m2.Yz + m1.Yz*m2.Zz

    result.Zx = m1.Zx*m2.Xx + m1.Zy*m2.Yx + m1.Zz*m2.Zx
    result.Zy = m1.Zx*m2.Xy + m1.Zy*m2.Yy + m1.Zz*m2.Zy
    result.Zz = m1.Zx*m2.Xz + m1.Zy*m2.Yz + m1.Zz*m2.Zz
    return result

def get_normal_from_matrix(originPoint, mat, axis, distance):

    if axis == "X":
        vx, vy, vz = mat.Xx, mat.Xy, mat.Xz  # Wektor osi X
    elif axis == "Y":
        vx, vy, vz = mat.Yx, mat.Yy, mat.Yz  # Wektor osi Y
    elif axis == "Z":
        vx, vy, vz = mat.Zx, mat.Zy, mat.Zz  # Wektor osi Z
    else:
        raise ValueError("unknown axis. Use 'X', 'Y' or 'Z'.")

    # Normalizacja wektora
    length = (vx**2 + vy**2 + vz**2) ** 0.5
    vx /= length
    vy /= length
    vz /= length

    # Obliczenie przesunięcia
    dx = vx * distance
    dy = vy * distance
    dz = vz * distance

    x = originPoint.X
    y = originPoint.Y
    z = originPoint.Z

    # Nowa pozycja
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

def create_sections(workPart, axisorigin, origin, base_matrix, rotAxisSel, angle_range_dwon, angle_range_top, step): #create cestion with additional rotation
    try:
        dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
        dynamicSectionBuilder.ShowClip = True

        smalest_area = []
        for rotation_axis in rotAxisSel:
            for angle in range(angle_range_dwon, angle_range_top, step):
                # create global matrix
                rot_matrix = create_rotation_matrix(rotation_axis, angle)
                # multiplication of global matrix and rotation matrix
                final_matrix = multiply_matrices(base_matrix, rot_matrix)
                # set section plane
                dynamicSectionBuilder.SetPlane(axisorigin, origin, final_matrix)
                dynamicSectionBuilder.Commit()

                area = MA.main()
                temp = [area, rotation_axis, angle, angle_range_dwon, angle_range_top, step, final_matrix]
                smalest_area.append(temp)

        
        min_list = min(smalest_area, key=lambda x: x[0], default="EMPTY")
        smalest_area.clear()
        return min_list
    except Exception as ex:
        errorLog()
        errorExit()

def removeLines(workPart, theSession):
    splines = workPart.Splines
    splObj = []

    lines = workPart.Lines
    lineObj = []
    for line in lines:
        lineObj.append(line)

    nErrs1 = theSession.UpdateManager.AddObjectsToDeleteList(lineObj)
    id1 = theSession.NewestVisibleUndoMark
    nErrs2 = theSession.UpdateManager.DoUpdate(id1)

    for spline in splines:
        splObj.append(spline)

    nErrs1 = theSession.UpdateManager.AddObjectsToDeleteList(splObj)
    id1 = theSession.NewestVisibleUndoMark
    nErrs2 = theSession.UpdateManager.DoUpdate(id1)

def createVector(RotMatrix, origin, TempPlaneSel, workPart, theSession):
    planeSel = ["X", "Y", "Z"]


    axiesList = list(set(planeSel)-set(TempPlaneSel))
    axies = axiesList[0]
    # log("axies", axies)
    endPoint = get_normal_from_matrix(origin, RotMatrix,axies, -100)
    startPoint = get_normal_from_matrix(origin, RotMatrix,axies, 100)
    workPart.ModelingViews.WorkView.DisplaySectioningToggle = False #turn off cilp
    line1 = workPart.Curves.CreateLine(endPoint,startPoint)

    # result = MB.YNBox("Confirm", "Is it Correct Vector?")
    # if result == 1:
        # MB.msgBox("test", "correct")
    removeLines(workPart, theSession)
    # else:
    #     MB.msgBox("vector", "Wrong vector - In Progress")
    #     sys.exit()
    return RotMatrix, axies, origin



def correction(workPart, axisorigin, origin, inputList, theSession):

    planeSel = ["X", "Y", "Z"]
    showSection(workPart, axisorigin, origin, inputList[6])
    # respons1 = MB.YNBox("Correction", "Is it correct vector of head axies?")
    # if respons1 == 2:
    #     MB.msgBox("Wrong axies vector", "Work in progress")
    #     sys.exit()
        
    
    minlist = inputList.copy()
    for i in range(10):
        rangeRotT = 6
        rangeRotD = -6

        TempMinlist = create_sections(workPart, axisorigin, origin, minlist[6], planeSel, rangeRotD, rangeRotT, 2)
        
        for i in range(5):
            if TempMinlist[2] == rangeRotT:
                rangeRotD=rangeRotT
                rangeRotT=rangeRotT+5
                TempMinlist = create_sections(workPart, axisorigin, origin, minlist[6], planeSel, rangeRotD, rangeRotT, 1)
                

            elif TempMinlist[2] == rangeRotD:
                rangeRotT=rangeRotD
                rangeRotD=rangeRotD-5

                
                TempMinlist = create_sections(workPart, axisorigin, origin, minlist[6], planeSel, rangeRotD, rangeRotT, 1)
                
                
            elif i==4:
                respons = MB.YNBox("Rotation Range", "Range of rotation is to small. Do you want to continue?")
                if respons == 1:
                    i=-1
                else:
                    break
            else:
                break

        TempPlaneSel = planeSel.copy()
        TempPlaneSel.remove(TempMinlist[1])
        TempOrigin = origin
        tempAxies = 0
        origin = get_normal_from_matrix(origin, TempMinlist[6], TempPlaneSel[1], 6)
        tempAxies=TempPlaneSel[1]
        showSection(workPart, axisorigin, origin, TempMinlist[6])
        area = MA.main()
        tempArea = round(TempMinlist[0], 2)
        if area == tempArea:
            origin = get_normal_from_matrix(origin, TempMinlist[6], TempPlaneSel[0], 6)
            tempAxies=TempPlaneSel[0]


        minAreaOfAll = minlist.copy()
        if TempMinlist[0] < minlist[0]:
            minlist = TempMinlist.copy()
            if minlist[0] < minAreaOfAll[0]:
                minAreaOfAll = TempMinlist.copy()
                TempOrigin = origin

        else:
            if TempMinlist[0] > minlist[0]*1.1:
                if TempMinlist[0]>1000:
                    continue
                else:
                    log("axies found", f"{TempMinlist[0]}{origin}")
                    break
            else:
                minlist = TempMinlist.copy()
                log("new min but greater than smallest", minlist)

            continue
    
    showSection(workPart, axisorigin, TempOrigin, minAreaOfAll[6])
    # log("minareaofall", f"{minAreaOfAll}{TempOrigin}")
    # log("tempAxies", TempPlaneSel)
    # log("matrix",f"{minlist[6].Xx}, {minlist[6].Xy}, {minlist[6].Xz}, {minlist[6].Yx}, {minlist[6].Yy}, {minlist[6].Yz}, {minlist[6].Zx}, {minlist[6].Zy}, {minlist[6].Zz}")
    RotMatrix, axies, origin = createVector(minAreaOfAll[6],TempOrigin,TempPlaneSel,workPart, theSession)

    return RotMatrix, axies, origin, axisorigin

        


def main():
    # #for testing only
    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    base_matrixZ = NXOpen.Matrix3x3()
    axisorigin = NXOpen.Point3d(0.0, 0.0, 0.0)
    origin = NXOpen.Point3d(0.0, -0.26495963211660245, 0.42402404807821298)
    base_matrixZ.Xx = 0.0
    base_matrixZ.Xy = -0.5299192642332049
    base_matrixZ.Xz = 0.848048096156426
    base_matrixZ.Yx = 0.8660254037844387
    base_matrixZ.Yy = 0.4240240480782129
    base_matrixZ.Yz = 0.2649596321166024
    base_matrixZ.Zx = -0.49999999999999994
    base_matrixZ.Zy = 0.7344311949024933
    base_matrixZ.Zz = 0.45892354478071395
    dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    dynamicSectionBuilder.ShowClip = True
    dynamicSectionBuilder.SetPlane(axisorigin, origin, base_matrixZ)
    dynamicSectionBuilder.Commit()
    planesel = ["X", "Y", "Z"]

    minlist = [1337.567261815182, 'X', 0, -30, 30, 5, base_matrixZ]

    correction(workPart, axisorigin, origin, minlist, theSession)

   

if __name__ == '__main__':
    a = main()

