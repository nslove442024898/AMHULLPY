## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft23.py
#
#      PURPOSE:
#
#          This example program shows properties of selected texts, symbols and contours
#

import sys
import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import KcsStringlist
import KcsContour2D
import KcsColour
import KcsLinetype
import KcsLayer
import KcsSymbol
import KcsText

#-------------------------------------------------------------------------------------------------------------
def ShowSymbolProperties(symbol):                           # function displays properties of symbol
    try:
        properties = KcsStringlist.Stringlist('----------------- common -----------------------')
        if symbol.IsVisible():
            properties.AddString('Visible: True')
        else:
            properties.AddString('Visible: False')
        if symbol.IsDetectable():
            properties.AddString('Detectable: True')
        else:
            properties.AddString('Detectable: False')
        properties.AddString('Colour: ' + (symbol.GetColour()).Name())
        properties.AddString('Linetype: ' +(symbol.GetLineType()).Name())
        properties.AddString('Layer: ' + str((symbol.GetLayer()).GetLayer()))
        properties.AddString('---------------- specifics ---------------------')
        point = symbol.GetPosition()
        properties.AddString('Position:  X: ' + str(point.X) + '   Y: ' + str(point.Y))
        properties.AddString('Height: ' + str(symbol.GetHeight()))
        properties.AddString('Rotation: ' + str(symbol.GetRotation()))
        properties.AddString('FontId: ' + str(symbol.GetFontId()))
        properties.AddString('SymbolId: ' + str(symbol.GetSymbolId()))
        if symbol.IsReflected():
            properties.AddString('Reflection: No')
        elif symbol.IsReflectedInUAxis():
            properties.AddString('Reflection: in U axis')
        elif symbol.IsReflectedInVAxis():
            properties.AddString('Reflection: in V axis')
    except:
        print KcsStringlist.error

    try:
        kcs_ui.string_select('Symbol properties', '', '', properties)
    except:
        print kcs_ui.error

    return

#-------------------------------------------------------------------------------------------------------------
def ShowTextProperties(text):                               # function displays properties of text
    try:
        properties = KcsStringlist.Stringlist('----------------- common -----------------------')
        if text.IsVisible():
            properties.AddString('Visible: True')
        else:
            properties.AddString('Visible: False')
        if text.IsDetectable():
            properties.AddString('Detectable: True')
        else:
            properties.AddString('Detectable: False')
        properties.AddString('Colour: ' + (text.GetColour()).Name())
        properties.AddString('Linetype: ' +(text.GetLineType()).Name())
        properties.AddString('Layer: ' + str((text.GetLayer()).GetLayer()))
        properties.AddString('---------------- specifics ---------------------')
        point = text.GetPosition()
        properties.AddString('Text: ' + text.GetString())
        properties.AddString('Font: ' + str(text.GetFont()))
        properties.AddString('Position: X: ' + str(point.X) + '   Y: ' + str(point.Y))
        properties.AddString('Height: ' + str(text.GetHeight()))
        properties.AddString('Rotation: ' + str(text.GetRotation()))
        properties.AddString('Aspect: ' + str(text.GetAspect()))
        properties.AddString('Slanting: ' + str(text.GetSlanting()))
    except:
        print KcsStringlist.error

    try:
        kcs_ui.string_select('Text properties', '', '', properties)
    except:
        print kcs_ui.error

    return

#-------------------------------------------------------------------------------------------------------------
def ShowContourProperties(contour):                         # function displays properties of contour
    try:
        properties = KcsStringlist.Stringlist('----------------- common -----------------------')
        if contour.IsVisible():
            properties.AddString('Visible: True')
        else:
            properties.AddString('Visible: False')
        if contour.IsDetectable():
            properties.AddString('Detectable: True')
        else:
            properties.AddString('Detectable: False')
        properties.AddString('Colour: ' + (contour.GetColour()).Name())
        properties.AddString('Linetype: ' +(contour.GetLineType()).Name())
        properties.AddString('Layer: ' + str((contour.GetLayer()).GetLayer()))
        properties.AddString('-------------- first 10 points -----------------')
        segments = contour.Contour[0:10]
        for segment in segments:
            msg = ''
            if len(segment)>0:
                point = segment[0]
                msg = 'X: ' + str(point.X) + '  Y: ' + str(point.Y)
            if len(segment)>1:
                amplitude = segment[1]
                msg = msg + '   amplitude: ' + str(amplitude)
            if len(segment)>0:
                properties.AddString(msg)
    except:
        print KcsStringlist.error

    try:
        kcs_ui.string_select('Contour properties', '', '', properties)
    except:
        print kcs_ui.error

    return

#-------------------------------------------------------------------------------------------------------------
def FindElement(elementkind, point):                    # function gets element handle and reports it on screen
    handle = -1
    try:                                                # if element not found reports a message
        if elementkind==1:
            handle = kcs_draft.text_identify(point)     # text
            kcs_draft.element_highlight(handle)
            text = KcsText.Text('')
            text = kcs_draft.text_properties_get(handle, text)
            ShowTextProperties(text)
        elif elementkind==2:
            handle = kcs_draft.symbol_identify(point)    # symbol
            kcs_draft.element_highlight(handle)
            symbol = KcsSymbol.Symbol(1, 1)
            symbol = kcs_draft.symbol_properties_get(handle, symbol)
            ShowSymbolProperties(symbol)
        elif elementkind==3:
            handle = kcs_draft.contour_identify(point)   # contour
            kcs_draft.element_highlight(handle)
            contour2d = KcsContour2D.Contour2D(point)
            contour2d = kcs_draft.contour_properties_get(handle, contour2d)
            ShowContourProperties(contour2d)
        else:
            return

        kcs_draft.highlight_off(0)                      # highlight off all highlighted elements

    except:
        print kcs_draft.error
        if kcs_draft.error == 'kcs_NotFound':
            kcs_ui.message_noconfirm('kcs_NotFound')
        kcs_draft.highlight_off(0)                      # highlight off all highlighted element

    return

#-------------------------------------------------------------------------------------------------------------
def ElementFromPoint(elementkind):                   # function gets point and calls searching for element
    try:
        point = KcsPoint2D.Point2D()
    except:
        print KcsPoint2D.error
        return

    prompt = ''

    if elementkind == 1:
        prompt = 'Indicate text, OC to exit'
    if elementkind == 2:
        prompt = 'Indicate symbol, OC to exit'
    if elementkind == 3:
        prompt = 'Indicate contour, OC to exit'

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
        actions = KcsStringlist.Stringlist('text properties')
        actions.AddString('symbol properties')
        actions.AddString('contour properties')
    except:
        print KcsStringlist.error

    result = 1
    while result:
        res = kcs_ui.choice_select('Get properties', 'Select element kind', actions)
        if res[0]==kcs_util.ok():
            elementkind = res[1]
            ElementFromPoint(elementkind)
        else:
            result = 0

    kcs_ui.message_noconfirm('Script interrupted')

except:
    print kcs_ui.error
