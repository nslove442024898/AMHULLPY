## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft20.py
#
#      PURPOSE:
#
#          This example program prints handle to selected view, subview, or component
#				1. closest to selected point
#				2. selected by name
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import KcsStringlist

#-------------------------------------------------------------------------------------------------------------
def GetEntityHandle(elementkind, criteria):             # function calls corresponding identify function
    handle = -1                                         # and returns handle to founded entity

    # call corresponding function
    if elementkind == 1:
        handle = kcs_draft.view_identify(criteria)      # view
    elif elementkind == 2:
        handle = kcs_draft.subview_identify(criteria)   # subview
    elif elementkind == 3:
        handle = kcs_draft.component_identify(criteria) # component

    assert handle!=-1
    return handle

#-------------------------------------------------------------------------------------------------------------
def FindEntity(elementkind, criteria):                  # function gets entity handle and reports it on screen
    try:                                                # if entity not found reports a message

        kcs_draft.highlight_off(0)                      # highlight off all highlighted entities

        handle = GetEntityHandle(elementkind, criteria) # get entity handle

        kcs_draft.element_highlight(handle)             # highlight founded entity

        try:                                            # display result
            print 'entity handle:', handle
            kcs_ui.message_noconfirm('entity handle: '+str(handle))

        except:
            print kcs_ui.error

    except:
        print kcs_draft.error

        if kcs_draft.error == 'kcs_ViewNotFound':       # corresponding message if entity not found
            kcs_ui.message_noconfirm('view not found')
        elif kcs_draft.error == 'kcs_SubviewNotFound':
            kcs_ui.message_noconfirm('subview not found')
        elif kcs_draft.error == 'kcs_ComponentNotFound':
            kcs_ui.message_noconfirm('component not found')
        return

#-------------------------------------------------------------------------------------------------------------
def EntityFromPoint(elementkind):                   # funtion gets point and calls searching for entity
    try:
        point = KcsPoint2D.Point2D()
    except:
        print KcsPoint2D.error

    prompt = ''

    if elementkind == 1:                            # select corresponding prompt
        prompt = 'Indicate view, OC to exit'
    elif elementkind == 2:
        prompt = 'Indicate subview, OC to exit'
    elif elementkind == 3:
        prompt = 'Indicate component, OC to exit'

    result = 1
    while result:
        resp = kcs_ui.point2D_req(prompt, point)    # request user for point
        if resp[0] == kcs_util.ok():
            FindEntity(elementkind, point)          # find entity
        else:
            result = 0

    return

#-------------------------------------------------------------------------------------------------------------
def EntityFromName(elementkind):                    # select by name
    prompt = ''

    if elementkind == 1:                            # select corresponding prompt
        prompt = 'View name'
    elif elementkind == 2:
        prompt = 'Subview name'
    elif elementkind == 3:
        prompt = 'Component name'

    result = 1

    while result:
        (status, name) = kcs_ui.string_req(prompt, "")  # request user for name
        if status == kcs_util.ok():
            FindEntity(elementkind, name)               # find entity
        else:
            result = 0

    return

#-------------------------------------------------------------------------------------------------------------
def GetSelectionMethod(elementkind):                      # function gets selection method and select entity
    try:
        # build options list
        actions = KcsStringlist.Stringlist('closest to point')
        actions.AddString('selected by name')
    except:
        print KcsStringlist.error

    # get user choice and select entity
    result = 1
    try:
        while result:
            res = kcs_ui.choice_select('Method selection', 'Select method:', actions)
            if res[0] == kcs_util.ok():
                method = res[1]
                if method == 1:
                    EntityFromPoint(elementkind)
                else:
                    EntityFromName(elementkind)
            else:
                result = 0
    except:
        print kcs_ui.error

    return


# get user choice and select entity
try:
    try:
        # build elements kind list
        actions = KcsStringlist.Stringlist('view identify')
        actions.AddString('subview identify')
        actions.AddString('component identify')
    except:
        print KcsStringlist.error

    result = 1
    while result:
        res = kcs_ui.choice_select('Get identify', 'Select element kind', actions)
        if res[0]==kcs_util.ok():
            GetSelectionMethod(res[1])
        else:
            result = 0

    kcs_ui.message_noconfirm('Script interrupted')
    kcs_draft.highlight_off(0)                      # highlight off all highlighted entities

except:
    print kcs_ui.error
    kcs_draft.highlight_off(0)                      # highlight off all highlighted entities
