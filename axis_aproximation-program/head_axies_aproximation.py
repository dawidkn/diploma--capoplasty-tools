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