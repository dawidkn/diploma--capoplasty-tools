
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
        raise ValueError("Niepoprawna oś. Użyj 'X', 'Y' lub 'Z'.")

    return rotation_matrix

def create_sections():

    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    
    axisorigin = NXOpen.Point3d(0.0, 0.0, 0.0)
    origin = NXOpen.Point3d(0.0, 0.0, 0.0)
    # planeC = MB.inputBox("1-XY, 2-YZ, 3-ZX")
    planeC=["2"]
    
    planeSel=[]

    rotationmatrix1 = NXOpen.Matrix3x3()

    if planeC[0] == "1":      
        rotationmatrix1.Xx = 0.0
        rotationmatrix1.Xy = 1.0
        rotationmatrix1.Xz = 0.0
        rotationmatrix1.Yx = -1.0
        rotationmatrix1.Yy = 0.0
        rotationmatrix1.Yz = 0.0
        rotationmatrix1.Zx = 0.0
        rotationmatrix1.Zy = 0.0
        rotationmatrix1.Zz = 1.0
        planeSel=["X","Y"]

    elif planeC[0] == "2":
        rotationmatrix1.Xx = 0.0
        rotationmatrix1.Xy = 1.0
        rotationmatrix1.Xz = 0.0
        rotationmatrix1.Yx = 0.0
        rotationmatrix1.Yy = 0.0
        rotationmatrix1.Yz = 1.0
        rotationmatrix1.Zx = 1.0
        rotationmatrix1.Zy = 0.0
        rotationmatrix1.Zz = 0.0
        planeSel=["Y","X", "Z"]


    elif planeC[0] == "3":


        rotationmatrix1.Xx = 0.0
        rotationmatrix1.Xy = 0.0
        rotationmatrix1.Xz = 1.0
        rotationmatrix1.Yx = 1.0
        rotationmatrix1.Yy = 0.0
        rotationmatrix1.Yz = 0.0
        rotationmatrix1.Zx = 0.0
        rotationmatrix1.Zy = 1.0
        rotationmatrix1.Zz = 0.0
        planeSel=["X","Z"]


    else:
        MB.msgBox("chuj","chuj")


    log("BASE - rotationmatrix",rotationmatrix1)
    dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)

    dynamicSectionBuilder.ShowClip = True
    dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)
    MB.msgBox("plane",planeSel)

    section = dynamicSectionBuilder.Commit()
    # MB.msgBox("Plane",planeSel[0]+planeSel[1])
    

    for rotation_axis in [planeSel[0], planeSel[1], planeSel[2]]:
        for angle in range(-60, 60, 10):
            rotationmatrix1 = create_rotation_matrix(rotation_axis, angle)
            dynamicSectionBuilder.ShowClip = True
            log(f"Rotation axies: {rotation_axis}, Angle: {angle}",rotationmatrix1)

            dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)

            section = dynamicSectionBuilder.Commit()
            time.sleep(0.2)


create_sections()
