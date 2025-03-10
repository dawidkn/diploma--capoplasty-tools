# NX 2011
# Journal created by dawid on Mon Mar 10 22:41:31 2025 Środkowoeuropejski czas stand.

#
import math
import NXOpen
import NXOpen.Features
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: Edit->Delete...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Delete")
    
    theSession.UpdateManager.ClearErrorList()
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Delete")
    
    objects1 = [NXOpen.TaggedObject.Null] * 1 
    boundedPlane1 = workPart.Features.FindObject("BOUNDED_PLANE(3539)")
    objects1[0] = boundedPlane1
    nErrs1 = theSession.UpdateManager.AddObjectsToDeleteList(objects1)
    
    id1 = theSession.NewestVisibleUndoMark
    
    nErrs2 = theSession.UpdateManager.DoUpdate(id1)
    
    theSession.DeleteUndoMark(markId1, None)
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()