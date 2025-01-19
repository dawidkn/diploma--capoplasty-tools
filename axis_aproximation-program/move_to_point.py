import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log

def move_to_point(workPart, body1, cog_pos):

    try:
        moveObjectBuilder1 = workPart.BaseFeatures.CreateMoveObjectBuilder(NXOpen.Features.MoveObject.Null)
        moveObjectBuilder1.TransformMotion.Option = NXOpen.GeometricUtilities.ModlMotion.Options.PointToPoint

        display_body = workPart.Bodies


        added1 = moveObjectBuilder1.ObjectToMoveObject.Add(body1)

        unit1 = moveObjectBuilder1.TransformMotion.RadialOriginDistance.Units
        expression29 = workPart.Expressions.CreateSystemExpressionWithUnits(str(cog_pos[0]), unit1)
        
        scalar13 = workPart.Scalars.CreateScalarExpression(expression29, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        
        expression30 = workPart.Expressions.CreateSystemExpressionWithUnits(str(cog_pos[1]), unit1)
        
        scalar14 = workPart.Scalars.CreateScalarExpression(expression30, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        
        expression31 = workPart.Expressions.CreateSystemExpressionWithUnits(str(cog_pos[2]), unit1)
        
        scalar15 = workPart.Scalars.CreateScalarExpression(expression31, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        
        point5 = workPart.Points.CreatePoint(scalar13, scalar14, scalar15, NXOpen.SmartObject.UpdateOption.WithinModeling)


        moveObjectBuilder1.TransformMotion.FromPoint = point5



        
        expression51 = workPart.Expressions.CreateSystemExpressionWithUnits("0.00000000000", unit1)
        
        scalar22 = workPart.Scalars.CreateScalarExpression(expression51, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        
        expression52 = workPart.Expressions.CreateSystemExpressionWithUnits("0.00000000000", unit1)
        
        scalar23 = workPart.Scalars.CreateScalarExpression(expression52, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        
        expression53 = workPart.Expressions.CreateSystemExpressionWithUnits("0.00000000000", unit1)
        
        scalar24 = workPart.Scalars.CreateScalarExpression(expression53, NXOpen.Scalar.DimensionalityType.NotSet, NXOpen.SmartObject.UpdateOption.WithinModeling)
        
        point8 = workPart.Points.CreatePoint(scalar22, scalar23, scalar24, NXOpen.SmartObject.UpdateOption.WithinModeling)



        moveObjectBuilder1.TransformMotion.ToPoint = point8

        nXObject1 = moveObjectBuilder1.Commit()

    except NXOpen.NXException as ex:
        log("move to point:", "impossible to move body")
        ex.AssertErrorCode(1050029)


