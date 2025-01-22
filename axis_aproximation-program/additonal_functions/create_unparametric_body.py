# NX 2011
# Journal created by dawid on Tue Jan 21 20:46:52 2025 Środkowoeuropejski czas stand.

#
import math
import NXOpen
from datetime import datetime
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: File->Export->STEP...
    # ----------------------------------------------
    markId1 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Visible, "Start")
    
    stepCreator1 = theSession.DexManager.CreateStepCreator()
    
    stepCreator1.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap214
    
    stepCreator1.ExportFrom = NXOpen.StepCreator.ExportFromOption.ExistingPart
    
    stepCreator1.SettingsFile = "C:\\Program Files\\Siemens\\NX2007\\step203ug\\ugstep203.def"
    
    stepCreator1.ObjectTypes.Csys = True
    
    stepCreator1.ExportAs = NXOpen.StepCreator.ExportAsOption.Ap203
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")
    stepCreator1.InputFile = "C:\\Users\\dawid\\Desktop\\praca magisterska\\modele kosci\\only_head_ver"+current_datetime+".prt"
    
    theSession.SetUndoMarkName(markId1, "Export STEP File Dialog")
    
    stepCreator1.ObjectTypes.Csys = False
    
    markId2 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Export STEP File")
    
    theSession.DeleteUndoMark(markId2, None)
    
    markId3 = theSession.SetUndoMark(NXOpen.Session.MarkVisibility.Invisible, "Export STEP File")
    current_datetime = datetime.now().strftime("%Y-%m-%d-%H-%M")
    stepCreator1.OutputFile = "C:\\Users\\dawid\\Desktop\\praca magisterska\\modele kosci\\only_head_ver"+current_datetime+".stp"
    
    stepCreator1.FileSaveFlag = False
    
    stepCreator1.LayerMask = "1-256"
    
    stepCreator1.ProcessHoldFlag = True
    
    nXObject1 = stepCreator1.Commit()
    
    theSession.DeleteUndoMark(markId3, None)
    
    theSession.SetUndoMarkName(markId1, "Export STEP File")
    
    stepCreator1.Destroy()
    
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()