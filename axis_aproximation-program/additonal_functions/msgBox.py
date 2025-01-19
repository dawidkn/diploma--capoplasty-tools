import NXOpen.UF

def msgBox(name, value):
    theUI = NXOpen.UI.GetUI()
    theNxMessageBox = theUI.NXMessageBox
    theNxMessageBox.Show(name, NXOpen.NXMessageBox.DialogType.Information,str(value))