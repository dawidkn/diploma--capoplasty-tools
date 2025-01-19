import math
import NXOpen
import NXOpen.Features

def main() : #create datum in 0,0,0

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    datumCsysBuilder1 = workPart.Features.CreateDatumCsysBuilder(NXOpen.Features.Feature.Null)
    
    origin5 = NXOpen.Point3d(0.0, 0.0, 0.0)
    xDirection1 = NXOpen.Vector3d(1.0, 0.0, 0.0)
    yDirection1 = NXOpen.Vector3d(0.0, 1.0, 0.0)
    xform1 = workPart.Xforms.CreateXform(origin5, xDirection1, yDirection1, NXOpen.SmartObject.UpdateOption.WithinModeling, 1.0)
    
    cartesianCoordinateSystem1 = workPart.CoordinateSystems.CreateCoordinateSystem(xform1, NXOpen.SmartObject.UpdateOption.WithinModeling)

    datumCsysBuilder1.Csys = cartesianCoordinateSystem1
    
    
    nXObject1 = datumCsysBuilder1.Commit()

if __name__ == '__main__':
    main()