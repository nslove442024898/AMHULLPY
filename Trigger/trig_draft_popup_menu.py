## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          trig_draft_popup_menu.py
#
#      PURPOSE:
#          Implementation of context menu
#

import kcs_util
import kcs_gui
import kcs_draft

import KcsPoint2D
import KcsModel
import KcsElementHandle
import os

import KcsPythonUtil
util = KcsPythonUtil.PythonUtil()
util.AppendPythonPath(os.path.dirname(__file__)+'\\..\\Context_Menu')

def ParseArguments(args):

    # create common 'Context' variables in kcs_draft module
    kcs_draft.ContextPoint         = None
    kcs_draft.ContextElement       = None
    kcs_draft.ContextModel         = None
    kcs_draft.ContextSubpictures   = []

    # try to get point, closest geometry and model information
    if len(args)==3:
        if isinstance(args[2], KcsPoint2D.Point2D):
            kcs_draft.ContextPoint = args[2]
            try:
                # find geometry element
                kcs_draft.ContextElement = kcs_draft.geometry_identify(kcs_draft.ContextPoint)

                # get subpictures
                try:
                    kcs_draft.ContextSubpictures.insert(0, kcs_draft.element_parent_get(kcs_draft.ContextElement))
                    kcs_draft.ContextSubpictures.insert(0, kcs_draft.element_parent_get(kcs_draft.ContextSubpictures[0]))
                    kcs_draft.ContextSubpictures.insert(0, kcs_draft.element_parent_get(kcs_draft.ContextSubpictures[0]))
                except Exception, e:
                    print e

                # get model information
                kcs_draft.ContextModel = kcs_draft.model_properties_get(kcs_draft.ContextElement, KcsModel.Model())
            except:
                pass
    elif len(args)==2:
        if isinstance(args[1], KcsElementHandle.ElementHandle):
            try:
                kcs_draft.ContextSubpictures.insert(0, args[1])
                kcs_draft.ContextSubpictures.insert(0, kcs_draft.element_parent_get(kcs_draft.ContextSubpictures[0]))
                kcs_draft.ContextSubpictures.insert(0, kcs_draft.element_parent_get(kcs_draft.ContextSubpictures[0]))
            except:
                pass

#-------------------------------------------------------------------------------------------------------------
def pre(*args):                             # pre trigger definition

    # get arguments information
    ParseArguments(args)

    itemindex = 0

    # add ModelInfo item
    if kcs_draft.ContextModel != None:
        kcs_gui.menu_item_usr_add(args[0], itemindex, "Model &Info", "ctx_menu2")
        itemindex = itemindex + 1

    # add Delete item
    if len(kcs_draft.ContextSubpictures):
        kcs_gui.menu_item_usr_add(args[0], itemindex, "&Delete", "ctx_menu1")
        itemindex = itemindex + 1

    # add Subpicture Properties item
    if len(kcs_draft.ContextSubpictures):
        kcs_gui.menu_item_usr_add(args[0], itemindex, "&Subpicture properties", "ctx_menu7")
        itemindex = itemindex + 1

    # add element properties and 'Move' items
    if kcs_draft.ContextElement != None:
        if kcs_draft.element_is_text(kcs_draft.ContextElement):
            kcs_gui.menu_item_usr_add(args[0], itemindex, "&Text properties", "ctx_menu3")
            itemindex += 1
            kcs_gui.menu_item_usr_add(args[0], itemindex, "&Move Text", "ctx_menu6")
            itemindex + 1
        elif kcs_draft.element_is_contour(kcs_draft.ContextElement):
            kcs_gui.menu_item_usr_add(args[0], itemindex, "&Contour properties", "ctx_menu5")
            itemindex + 1
        elif kcs_draft.element_is_symbol(kcs_draft.ContextElement):
            kcs_gui.menu_item_usr_add(args[0], itemindex, "&Symbol properties", "ctx_menu4")
            itemindex += 1
            kcs_gui.menu_item_usr_add(args[0], itemindex, "&Move Symbol", "ctx_menu6")
            itemindex + 1

    kcs_gui.menu_item_usr_add(args[0], itemindex, "&Move view", "ctx_menu8")
    itemindex += 1

    if len(kcs_draft.ContextSubpictures) >= 2:
        kcs_gui.menu_item_usr_add(args[0], itemindex, "&Move subview", "ctx_menu9")
        itemindex += 1

    return kcs_util.trigger_ok()

