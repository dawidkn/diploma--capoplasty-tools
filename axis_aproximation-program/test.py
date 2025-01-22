# NX 2011
# Journal created by dawid on Tue Jan 21 23:42:49 2025 Środkowoeuropejski czas stand.

#
import math
import NXOpen
import NXOpen.Display
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: View->Section->Edit Section...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    dynamicSectionBuilder1 = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    
    dynamicSectionBuilder1.DeferCurveUpdate = True
    
    origin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
    normal1 = NXOpen.Vector3d(0.0, 0.0, 1.0)
    plane1 = workPart.Planes.CreatePlane(origin1, normal1, NXOpen.SmartObject.UpdateOption.WithinModeling)
    
    unit1 = workPart.UnitCollection.FindObject("MilliMeter")
    expression1 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    expression2 = workPart.Expressions.CreateSystemExpressionWithUnits("0", unit1)
    
    dynamicSectionBuilder1.SeriesSpacing = 3.0
    
    dynamicSectionBuilder1.DefaultPlaneAxis = NXOpen.Display.DynamicSectionTypes.Axis.Z
    
    theSession.SetUndoMarkName(markId1, "View Section Dialog")
    
    plane1.SetMethod(NXOpen.PlaneTypes.MethodType.Coincident)
    
    dynamicSectionBuilder1.ShowClip = True
    
    dynamicSectionBuilder1.CsysType = NXOpen.Display.DynamicSectionTypes.CoordinateSystem.Wcs
    
    dynamicSectionBuilder1.DefaultPlaneAxis = NXOpen.Display.DynamicSectionTypes.Axis.Z
    
    mincornerpt1 = NXOpen.Point3d(-46.602688414586432, -44.016079119072721, -65.546137218145446)
    maxcornerpt1 = NXOpen.Point3d(70.750402952048987, 50.138897959776905, 55.447465535290192)
    dynamicSectionBuilder1.SetBoundingBox(mincornerpt1, maxcornerpt1)
    
    dynamicSectionBuilder1.DeferCurveUpdate = False
    
    dynamicSectionBuilder1.ShowCurvePreview(True)
    
    geom1 = []
    plane1.SetGeometry(geom1)
    
    plane1.SetMethod(NXOpen.PlaneTypes.MethodType.FixedY)
    
    geom2 = []
    plane1.SetGeometry(geom2)
    
    origin2 = NXOpen.Point3d(0.0, 0.0, 0.0)
    plane1.Origin = origin2
    
    matrix1 = NXOpen.Matrix3x3()
    
    matrix1.Xx = 0.0
    matrix1.Xy = 0.0
    matrix1.Xz = 1.0
    matrix1.Yx = 1.0
    matrix1.Yy = 0.0
    matrix1.Yz = 0.0
    matrix1.Zx = 0.0
    matrix1.Zy = 1.0
    matrix1.Zz = 0.0
    plane1.Matrix = matrix1
    
    plane1.SetAlternate(NXOpen.PlaneTypes.AlternateType.One)
    
    plane1.Evaluate()
    
    plane1.SetMethod(NXOpen.PlaneTypes.MethodType.FixedY)
    
    dynamicSectionBuilder1.SetAssociativePlane(NXOpen.Plane.Null)
    
    axisorigin1 = NXOpen.Point3d(0.0, 0.0, 0.0)
    origin3 = NXOpen.Point3d(0.0, 0.0, 0.0)
    rotationmatrix1 = NXOpen.Matrix3x3()
    
    rotationmatrix1.Xx = 0.0
    rotationmatrix1.Xy = 0.0
    rotationmatrix1.Xz = -1.0
    rotationmatrix1.Yx = -1.0
    rotationmatrix1.Yy = 0.0
    rotationmatrix1.Yz = 0.0
    rotationmatrix1.Zx = 0.0
    rotationmatrix1.Zy = 1.0
    rotationmatrix1.Zz = 0.0
    dynamicSectionBuilder1.SetPlane(axisorigin1, origin3, rotationmatrix1)
    
    geom3 = []
    plane1.SetGeometry(geom3)
    
    plane1.SetMethod(NXOpen.PlaneTypes.MethodType.FixedZ)
    
    geom4 = []
    plane1.SetGeometry(geom4)
    
    origin4 = NXOpen.Point3d(0.0, 0.0, 0.0)
    plane1.Origin = origin4
    
    matrix2 = NXOpen.Matrix3x3()
    
    matrix2.Xx = 1.0
    matrix2.Xy = 0.0
    matrix2.Xz = 0.0
    matrix2.Yx = 0.0
    matrix2.Yy = 1.0
    matrix2.Yz = 0.0
    matrix2.Zx = 0.0
    matrix2.Zy = 0.0
    matrix2.Zz = 1.0
    plane1.Matrix = matrix2
    
    plane1.SetAlternate(NXOpen.PlaneTypes.AlternateType.One)
    
    plane1.Evaluate()
    
    plane1.SetMethod(NXOpen.PlaneTypes.MethodType.FixedZ)
    
    dynamicSectionBuilder1.SetAssociativePlane(NXOpen.Plane.Null)
    
    axisorigin2 = NXOpen.Point3d(0.0, 0.0, 0.0)
    origin5 = NXOpen.Point3d(0.0, 0.0, 0.0)
    rotationmatrix2 = NXOpen.Matrix3x3()
    
    rotationmatrix2.Xx = 0.0
    rotationmatrix2.Xy = 1.0
    rotationmatrix2.Xz = -0.0
    rotationmatrix2.Yx = -1.0
    rotationmatrix2.Yy = 0.0
    rotationmatrix2.Yz = 0.0
    rotationmatrix2.Zx = 0.0
    rotationmatrix2.Zy = 0.0
    rotationmatrix2.Zz = 1.0
    dynamicSectionBuilder1.SetPlane(axisorigin2, origin5, rotationmatrix2)
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "View Section")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "View Section")
    
    nXObject1 = dynamicSectionBuilder1.Commit()
    
    objects1 = dynamicSectionBuilder1.GetCommittedObjects()
    
    id1 = theSession.NewestVisibleUndoMark
    
    nErrs1 = theSession.UpdateManager.DoUpdate(id1)
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(id1, "View Section")
    
    objects2 = [NXOpen.TaggedObject.Null] * 1 
    objects2[0] = plane1
    nErrs2 = theSession.UpdateManager.AddObjectsToDeleteList(objects2)
    
    dynamicSectionBuilder1.Destroy()
    
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression2)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    try:
        # Expression is still in use.
        workPart.Expressions.Delete(expression1)
    except NXOpen.NXException as ex:
        ex.AssertErrorCode(1050029)
        
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()