import math
import NXOpen
import NXOpen.Features
import NXOpen.GeometricUtilities
from logs_and_save.logs import log,errorLog, errorExit
from additonal_functions.msgBox import msgBox, inputBox, YNBox
import random

def changeColor(workPart, theSession):
    res = inputBox("Enter the name of the body to change color")
    index = res[0]
    log("Body name: ",res)
    bodies = workPart.Bodies
    bodies1 = []   
    for body in bodies:
        bodies1.append(body)

    rand = random.randint(0, 200)
    displayModification1 = theSession.DisplayManager.NewDisplayModification()
    
    displayModification1.ApplyToAllFaces = True
    
    displayModification1.ApplyToOwningParts = False
    
    displayModification1.NewColor = rand
    
    objects1 = [NXOpen.DisplayableObject.Null] * 1 
    objects1[0] = bodies1[int(index)]
    displayModification1.Apply(objects1)
    
    displayModification1.Dispose()

def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    changeColor(workPart, theSession)
    
if __name__ == '__main__':
    main()