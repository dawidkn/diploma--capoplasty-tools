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


def YNBox(info, title):
    the_ui = NXOpen.UI.GetUI()
    response = the_ui.NXMessageBox.Show(info, NXOpen.NXMessageBox.DialogType.Question, title)
    return response