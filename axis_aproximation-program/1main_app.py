import NXOpen
import NXOpen.UF
import math
import logs_and_save.save_and_read as sar
from logs_and_save.logs import log,errorLog, errorExit
from move_to_point import move_to_point
from read_cog import read_cog
from additonal_functions.msgBox import msgBox
import determinate_first_vector as CS
import head_axies_aproximation as HA
import sys
import NXOpen.Annotations

    

theSession = NXOpen.Session.GetSession()
workPart = theSession.Parts.Work

display_body = workPart.Bodies

for solid_body in display_body:
    if solid_body and isinstance(solid_body, NXOpen.Body):

        body1 = [solid_body]

        COG_Pos = read_cog(theSession, body1)
        log("Status_main", "COG_Pos: " + str(COG_Pos))
        move_to_point(workPart, body1, COG_Pos)
        log("Status_main", "move_to_point")


        origin, min_list, axisorigin = CS.basePlanedef(theSession,workPart)

        HA.correction(workPart, axisorigin, origin, min_list)
        
        msgBox("This is the END", "Work in progress")
        sys.exit()
        break

    else:
        log("Status_main", "body do not exist")
        errorLog()
        errorExit()
sys.exit()

