## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_ui
import kcs_gui
import kcs_util
import munModelUnitMenu

# =============================================================================================#
# Name :
#       muntrig_draft_init.py
# Purpose:
#     This file contains the code snippet that should be included in the
#       Initialization trigger of Structure Modelling Application in the respective functions
#       as below
#===============================================================================================#




def pre(*args):
    return  kcs_util.trigger_ok()



def post(*args):
    menu=munModelUnitMenu.CModelUnitMenu(10,"Model &Unit")
    menu.CreateMenu()
    menu.CreateDefineModelUnitMenu(0,"&Define Model Unit","munDefineModelUnit")
    menu.CreateUnDefineModelUnitMenu(1,"&UnDefine Model Unit","munUnDefineModelUnit")
    menu.CreateHighLightModelUnitMenu(2,"&High Light","munHighlightModelUnit")
    menu.CreateUnHighLightModelUnitMenu(3,"U&nHighLight","munUnHighLightModelUnit")
    return  kcs_util.trigger_ok()




