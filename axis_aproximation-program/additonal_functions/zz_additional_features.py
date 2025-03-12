import NXOpen
import NXOpen.UF

def get_extreme_points(body):
    theUI = NXOpen.UI.GetUI()
    theUfSession = NXOpen.UF.UFSession.GetUFSession()
    bounding_box = theUfSession.ModlGeneral.AskBoundingBoxExact(body.Tag, 0)
    
    log("points",bounding_box)
    min_point = bounding_box.MinPoint
    max_point = bounding_box.MaxPoint
    

    return [max_point.X,
        min_point.X,
        max_point.Y,
        min_point.Y,
        max_point.Z,
        min_point.Z]

extreme_points = get_extreme_points(solid_body)


time.sleep(2)

def hide_body():
        # #-----------hide body--------
    #this function hiding first body in tree

    body1 = workPart.Bodies
    bodys = []
    for body in body1:
        bodys.append(body)
        break
    theSession.DisplayManager.BlankObjects(bodys)

def show_body():
     # #-----show body-----
    theSession.DisplayManager.ShowObjects(bodys, NXOpen.DisplayManager.LayerSetting.ChangeLayerToSelectable)


def getLenghtline(line):
    spLenght = line.GetLength()

if __name__ == '__main__':
    main()