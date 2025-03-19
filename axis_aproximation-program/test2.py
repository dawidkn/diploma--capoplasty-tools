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

theSession  = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

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
TempPlaneSel =['X', 'Y']
planeSel = ["X", "Y", "Z"]


axies = list(set(planeSel)-set(TempPlaneSel))

log("test", axies[0])
showSection(workPart, axisorigin, origin, base_matrixZ)

endPoint = get_normal_from_matrix(origin, base_matrixZ,axies[0], -100)
startPoint = get_normal_from_matrix(origin, base_matrixZ,axies[0], 100)

try:


    line1 = workPart.Curves.CreateLine(endPoint,startPoint)


except:
    errorLog()


