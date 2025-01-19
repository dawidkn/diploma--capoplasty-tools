def measureSurface(theSession,workPart):
    workPart.MeasureManager.SetPartTransientModification()
    scCollector1 = workPart.ScCollectors.CreateCollector()
    scCollector1.SetMultiComponent()
    workPart.MeasureManager.SetPartTransientModification()

    selectionIntentRuleOptions = workPart.ScRuleFactory.CreateRuleOptions()
    selectionIntentRuleOptions.SetSelectedFromInactive(False)

    extrudes = workPart.Features
    # log("extrude len", len(extrudes))
    faces = [NXOpen.Face.Null] * 1
    temp_f = []
    for extrude in extrudes:
        # temp1 = extrude.GetFaces()
        temp_f.append(extrude)
    
    log("temp_f len 1", len(temp_f))
    log("temp_f 1", temp_f)
    del faces[1] #removed faces from bone 


    temp_f = faces[1]


    log("temp", temp_f)

    faces2 = [NXOpen.Face.Null] * len(temp_f)
    log("faces2 len", len(faces2))
    log("faces2", faces2)

    i=0
    for face in temp_f:
        faces2[i]=face
        i=+1
    # log("faces2", faces2)
    area1 = theSession.Measurement.GetFaceProperties(faces2, 0.98999999999999999, NXOpen.Measurement.AlternateFace.Radius, True)

    log("sheet area: ",area1)