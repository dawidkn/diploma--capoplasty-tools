#this functions are responsible for - create splines from section -> create extrude from those splines with 0 thk ->
# ->measure area (return result)-> remove extrude and splines
import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log
import time
import NXOpen.Annotations
import NXOpen.Drawings

def create_spline(workPart):
    Sections = workPart.DynamicSections
    for dynamicSection1 in Sections:
        dynamicSectionBuilder1 = workPart.DynamicSections.CreateSectionBuilder(dynamicSection1, NXOpen.ModelingView.Null)
        workPart.ModelingViews.WorkView.SetDynamicSectionVisible(dynamicSection1, True)    
        dynamicSectionBuilder1.SaveCurves(None)
        workPart.ModelingViews.WorkView.SetDynamicSectionVisible(dynamicSection1, False)

def create_extrude(workPart):
    extrudeBuilder1 = workPart.Features.CreateExtrudeBuilder(NXOpen.Features.Feature.Null)

    unit1 = extrudeBuilder1.Draft.FrontDraftAngle.Units

    extrudeBuilder1.BooleanOperation.Type = NXOpen.GeometricUtilities.BooleanOperation.BooleanType.Create
    section1 = workPart.Sections.CreateSection(0.0094999999999999998, 0.01, 0.5)
    extrudeBuilder1.Section = section1

    extrudeBuilder1.Limits.StartExtend.Value.SetFormula("0")
    extrudeBuilder1.Limits.EndExtend.Value.SetFormula("0")

    section1.DistanceTolerance = 0.01
    lines = workPart.Lines
    for line in lines:
        lineObj = []
        lineObj.append(line)
        selectionIntentRuleOptions = workPart.ScRuleFactory.CreateRuleOptions()

        selectionIntentRuleOptions.SetSelectedFromInactive(False)
        curveDumbRule = workPart.ScRuleFactory.CreateRuleBaseCurveDumb(lineObj, selectionIntentRuleOptions)
        rules = [None] * 1 
        rules[0] = curveDumbRule
        helpPoint = NXOpen.Point3d(0.0, 0.0, 0.0)

        section1.AddToSection(rules, NXOpen.NXObject.Null, NXOpen.NXObject.Null, NXOpen.NXObject.Null, helpPoint, NXOpen.Section.Mode.Create, False)

    splines = workPart.Splines
    
    for spline in splines:
        splObj = []
        splObj.append(spline)

        selectionIntentRuleOptions = workPart.ScRuleFactory.CreateRuleOptions()
    
        selectionIntentRuleOptions.SetSelectedFromInactive(False)
        curveDumbRule = workPart.ScRuleFactory.CreateRuleBaseCurveDumb(splObj, selectionIntentRuleOptions)
        rules = [None] * 1 
        rules[0] = curveDumbRule
        helpPoint = NXOpen.Point3d(0.0, 0.0, 0.0)

        section1.AddToSection(rules, NXOpen.NXObject.Null, NXOpen.NXObject.Null, NXOpen.NXObject.Null, helpPoint, NXOpen.Section.Mode.Create, False)


    origin1 = NXOpen.Point3d(-9.8446232789497294, -2.58990454796721, 6.3232252947931977)

    vector1 = NXOpen.Vector3d(0.0, 0.0, 1.0)
    direction1 = workPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.WithinModeling)
    extrudeBuilder1.Direction = direction1

    feature1 = extrudeBuilder1.CommitFeature()

def measureSurface(theSession,workPart):
    workPart.MeasureManager.SetPartTransientModification()
    scCollector1 = workPart.ScCollectors.CreateCollector()
    scCollector1.SetMultiComponent()
    workPart.MeasureManager.SetPartTransientModification()

    selectionIntentRuleOptions = workPart.ScRuleFactory.CreateRuleOptions()
    selectionIntentRuleOptions.SetSelectedFromInactive(False)

    extrudes = workPart.Features
    faces = [NXOpen.Face.Null] * 1
    temp_f = []
    for extrude in extrudes:
        temp_f.append(extrude)
    
    faces[0]=temp_f[1]

    temp_f2 = faces[0]
    
    temp_f = temp_f2.GetFaces()


    area1 = theSession.Measurement.GetFaceProperties(temp_f, 0.98999999999999999, NXOpen.Measurement.AlternateFace.Radius, True)

    # log("sheet area: ",area1[0])
    return area1[0]

def reamove_extrude_and_splines(theSession,workPart):
    #---reamove extrude
    extrudes = workPart.Features
    faces = [NXOpen.Face.Null] * 1 
    for extrude in extrudes:
        faces.append(extrude)
    
    del faces[0]
    del faces[0]

    nErrs1 = theSession.UpdateManager.AddObjectsToDeleteList(faces)
    
    id1 = theSession.NewestVisibleUndoMark
    nErrs2 = theSession.UpdateManager.DoUpdate(id1)

    #---reamove splines and lines
    splines = workPart.Splines
    splObj = []

    lines = workPart.Lines
    lineObj = []
    for line in lines:
        lineObj.append(line)

    nErrs1 = theSession.UpdateManager.AddObjectsToDeleteList(lineObj)
    id1 = theSession.NewestVisibleUndoMark
    nErrs2 = theSession.UpdateManager.DoUpdate(id1)

    for spline in splines:
        splObj.append(spline)

    nErrs1 = theSession.UpdateManager.AddObjectsToDeleteList(splObj)
    id1 = theSession.NewestVisibleUndoMark
    nErrs2 = theSession.UpdateManager.DoUpdate(id1)


def main() : 
    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    reamove_extrude_and_splines(theSession,workPart)
    create_spline(workPart)
    create_extrude(workPart)
    area = measureSurface(theSession,workPart)
    reamove_extrude_and_splines(theSession,workPart)


   
    return area


if __name__ == '__main__':
    a = main()