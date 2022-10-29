## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_model01.py
#
#      PURPOSE:
#
#          This example shows how to use model_hull_contact.
#
#
import kcs_model
import kcs_ui
import kcs_util
import KcsModel
import CommonSample
import math

model = None

def BuildChoiceSelectList():
    list = []
    if model == None:
        list.append('Model: None')
    else:
        list.append('Model: ' + model.Name + " (" + model.Type + ")")
    list.append('Find hull contact')
    return list

while 1:
    res, index = kcs_ui.choice_select('model_hull_contact test', 'Action:', BuildChoiceSelectList())
    if res == kcs_util.ok():
        if index==1:
            model = CommonSample.SelectModel()
        elif index==2:
            try:
                models = kcs_model.model_hull_contact(model)
                results = []
                if models != None:
                    for model in models:
                        results.append(model.Name + "(" + model.Type + ")")
                else:
                    results.append('No models found!')
                kcs_ui.string_select('hull models', 'Results', 'Press cancel', results)
            except:
                pass
    else:
        break

