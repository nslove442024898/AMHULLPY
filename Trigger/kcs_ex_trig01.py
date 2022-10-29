## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_trig01.py
#
#      PURPOSE:
#
#          This is an example of Post- and Pre- trigger definitions. Program allows user to view
#          input parameters, define output parameters and select appropriate result to return
#          from funtion
#

import kcs_ui
import kcs_util
import KcsStringlist

#-------------------------------------------------------------------------------------------------------------
def ShowParametersList(parameters):                     # function lists parameters
    list = KcsStringlist.Stringlist('parameters:')
    for parameter in parameters:
        list.AddString(str(parameter))
    kcs_ui.string_select('Parameters', '', '', list)

#-------------------------------------------------------------------------------------------------------------
def AddStringParameter(resultslist):                    # define string parameter
    (status, parameter) = kcs_ui.string_req('parameter', '')
    if status == kcs_util.ok():
        resultslist.append(parameter)

#-------------------------------------------------------------------------------------------------------------
def AddRealParameter(resultslist):                      # define real parameter
    (status, parameter) = kcs_ui.real_req('parameter')
    if status == kcs_util.ok():
        resultslist.append(parameter)

#-------------------------------------------------------------------------------------------------------------
def AddIntegerParameter(resultslist):                   # define integer parameter
    (status, parameter) = kcs_ui.int_req('parameter')
    if status == kcs_util.ok():
        resultslist.append(parameter)

#-------------------------------------------------------------------------------------------------------------
def EditOutputParameters(resultslist):                  # function allows user to edit parameters
    try:
        # build elements kind list
        actions = KcsStringlist.Stringlist('add string')
        actions.AddString('add integer')
        actions.AddString('add real')
        actions.AddString('delete all')
        actions.AddString('view parameters')
        actions.AddString('return')
    except:
        print KcsStringlist.error

    stop = 0
    while not stop:
        res = kcs_ui.choice_select('Add return value', '', actions)
        if res[0] != kcs_util.ok():
            result = 0
        else:
            if res[1]==1:
                AddStringParameter(resultslist)
            elif res[1]==2:
                AddIntegerParameter(resultslist)
            elif res[1]==3:
                AddRealParameter(resultslist)
            elif res[1]==4:
                templist = resultslist[0:]
                for item in templist:
                    resultslist.remove(item)
            elif res[1]==5:
                ShowParametersList(resultslist)
            elif res[1]==6:
                stop = 1

#-------------------------------------------------------------------------------------------------------------
def ShowTriggerInfo(args, triggertype):                 # function shows and allow user to edit trigger parameters
    arguments = []
    resultslist = []
    result = kcs_util.trigger_ok()

    for argument in args:
        arguments.append(argument)

    title = ''
    if triggertype<0:
        title = 'Pre trigger started'
    else:
        title = 'Post trigger started'

    try:
        # build elements kind list
        actions = KcsStringlist.Stringlist('view input parameters')
        actions.AddString('define output parameter')
        actions.AddString('return invalid value')
        actions.AddString('return ok')
        if triggertype<0:
            actions.AddString('return override')
            actions.AddString('return abort')
    except:
        print KcsStringlist.error

    stop = 0
    while not stop:
        res = kcs_ui.choice_select(title, 'Select operation', actions)
        if res[0] != kcs_util.ok():
            result = kcs_util.trigger_ok()
            stop = 1
        else:
            if res[1]==1:
                ShowParametersList(arguments)           # check input parameters
            elif res[1]==2:
                EditOutputParameters(resultslist)       # define output parameters
            elif res[1]==3:
                result = -2                             # invalid return value
                stop = 1
            elif res[1]==4:
                result = kcs_util.trigger_ok()          # ok value
                stop = 1
            elif res[1]==5:
                result = kcs_util.trigger_override()    # override value
                stop = 1
            elif res[1]==6:                             # abort value
                result = kcs_util.trigger_abort()
                stop = 1


    if len(resultslist)>0:                  # format result value
        tmplist = []
        tmplist.append(result)
        for parameter in resultslist:
            tmplist.append(parameter)
        return tmplist
    else:
        return result

#-------------------------------------------------------------------------------------------------------------
def pre(*args):                             # pre trigger definition
    result = ShowTriggerInfo(args, -1)
    print result
    return result;

#-------------------------------------------------------------------------------------------------------------
def post(*args):                            # post trigger definition
    result = ShowTriggerInfo(args, 1)
    print result
    return result;

