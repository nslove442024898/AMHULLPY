## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft41.py
#
#      PURPOSE:
#
#          This example shows how to use linetype display settings functions
#

#-------------------------------------------------------------------------------------------------------------

from KcsLineTypeDisplaySettings import LineTypeDisplaySettings
import kcs_draft
import kcs_ui
import kcs_util
import string

try:
   settings = kcs_draft.linetype_display_settings_get()
except:
   kcs_ui.message_confirm("Can't retrive current settings!")
   settings = LineTypeDisplaySettings()

def ChangeWidths():
   # create dictionary with names of line types and get, set functions
   try:
      selected = 0
      functions = { }
      functions['Thin'] = [settings.GetThinWidth, settings.SetThinWidth]
      functions['Wide'] = [settings.GetWideWidth, settings.SetWideWidth]
      functions['XWide'] = [settings.GetXWideWidth, settings.SetXWideWidth]
      functions['DashedAndSolid'] = [settings.GetDashedAndSolidWidth, settings.SetDashedAndSolidWidth]
      functions['Track'] = [settings.GetTrackWidth, settings.SetTrackWidth]
      functions['System5'] = [settings.GetSystem5Width, settings.SetSystem5Width]
      functions['System6'] = [settings.GetSystem6Width, settings.SetSystem6Width]
      functions['System8'] = [settings.GetSystem8Width, settings.SetSystem8Width]
      functions['System9'] = [settings.GetSystem9Width, settings.SetSystem9Width]
      functions['System15'] = [settings.GetSystem15Width, settings.SetSystem15Width]
      functions['System16'] = [settings.GetSystem16Width, settings.SetSystem16Width]
      functions['System22'] = [settings.GetSystem22Width, settings.SetSystem22Width]
      functions['System23'] = [settings.GetSystem23Width, settings.SetSystem23Width]
      functions['System24'] = [settings.GetSystem24Width, settings.SetSystem24Width]
      functions['System25'] = [settings.GetSystem25Width, settings.SetSystem25Width]
      functions['System26'] = [settings.GetSystem26Width, settings.SetSystem26Width]
      functions['System27'] = [settings.GetSystem27Width, settings.SetSystem27Width]
   except Exception, e:
      kcs_ui.message_confirm(str(e))
      return

   while 1:
      results = []
      for key in functions.keys():
         results.append(key + ': ' + str(functions[key][0]()))
      results.sort()

      res = kcs_ui.string_select('Line type widths', 'Values', 'Select linetype or Options to update display settings', results)
      if res[0] == kcs_util.ok():
         linetype = string.split(results[res[1]-1], ':')[0]
         res, value = kcs_ui.real_req('Keyin new linetype width for '+linetype, functions[linetype][0]())
         if res == kcs_util.ok():
            functions[linetype][1](value)
      elif res[0] == kcs_util.options():
         res = kcs_ui.answer_req('Update', 'Do you want to update drawing settings?')
         if res == kcs_util.yes():
            try:
               kcs_draft.linetype_display_settings_set(settings)
            except Exception, e:
               kcs_ui.message_confirm(str(e))
         break
      else:
         break

def ChangePatterns():
   while 1:
      results = []
      Patterns = settings._LineTypeDisplaySettings__Patterns;
      for name in Patterns.keys():
         results.append(name + ': ' + str(Patterns[name]))
      results.sort()

      res = kcs_ui.string_select('Line type patterns', 'Values', 'Select pattern to change or Options to update display settings', results)
      if res[0] == kcs_util.ok():
         name = string.split(results[res[1]-1], ':')[0]
         res, value = kcs_ui.string_req('Keyin new pattern for (use "," as delimiter)'+linetype, '')
         if res == kcs_util.ok():
            results = string.split(value, ',')
            try:
               results = map(float, results)
               settings.SetPattern(name, results)
            except Exception, e:
               kcs_ui.message_confirm(str(e))
      elif res[0] == kcs_util.options():
         res = kcs_ui.answer_req('Update', 'Do you want to update drawing settings?')
         if res == kcs_util.yes():
            try:
               kcs_draft.linetype_display_settings_set(settings)
            except Exception, e:
               kcs_ui.message_confirm(str(e))
         break
      else:
         break

def ChangeLengths():
   while 1:
      results = []
      Lengths = settings._LineTypeDisplaySettings__PatternsLength;
      for name in Lengths.keys():
         results.append(name + ': ' + str(Lengths[name]))
      results.sort()

      res = kcs_ui.string_select('Line type lengths', 'Values', 'Select length to change or Options to update display settings', results)
      if res[0] == kcs_util.ok():
         name = string.split(results[res[1]-1], ':')[0]
         res, value = kcs_ui.real_req('Keyin new length for '+name, 0.0)
         if res == kcs_util.ok():
            try:
               settings.SetPatternLength(name, value)
            except Exception, e:
               kcs_ui.message_confirm(str(e))
      elif res[0] == kcs_util.options():
         res = kcs_ui.answer_req('Update', 'Do you want to update drawing settings?')
         if res == kcs_util.yes():
            try:
               kcs_draft.linetype_display_settings_set(settings)
            except Exception, e:
               kcs_ui.message_confirm(str(e))
         break
      else:
         break

try:           # main
   while 1:
      actions = ['widths', 'patterns', 'length']
      res = kcs_ui.choice_select('Linetype', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:
               ChangeWidths()
            elif res[1] == 2:
               ChangePatterns()
            elif res[1] == 3:
               ChangeLengths()
         else:
            break;
      except:
         break
except:
   pass
