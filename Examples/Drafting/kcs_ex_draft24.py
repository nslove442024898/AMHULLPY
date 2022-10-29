## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft24.py
#
#      PURPOSE:
#
#          This example program creates new texts and symbols.
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
from math import *

#-------------------------------------------------------------------------------------------------------------
def BuildTextOptions(text):                                             # function builds actions list for text
    list = KcsStringlist.Stringlist('Text: '+text.GetString())
    list.AddString('Font: '+text.GetFont())
    pos = text.GetPosition()
    list.AddString('Pos: ' + str(pos.X) + ' ' + str(pos.Y))
    list.AddString('Height: ' + str(text.GetHeight()))
    list.AddString('Slant: ' + str(text.GetSlanting()))
    list.AddString('Aspect: ' + str(text.GetAspect()))
    list.AddString('Rotation: ' + str(text.GetRotation()))

    if text.IsVisible():
        list.AddString('Visible: Yes')
    else:
        list.AddString('Visible: No')

    if text.IsDetectable():
        list.AddString('Detectable: Yes')
    else:
        list.AddString('Detectable: No')

    list.AddString('Layer: ' + str((text.GetLayer()).GetLayer()))

    list.AddString('Ltype: ' + (text.GetLineType()).Name())

    list.AddString('Color: ' + (text.GetColour()).Name())

    list.AddString('insert text')

    return list;

#-------------------------------------------------------------------------------------------------------------
def BuildSymbolOptions(symbol):                                         # function builds actions list for text
    list = KcsStringlist.Stringlist('Symbol: ' + str(symbol.GetSymbolId()))
    list.AddString('Font: '+ str(symbol.GetFontId()))
    pos = symbol.GetPosition()
    list.AddString('Pos: ' + str(pos.X) + ' ' + str(pos.Y))
    list.AddString('Height: ' + str(symbol.GetHeight()))
    list.AddString('Rotation: ' + str(symbol.GetRotation()))

    if symbol.IsVisible():
        list.AddString('Visible: Yes')
    else:
        list.AddString('Visible: No')

    if symbol.IsDetectable():
        list.AddString('Detectable: Yes')
    else:
        list.AddString('Detectable: No')

    list.AddString('Layer: ' + str((symbol.GetLayer()).GetLayer()))

    list.AddString('Ltype: ' + (symbol.GetLineType()).Name())

    list.AddString('Color: ' + (symbol.GetColour()).Name())

    list.AddString('insert symbol')

    return list;

#-------------------------------------------------------------------------------------------------------------
def EditSymbol(symbol):                                         # function allows to change properties of text
    # build elements kind list
    actions = KcsStringlist.Stringlist('')
    actions = BuildSymbolOptions(symbol)

    result = 1
    while result:
        res = kcs_ui.choice_select('Edit symbol', '', actions)
        if res[0]==kcs_util.ok():
            if res[1] == 1:                                                             # symbol id
                (set, symbolId) = kcs_ui.int_req('Input symbol ID:', symbol.GetSymbolId())
                if set == kcs_util.ok():
                    symbol.SetSymbolId(symbolId)
                    actions = BuildSymbolOptions(symbol)
            elif res[1] == 2:                                                           # font id
                (set, fontId) = kcs_ui.int_req('Input font ID:', symbol.GetFontId())
                if set == kcs_util.ok():
                    symbol.SetFontId(fontId)
                    actions = BuildSymbolOptions(symbol)
            elif res[1] == 3:                                                           # position
                pos = symbol.GetPosition()
                (set, pos) = kcs_ui.point2D_req('Indicate position:', pos)
                if set == kcs_util.ok():
                        symbol.SetPosition(pos)
                        actions = BuildSymbolOptions(symbol)
            elif res[1] == 4:                                                           # height
                pos1 = KcsPoint2D.Point2D()
                pos2 = KcsPoint2D.Point2D()
                (set, pos1) = kcs_ui.point2D_req('Indicate first point:', pos1)
                if set == kcs_util.ok():
                        (set, pos2) = kcs_ui.point2D_req('Indicate first point:', pos2)
                        if set == kcs_util.ok():
                            height = sqrt( pow(pos1.X-pos2.X, 2) + pow(pos1.Y-pos2.Y, 2) )
                            symbol.SetHeight(height)
                            actions = BuildSymbolOptions(symbol)
            elif res[1] == 5:                                                           # rotation
                (set, rotation) = kcs_ui.real_req('Rotation:', symbol.GetRotation())
                if set == kcs_util.ok():
                        symbol.SetRotation(rotation)
                        actions = BuildSymbolOptions(symbol)
            elif res[1] == 6:                                                           # visibility
                if symbol.IsVisible():
                    symbol.SetVisible(0)
                else:
                    symbol.SetVisible(1)
                actions = BuildSymbolOptions(symbol)
            elif res[1] == 7:                                                           # detectability
                if symbol.IsDetectable():
                    symbol.SetDetectable(0)
                else:
                    symbol.SetDetectable(1)
                actions = BuildSymbolOptions(symbol)
            elif res[1] == 8:                                                           # layer
                (set, layerid) = kcs_ui.int_req('Layer:', (text.GetLayer()).GetLayer())
                if set == kcs_util.ok():
                        layer = symbol.GetLayer()
                        layer.SetLayer(layerid)
                        symbol.SetLayer(layer)
                        actions = BuildSymbolOptions(symbol)
            elif res[1] == 9:                                                           # line type
                (set, ltypestr) = kcs_ui.string_req('Linetype:', (symbol.GetLineType()).Name())
                if set == kcs_util.ok():
                    ltype = symbol.GetLineType()
                    ltype.SetName(ltypestr)
                    symbol.SetLineType(ltype)
                    actions = BuildSymbolOptions(symbol)
            elif res[1] == 10:                                                          # colour
                (set, colourstr) = kcs_ui.string_req('Colour:', (symbol.GetColour()).Name())
                if set == kcs_util.ok():
                    colour = symbol.GetColour()
                    colour.SetName(colourstr)
                    symbol.SetColour(colour)
                    actions = BuildSymbolOptions(symbol)
            elif res[1] == 11:                                                          # accept changes
                return 1
        else:
            return 0

#-------------------------------------------------------------------------------------------------------------
def EditText(text):                                     # function allows to change properties of text
    # build elements kind list
    actions = KcsStringlist.Stringlist('')
    actions = BuildTextOptions(text)

    result = 1
    while result:
        res = kcs_ui.choice_select('Edit text', '', actions)
        if res[0]==kcs_util.ok():
            if res[1] == 1:                                                             # text string
                (set, str) = kcs_ui.string_req('Input string:', text.GetString())
                if set == kcs_util.ok():
                    text.SetString(str)
                    actions = BuildTextOptions(text);
            elif res[1] == 2:                                                           # font name
                (set, str) = kcs_ui.string_req('Font name:', text.GetFont())
                if set == kcs_util.ok():
                    text.SetFont(str)
                    actions = BuildTextOptions(text);
            elif res[1] == 3:                                                           # position
                pos = text.GetPosition()
                (set, pos) = kcs_ui.point2D_req('Indicate position:', pos)
                if set == kcs_util.ok():
                        text.SetPosition(pos)
                        actions = BuildTextOptions(text);
            elif res[1] == 4:                                                           # height
                pos1 = KcsPoint2D.Point2D()
                pos2 = KcsPoint2D.Point2D()
                (set, pos1) = kcs_ui.point2D_req('Indicate first point:', pos1)
                if set == kcs_util.ok():
                        (set, pos2) = kcs_ui.point2D_req('Indicate first point:', pos2)
                        if set == kcs_util.ok():
                            height = sqrt( pow(pos1.X-pos2.X, 2) + pow(pos1.Y-pos2.Y, 2) )
                            text.SetHeight(height)
                            actions = BuildTextOptions(text);
            elif res[1] == 5:                                                           # slant
                (set, slant) = kcs_ui.real_req('New slanting:', text.GetSlanting())
                if set == kcs_util.ok():
                        text.SetSlanting(slant)
                        actions = BuildTextOptions(text);
            elif res[1] == 6:                                                           # aspect
                (set, aspect) = kcs_ui.real_req('New aspect ratio:', text.GetAspect())
                if set == kcs_util.ok():
                        text.SetAspect(aspect)
                        actions = BuildTextOptions(text);
            elif res[1] == 7:                                                           # rotation
                (set, rotation) = kcs_ui.real_req('Rotation:', text.GetRotation())
                if set == kcs_util.ok():
                        text.SetRotation(rotation)
                        actions = BuildTextOptions(text);
            elif res[1] == 8:                                                           # visibility
                if text.IsVisible():
                    text.SetVisible(0)
                else:
                    text.SetVisible(1)
                actions = BuildTextOptions(text);
            elif res[1] == 9:                                                           # detectability
                if text.IsDetectable():
                    text.SetDetectable(0)
                else:
                    text.SetDetectable(1)
                actions = BuildTextOptions(text);
            elif res[1] == 10:                                                          # layer
                (set, layerid) = kcs_ui.int_req('Layer:', (text.GetLayer()).GetLayer())
                if set == kcs_util.ok():
                        layer = text.GetLayer()
                        layer.SetLayer(layerid)
                        text.SetLayer(layer)
                        actions = BuildTextOptions(text);
            elif res[1] == 11:                                                          # line type
                (set, ltypestr) = kcs_ui.string_req('Linetype:', (text.GetLineType()).Name())
                if set == kcs_util.ok():
                    ltype = text.GetLineType()
                    ltype.SetName(ltypestr)
                    text.SetLineType(ltype)
                    actions = BuildTextOptions(text);
            elif res[1] == 12:                                                          # colour
                (set, colourstr) = kcs_ui.string_req('Colour:', (text.GetColour()).Name())
                if set == kcs_util.ok():
                    colour = text.GetColour()
                    colour.SetName(colourstr)
                    text.SetColour(colour)
                    actions = BuildTextOptions(text);
            elif res[1] == 13:                                                          # accept changes
                return 1
        else:
            return 0

# get user choice and select element
try:
    # build elements kind list
    try:
        actions = KcsStringlist.Stringlist('create new text')
        actions.AddString('create new symbol')
    except:
        print KcsStringlist.error

    result = 1
    while result:
        res = kcs_ui.choice_select('Create new element', 'Select element kind', actions)
        if res[0]==kcs_util.ok():
            if res[1] == 1:
                text = KcsText.Text()
                if EditText(text):                      # create and edit new text element
                    try:
                        kcs_draft.text_new(text)        # add new text element
                    except:
                        print kcs_draft.error
            if res[1] == 2:
                symbol = KcsSymbol.Symbol()
                if EditSymbol(symbol):                  # create and edit new symbol element
                    try:
                        kcs_draft.symbol_new(symbol)    # add new symbol element
                    except:
                        print kcs_draft.error
        else:
            result = 0

    kcs_ui.message_noconfirm('Script interrupted')

except:
    print kcs_ui.error
