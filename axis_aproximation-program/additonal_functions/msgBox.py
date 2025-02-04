import NXOpen
import NXOpen.UF


def msgBox(name, value):
    theUI = NXOpen.UI.GetUI()
    theNxMessageBox = theUI.NXMessageBox
    theNxMessageBox.Show(name, NXOpen.NXMessageBox.DialogType.Information,str(value))

def inputBox(text):
    theUfSession  = NXOpen.UF.UFSession.GetUFSession()
    theUI = NXOpen.UI.GetUI()
    theUI.LockAccess()
    ret = theUfSession.Ui.AskStringInput("Enter String",text)
    theUI.UnlockAccess()
    return ret