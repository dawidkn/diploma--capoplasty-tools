import math
import NXOpen
import measure_area as MA


def calculate_direction_vector(p1, p2):
    return (p2[0] - p1[0], p2[1] - p1[1], p2[2] - p1[2])


def find_offset_point(p_new, direction_vector, distance):
    vx, vy, vz = direction_vector
    vector_length = math.sqrt(vx**2 + vy**2 + vz**2)
    t = distance / vector_length  # Obliczamy parametr t dla zadanej odległości
    return (p_new[0] + t * vx, p_new[1] + t * vy, p_new[2] + t * vz)

# --- Dane wejściowe ---
p1 = (-23.797783235633485, 12.977580455591582, -0.8917402042797428)      # Pierwszy punkt początkowej prostej
p2 = (-89.34249887521983, 81.52873544088796, 41.761134315621206)      # Drugi punkt początkowej prostej
p_new = (-35.492352226834214, 22.977832979386864, 4.068188828216064)   # Punkt, do którego przesuwamy prostą
distance = 100      # Odległość, o którą odsuwamy punkt

# --- Obliczenia ---
direction_vector = calculate_direction_vector(p1, p2)  # Wyznaczamy wektor kierunkowy
offset_point = find_offset_point(p_new, direction_vector, distance)  # Szukamy nowego punktu



theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work
p1 = NXOpen.Point3d(p_new[0],p_new[1],p_new[2])
p2 = NXOpen.Point3d(offset_point[0],offset_point[1],offset_point[2])

line1 = workPart.Curves.CreateLine(p1,p2)




#baseVector
p1 = NXOpen.Point3d(-23.797783235633485, 12.977580455591582, -0.8917402042797428)
p2 = NXOpen.Point3d(-89.34249887521983, 81.52873544088796, 41.761134315621206)

line1 = workPart.Curves.CreateLine(p1,p2)

#mid
p1 = NXOpen.Point3d(-35.492352226834214, 22.977832979386864, 4.068188828216064) 

#mid - first
p1 = NXOpen.Point3d(-35.492352226834214, 22.977832979386864, 4.068188828216064) 
p2 = NXOpen.Point3d(-23.797783235633485, 12.977580455591582, -0.8917402042797428)

line1 = workPart.Curves.CreateLine(p1,p2)





