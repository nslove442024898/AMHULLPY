## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft21.py
#
#      PURPOSE:
#
#          This example program prints handle to selected dimension, note, position number,
#          hatch, text, symbol, contour, point or geometry closest to selected point.
#

import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import KcsStringlist

#-------------------------------------------------------------------------------------------------------------
def GetElementHandle(elementkind, point):            # function calls corresponding identify function
    handle = -1                                      # and returns handle to founded element

    # call corresponding function
    if elementkind == 1:
        handle = kcs_draft.dim_identify(point)       # dimension
    elif elementkind == 2:
        handle = kcs_draft.note_identify(point)      # note
    elif elementkind == 3:
        handle = kcs_draft.posno_identify(point)     # position number
    elif elementkind == 4:
        handle = kcs_draft.hatch_identify(point)     # hatch
    elif elementkind == 5:
        handle = kcs_draft.text_identify(point)      # text
    elif elementkind == 6:
        handle = kcs_draft.symbol_identify(point)    # symbol
    elif elementkind == 7:
        handle = kcs_draft.contour_identify(point)   # contour
    elif elementkind == 8:
        handle = kcs_draft.point_identify(point)     # point
    elif elementkind == 9:
        handle = kcs_draft.geometry_identify(point)  # geometry

    return handle

#-------------------------------------------------------------------------------------------------------------
def FindElement(elementkind, point):                    # function gets element handle and reports it on screen
    try:                                                # if element not found reports a message

        kcs_draft.highlight_off(0)                      # highlight off all highlighted elements

        handle = GetElementHandle(elementkind, point)   # get element handle

        kcs_draft.element_highlight(handle)             # highlight founded element

        try:                                            # display result
            print 'element handle:', handle
            kcs_ui.message_noconfirm('element handle: '+str(handle))

        except:
            print kcs_ui.error
            return

    except:
        print kcs_draft.error
        if kcs_draft.error == 'kcs_NotFound':
            kcs_ui.message_noconfirm('kcs_NotFound')
        return

    return

#-------------------------------------------------------------------------------------------------------------
def ElementFromPoint(elementkind):                   # funtion gets point and calls searching for element
    try:
        point = KcsPoint2D.Point2D()
    except:
        print KcsPoint2D.error
        return

    prompt = ''

    if elementkind == 1:
        prompt = 'Indicate dimension, OC to exit'
    elif elementkind == 2:
        prompt = 'Indicate note, OC to exit'
    elif elementkind == 3:
        prompt = 'Indicate position number, OC to exit'
    elif elementkind == 4:
        prompt = 'Indicate hatch, OC to exit'
    elif elementkind == 5:
        prompt = 'Indicate text, OC to exit'
    elif elementkind == 6:
        prompt = 'Indicate symbol, OC to exit'
    elif elementkind == 7:
        prompt = 'Indicate contour, OC to exit'
    elif elementkind == 8:
        prompt = 'Indicate point, OC to exit'
    elif elementkind == 9:
        prompt = 'Indicate geometry, OC to exit'

    result = 1
    while result:
        resp = kcs_ui.point2D_req(prompt, point) # request user for point
        if resp[0] == kcs_util.ok():
            FindElement(elementkind, point)      # find element
        else:
            result = 0

    return

# get user choice and select element
try:
    # build elements kind list
    try:
        actions = KcsStringlist.Stringlist('dimension identify')
        actions.AddString('note identify')
        actions.AddString('position number identify')
        actions.AddString('hatch identify')
        actions.AddString('text identify')
        actions.AddString('symbol identify')
        actions.AddString('contour identify')
        actions.AddString('point identify')
        actions.AddString('geometry identify')
    except:
        print KcsStringlist.error

    result = 1
    while result:
        res = kcs_ui.choice_select('Get identify', 'Select element kind', actions)
        if res[0]==kcs_util.ok():
            elementkind = res[1]
            ElementFromPoint(elementkind)
        else:
            result = 0

    kcs_ui.message_noconfirm('Script interrupted')
    kcs_draft.highlight_off(0)                      # highlight off all highlighted elements

except:
    print kcs_ui.error
    kcs_draft.highlight_off(0)                      # highlight off all highlighted elements
