## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_model05.py
#
#      PURPOSE:
#
#          This example shows how to use model_interference_check.
#          Outfitting models touched by gievn panel in given range are delivered.
#
import kcs_model
import kcs_ui
import kcs_util
import KcsModel
import CommonSample
import math

Equipments = ['equipment', 'struct', 'pipe', 'ventilation', 'cable']

model = None
outfitting = Equipments[0]

def BuildChoiceSelectList():
    list = []
    if model == None:
        list.append('Model: None')
    else:
        list.append('Model: ' + model.Name + " (" + model.Type + ")")
    list.append('Outfit type: ' + outfitting)
    list.append('Check interference')
    return list

while 1:
    res, index = kcs_ui.choice_select('model_interference_check test', 'Action:', BuildChoiceSelectList())
    if res == kcs_util.ok():
        if index==1:
            model = CommonSample.SelectModel()
        elif index==2:
            res, index = kcs_ui.choice_select('Outfitting types', 'Select type:', Equipments)
            if res == kcs_util.ok():
                outfitting = Equipments[index-1]
        elif index==3:
            try:
                models = kcs_model.model_interference_check(model, outfitting)
                results = []
                if models != None:
                    for item in models:
                        results.append(item.Name + "(" + item.Type + ")")
                else:
                    results.append('No interferences found!')
                kcs_ui.string_select('Interference models', 'Results', 'Press cancel', results)
            except:
                pass
    else:
        break

