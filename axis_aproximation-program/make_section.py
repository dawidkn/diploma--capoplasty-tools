import math
import NXOpen
import NXOpen.Display
import time
from measure_area import main as measure
from logs_and_save.logs import log

def make_sec(workPart) : 


    dynamicSectionBuilder1 = workPart.DynamicSections.CreateSectionBuilder(workPart.ModelingViews.WorkView)
    
    dynamicSectionBuilder1.ShowClip = True

    sectionArea = [0,0,0]

    dynamicSectionBuilder1.PlaneX() 
    nXObject1 = dynamicSectionBuilder1.Commit()
    sectionArea[0] = measure()

    dynamicSectionBuilder1.PlaneY() 
    nXObject1 = dynamicSectionBuilder1.Commit()
    sectionArea[1] = measure()

    dynamicSectionBuilder1.PlaneZ() #to change the plane of section, change z to x or y
    nXObject1 = dynamicSectionBuilder1.Commit()
    sectionArea[2] = measure()
    
    dynamicSectionBuilder1.ShowClip = False
    log("sections area:", sectionArea)
