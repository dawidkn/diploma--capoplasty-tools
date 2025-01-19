import NXOpen
import NXOpen.UF
import math

def read_cog(theSession, body1):

    massprops1, weight1, centroid1, centroidunit1, density1, axis1 = theSession.Measurement.GetBodyProperties(body1, 0.98999999999999999, False)
    convert = str(centroid1)


    convert = convert.strip("[]")

    parts = convert.split(",")

    x = float(parts[0].split("=")[1])
    y = float(parts[1].split("=")[1])
    z = float(parts[2].split("=")[1])

    return [x,y,z]