import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log
import time
import NXOpen.Annotations
import NXOpen.Drawings
import measure_area as MA
import NXOpen.Display
from additonal_functions import msgBox as MB


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


def create_sections(workPart, axisorigin, origin, base_matrix, rotAxisSel, angle_range_dwon, angle_range_top, step): #create cestion with additional rotation
    # set base matrix
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

    min_list = min(smalest_area, key=lambda x: x[0])

    smalest_area.clear()
    return min_list



def correction_plane(workPart,min_list,axisorigin,origin):

    planesel = ["X","Y","Z"]

    if min_list[2]==min_list[3]:
        
        planesel = [item for item in planesel if item != min_list[1]]

        min_list = create_sections(workPart, axisorigin, origin, min_list[6], planesel, min_list[3]-7, min_list[3]+7, 1)

    elif min_list[2]==min_list[4]:
        
        planesel = [item for item in planesel if item != min_list[1]]

        min_list = create_sections(workPart, axisorigin, origin, min_list[6], planesel, min_list[4]-7, min_list[4]+7, 1)

    else:
        
        planesel = [item for item in planesel if item != min_list[1]]

        min_list = create_sections(workPart, axisorigin, origin, min_list[6], planesel, min_list[2]-7, min_list[2]+7, 1)

    log("min list after correction - dt virst vector",f"{min_list} and {min_list[6].Xx} {min_list[6].Xy} {min_list[6].Xz} {min_list[6].Yx} {min_list[6].Yy} {min_list[6].Yz} {min_list[6].Zx} {min_list[6].Zy} {min_list[6].Zz}")  
    
    origin = get_normal_from_matrix(origin, min_list[6], min_list[1], 0.5)  
    log("newOrigin - dt virst vector", origin)
    return origin, min_list


def basePlanedef(theSession,workPart):
    base_matrixX = NXOpen.Matrix3x3()
    base_matrixY = NXOpen.Matrix3x3()
    base_matrixZ = NXOpen.Matrix3x3()
    
    base_matrixX.Xx = 0.0
    base_matrixX.Xy = 1.0
    base_matrixX.Xz = 0.0
    base_matrixX.Yx = -1.0
    base_matrixX.Yy = 0.0
    base_matrixX.Yz = 0.0
    base_matrixX.Zx = 0.0
    base_matrixX.Zy = 0.0
    base_matrixX.Zz = 1.0

    base_matrixY.Xx = 0.0
    base_matrixY.Xy = 1.0
    base_matrixY.Xz = 0.0
    base_matrixY.Yx = 0.0
    base_matrixY.Yy = 0.0
    base_matrixY.Yz = 1.0
    base_matrixY.Zx = 1.0
    base_matrixY.Zy = 0.0
    base_matrixY.Zz = 0.0
 
    base_matrixZ.Xx = 0.0
    base_matrixZ.Xy = 0.0
    base_matrixZ.Xz = 1.0
    base_matrixZ.Yx = 1.0
    base_matrixZ.Yy = 0.0
    base_matrixZ.Yz = 0.0
    base_matrixZ.Zx = 0.0
    base_matrixZ.Zy = 1.0
    base_matrixZ.Zz = 0.0
    base_plane_matrix = [[base_matrixX,["X","Y"]], [base_matrixY,["Y","Z"]], [base_matrixZ,["X","Z"]]]


    axisorigin = NXOpen.Point3d(0.0, 0.0, 0.0)
    origin = NXOpen.Point3d(0.0, 0.0, 0.0)    
    smalest_area = []
    for bm in base_plane_matrix:
            base_matrix = bm[0]
            planeSel = bm[1]
            smalest_area.append(create_sections(workPart, axisorigin, origin, base_matrix, planeSel,-30, 30, 5))

    min_list = min(smalest_area, key=lambda x: x[0])
    smalest_area.clear()

    origin, min_list = correction_plane(workPart,min_list,axisorigin,origin)
    return origin, min_list, axisorigin

####Call separate function####
# theSession = NXOpen.Session.GetSession()
# workPart = theSession.Parts.Work
# basePlanedef(theSession,workPart)