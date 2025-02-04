
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

    angle_rad = math.radians(angle_deg-90)
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
    planeC = MB.inputBox("1-XY, 2-YZ, 3-ZX")
    

    rotationmatrix1 = NXOpen.Matrix3x3()
    dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)

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

        dynamicSectionBuilder.ShowClip = True
        dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)
        section = dynamicSectionBuilder.Commit()
        MB.msgBox("Plane","XY")

        for rotation_axis in ['X', 'Y']:
            for angle in range(-30, 30, 10):
                rotationmatrix1 = create_rotation_matrix(rotation_axis, angle)
                dynamicSectionBuilder.ShowClip = True

                dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)

                section = dynamicSectionBuilder.Commit()
                time.sleep(1)


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
        dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
        dynamicSectionBuilder.ShowClip = True

        


        dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)

        section = dynamicSectionBuilder.Commit()
        MB.msgBox("Plane","YZ")
        for rotation_axis in ['Y', 'Z']:
            for angle in range(0, 30, 10):
                rotationmatrix1 = create_rotation_matrix(rotation_axis, angle)
                dynamicSectionBuilder.ShowClip = True

                dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)

                section = dynamicSectionBuilder.Commit()
                time.sleep(1)

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

        dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
        dynamicSectionBuilder.ShowClip = True

        dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)

        section = dynamicSectionBuilder.Commit()
        MB.msgBox("Plane","ZX")
        for rotation_axis in ['X','Y']:
            for angle in range(-10, 10, 5):
                rotationmatrix1 = create_rotation_matrix(rotation_axis, angle)
                dynamicSectionBuilder.ShowClip = True

                dynamicSectionBuilder.SetPlane(axisorigin, origin, rotationmatrix1)

                section = dynamicSectionBuilder.Commit()
                time.sleep(1)

    else:
        MB.msgBox("chuj","chuj")


    # plane_orientations = {
    #     "XY": NXOpen.Matrix3x3(
    #         Xx=1.0, Xy=0.0, Xz=0.0,
    #         Yx=0.0, Yy=1.0, Yz=0.0,
    #         Zx=0.0, Zy=0.0, Zz=1.0
    #     ),
    #     "YZ": NXOpen.Matrix3x3(
    #         Xx=0.0, Xy=0.0, Xz=1.0,
    #         Yx=0.0, Yy=1.0, Yz=0.0,
    #         Zx=1.0, Zy=0.0, Zz=0.0
    #     ),
    #     "ZX": NXOpen.Matrix3x3(
    #         Xx=1.0, Xy=0.0, Xz=0.0,
    #         Yx=0.0, Yy=0.0, Yz=1.0,
    #         Zx=0.0, Zy=1.0, Zz=0.0
    #     )
    # }
    area = []
    

    # # Tworzenie przekrojów
    # for plane, base_matrix in plane_orientations.items():
    #     for rotation_axis in ['X', 'Y', 'Z']:
    #         for angle in range(0, 30, 10):
    #             # Generowanie macierzy rotacji dla obrotu
    #             rotation_matrix = create_rotation_matrix(rotation_axis, angle)

    #             # Połączenie macierzy bazowej z obrotem
    #             # W tej prostszej implementacji używamy tylko rotacji wokół jednej osi na raz
    #             final_matrix = rotation_matrix

    #             # Tworzenie dynamicznego przekroju
    #             dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    #             dynamicSectionBuilder.ShowClip = True

    #             # Ustawienie płaszczyzny przekroju
    #             dynamicSectionBuilder.SetPlane(axisorigin, origin, final_matrix)

    #             # Zatwierdzenie przekroju
    #             section = dynamicSectionBuilder.Commit()
    #             area.append([MA.main(),angle,rotation_axis,plane])


    #             # Zwolnienie zasobów
    #             dynamicSectionBuilder.Destroy()
    # log("correction area", area)
    # min_index, min_value = min(enumerate(area), key=lambda x: x[1][0])
    # log("min value", min_value)
    # log("type", area[min_index])

    # po=area[min_index]
    # rotation_matrix = create_rotation_matrix(po[2], po[1])
    # final_matrix = rotation_matrix
    # dynamicSectionBuilder = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    # dynamicSectionBuilder.ShowClip = True
    # dynamicSectionBuilder.SetPlane(axisorigin, origin, final_matrix)

    # # Zatwierdzenie przekroju
    # section = dynamicSectionBuilder.Commit()
    # log("after-close",MA.main())

    # # Ustawienie płaszczyzny przekroju
    # dynamicSectionBuilder.SetPlane(axisorigin, origin, final_matrix)

# Uruchomienie funkcji
create_sections()
