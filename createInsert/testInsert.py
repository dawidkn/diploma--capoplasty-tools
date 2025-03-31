
import math
import NXOpen
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display

    
    displayModification1 = theSession.DisplayManager.NewDisplayModification()
    
    displayModification1.ApplyToAllFaces = True
    
    displayModification1.ApplyToOwningParts = False
    
    displayModification1.NewColor = 186
    
    objects1 = [NXOpen.DisplayableObject.Null] * 1 
    body1 = workPart.Bodies.FindObject("CYLINDER(10681)")
    objects1[0] = body1
    displayModification1.Apply(objects1)
    
    displayModification1.Dispose()

    
if __name__ == '__main__':
    main()