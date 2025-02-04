# NX 2011
# Journal created by dawid on Thu Jan 23 00:22:14 2025 Środkowoeuropejski czas stand.

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
    
    dynamicSectionBuilder1.DefaultPlaneAxis = NXOpen.Display.DynamicSectionTypes.Axis.Y
    
    theSession.SetUndoMarkName(markId1, "View Section Dialog")
    
    plane1.SetMethod(NXOpen.PlaneTypes.MethodType.Coincident)
    
    dynamicSectionBuilder1.ShowClip = True
    
    dynamicSectionBuilder1.CsysType = NXOpen.Display.DynamicSectionTypes.CoordinateSystem.Absolute
    
    dynamicSectionBuilder1.DefaultPlaneAxis = NXOpen.Display.DynamicSectionTypes.Axis.Y
    
    mincornerpt1 = NXOpen.Point3d(-60.255600193708496, -44.016079119072714, -32.377705747405351)
    maxcornerpt1 = NXOpen.Point3d(84.90093628673371, 50.138897959776926, 38.16860111486556)
    dynamicSectionBuilder1.SetBoundingBox(mincornerpt1, maxcornerpt1)
    
    dynamicSectionBuilder1.DeferCurveUpdate = False
    
    dynamicSectionBuilder1.ShowCurvePreview(True)
    
    rotationmatrix1 = NXOpen.Matrix3x3()
    
    rotationmatrix1.Xx = 0.0
    rotationmatrix1.Xy = -1.0
    rotationmatrix1.Xz = 0.0
    rotationmatrix1.Yx = 0.99619469809174555
    rotationmatrix1.Yy = 0.0
    rotationmatrix1.Yz = 0.087155742747658096
    rotationmatrix1.Zx = -0.087155742747658096
    rotationmatrix1.Zy = 0.0
    rotationmatrix1.Zz = 0.99619469809174555
    dynamicSectionBuilder1.SetRotationMatrix(NXOpen.Display.DynamicSectionTypes.Axis.NotSet, rotationmatrix1)
    
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