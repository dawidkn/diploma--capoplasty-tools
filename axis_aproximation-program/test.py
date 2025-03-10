# NX 2011
# Journal created by dawid on Mon Mar 10 22:27:20 2025 Środkowoeuropejski czas stand.

#
import math
import NXOpen
import NXOpen.Features
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
  
    boundedPlaneBuilder1 = workPart.Features.CreateBoundedPlaneBuilder(NXOpen.Features.BoundedPlane.Null)
    boundedPlaneBuilder1.BoundingCurves.SetAllowedEntityTypes(NXOpen.Section.AllowTypes.OnlyCurves)
    selectionIntentRuleOptions1 = workPart.ScRuleFactory.CreateRuleOptions()
    selectionIntentRuleOptions1.SetSelectedFromInactive(False)
    splines = workPart.Splines
    lines = workPart.Lines
    boundedPlaneBuilder1.BoundingCurves.AllowSelfIntersection(False)
    boundedPlaneBuilder1.BoundingCurves.AllowDegenerateCurves(False)
    for line in lines:
        lineObj = []
        lineObj.append(line)
        curveDumbRule1 = workPart.ScRuleFactory.CreateRuleBaseCurveDumb(lineObj, selectionIntentRuleOptions1)
        rules1 = [None] * 1 
        rules1[0] = curveDumbRule1
        helpPoint1 = NXOpen.Point3d(0.0, 0.0, 0.0)
        boundedPlaneBuilder1.BoundingCurves.AddToSection(rules1, NXOpen.NXObject.Null, NXOpen.NXObject.Null, NXOpen.NXObject.Null, helpPoint1, NXOpen.Section.Mode.Create, True)
    for spline in splines:
        splObj = []
        splObj.append(spline)
        curveDumbRule1 = workPart.ScRuleFactory.CreateRuleBaseCurveDumb(splObj, selectionIntentRuleOptions1)
        rules1 = [None] * 1 
        rules1[0] = curveDumbRule1
        helpPoint1 = NXOpen.Point3d(0.0, 0.0, 0.0)
        boundedPlaneBuilder1.BoundingCurves.AddToSection(rules1, NXOpen.NXObject.Null, NXOpen.NXObject.Null, NXOpen.NXObject.Null, helpPoint1, NXOpen.Section.Mode.Create, True)
    nXObject1 = boundedPlaneBuilder1.Commit()
    

    extrudes = workPart.Features
    faces = [NXOpen.Face.Null] * 1 
    for extrude in extrudes:
        faces.append(extrude)

    nErrs1 = theSession.UpdateManager.AddObjectsToDeleteList(faces)
    
    id1 = theSession.NewestVisibleUndoMark
    nErrs2 = theSession.UpdateManager.DoUpdate(id1)
if __name__ == '__main__':
    main()