# NX 2011
# Journal created by dawid on Wed Mar 19 22:47:19 2025 Środkowoeuropejski czas stand.

#
import math
import NXOpen
def main() : 

    theSession  = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    displayPart = theSession.Parts.Display
    # ----------------------------------------------
    #   Menu: View->Section->Clip Section
    # ----------------------------------------------
    workPart.ModelingViews.WorkView.DisplaySectioningToggle = False
    
    # ----------------------------------------------
    #   Menu: Tools->Journal->Stop Recording
    # ----------------------------------------------
    
if __name__ == '__main__':
    main()