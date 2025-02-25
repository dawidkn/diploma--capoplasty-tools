import NXOpen
import NXOpen.UF
import math
import logs_and_save.save_and_read as sar
from logs_and_save.logs import log
from move_to_point import move_to_point
from read_cog import read_cog
from additonal_functions.msgBox import msgBox
import determinate_first_vector as CS
import sys

    

def main():

    theSession = NXOpen.Session.GetSession()
    workPart = theSession.Parts.Work
    
    display_body = workPart.Bodies

    for solid_body in display_body:
        if solid_body and isinstance(solid_body, NXOpen.Body):

            body1 = [solid_body]

            COG_Pos = read_cog(theSession, body1)
            
            move_to_point(workPart, body1, COG_Pos)

            CS.basePlanedef(theSession,workPart)



        else:
            log("Status_main", "body do not exist")
            sys.exit(0)

if __name__ == "__main__":
    main()
