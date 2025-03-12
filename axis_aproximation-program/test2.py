import NXOpen
import NXOpen.UF
from logs_and_save.logs import log, errorLog, errorExit
import traceback
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log
import time
import NXOpen.Annotations
import NXOpen.Drawings

theSession  = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work
try:
        boundedPlaneBuilder1 = workPart.Features.CreateBoundedPlaneBuilder(NXOpen.Features.BoundedPlane.Null)
        boundedPlaneBuilder1.BoundingCurves.SetAllowedEntityTypes(NXOpen.Section.AllowTypes.OnlyCurves)
        selectionIntentRuleOptions1 = workPart.ScRuleFactory.CreateRuleOptions()
        selectionIntentRuleOptions1.SetSelectedFromInactive(False)
        splines = workPart.Splines
        lines = workPart.Lines
        boundedPlaneBuilder1.BoundingCurves.AllowSelfIntersection(False)
        boundedPlaneBuilder1.BoundingCurves.AllowDegenerateCurves(True)
        rules1 = [None] * 1 
        for line in lines:
            lineObj = []
            spLenght = line.GetLength()
            if spLenght <0.3:
                continue
            else:
                lineObj.append(line)
                curveDumbRule1 = workPart.ScRuleFactory.CreateRuleBaseCurveDumb(lineObj, selectionIntentRuleOptions1)
                rules1 = [None] * 1 
                rules1[0] = curveDumbRule1
                helpPoint1 = NXOpen.Point3d(0.0, 0.0, 0.0)
                boundedPlaneBuilder1.BoundingCurves.AddToSection(rules1, NXOpen.NXObject.Null, NXOpen.NXObject.Null, NXOpen.NXObject.Null, helpPoint1, NXOpen.Section.Mode.Create, False)
        for spline in splines:
            splObj = []
            spLenght = spline.GetLength()
            if spLenght <0.3:
                continue
            else:
                splObj.append(spline)
                curveDumbRule1 = workPart.ScRuleFactory.CreateRuleBaseCurveDumb(splObj, selectionIntentRuleOptions1)
                rules1 = [None] * 1 
                rules1[0] = curveDumbRule1
                helpPoint1 = NXOpen.Point3d(0.0, 0.0, 0.0)

                boundedPlaneBuilder1.BoundingCurves.AddToSection(rules1, NXOpen.NXObject.Null, NXOpen.NXObject.Null, NXOpen.NXObject.Null, helpPoint1, NXOpen.Section.Mode.Create, False)
        nXObject1 = boundedPlaneBuilder1.Commit()
except:
    try:
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
            extrudeBuilder1.DistanceTolerance = 0.04
            section1.AddToSection(rules, NXOpen.NXObject.Null, NXOpen.NXObject.Null, NXOpen.NXObject.Null, helpPoint, NXOpen.Section.Mode.Create, False)

        origin1 = NXOpen.Point3d(-9.8446232789497294, -2.58990454796721, 6.3232252947931977)
        vector1 = NXOpen.Vector3d(0.0, 0.0, 1.0)
        direction1 = workPart.Directions.CreateDirection(origin1, vector1, NXOpen.SmartObject.UpdateOption.WithinModeling)
        extrudeBuilder1.Direction = direction1

        feature1 = extrudeBuilder1.CommitFeature()
    except Exception as ex:
        errorLog()
        errorExit()
