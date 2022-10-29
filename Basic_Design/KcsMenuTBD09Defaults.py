## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import kcs_ui
import kcs_util
import KcsTBDVitDef

ok = kcs_util.success()

#------------------------------------------------------------------------------
#  Change default values
#------------------------------------------------------------------------------

def changeDefaults():
  defdbm = KcsTBDVitDef.getDefaultdbm()
  deflist = KcsTBDVitDef.getDefaultList( defdbm)

  cho = kcs_ui.req_choice("Change: 1=Block 2=Aft limit 3=Forward limit 4=Stiffening 5=Stiffener margin 6=Stiffener position", 6)
  while cho[0] == ok:
    if cho[1] == 1:
      blo = kcs_ui.req_string("Default block (" + deflist['Block'] + ")")
      if blo[0] == ok:
        deflist['Block'] = blo[1]
    elif cho[1] == 2:
      lim = kcs_ui.req_string("Aft limit (" + deflist['AftLim'] + ")")
      if lim[0] == ok:
        deflist['AftLim'] = lim[1]
    elif cho[1] == 3:
      lim = kcs_ui.req_string("Forward limit (" + deflist['ForLim'] + ")")
      if lim[0] == ok:
        deflist['ForLim'] = lim[1]
    elif cho[1] == 4:
      lim = kcs_ui.req_choice("Stiffening: 1=Yes 2=Longitudinal 3=Transversal 4=No", 4)
      if lim[0] == ok:
        if lim[1] == 1:
          deflist['Stiff'] = "Y"
        elif lim[1] == 2:
          deflist['Stiff'] = "L"
        elif lim[1] == 3:
          deflist['Stiff'] = "T"
        else:
          deflist['Stiff'] = "N"
    elif cho[1] == 5:
      lim = kcs_ui.req_string("Stiffener edge margin (" + deflist['StiOff'] + ")")
      if lim[0] == ok:
        deflist['StiOff'] = lim[1]
    elif cho[1] == 6:
      lim = kcs_ui.req_answer("Use FR/LP positions for stiffeners")
      if lim[0] == ok:
        if lim[1] == 0:
          deflist['StiPos'] = "Y"
        else:
          deflist['StiPos'] = "N"

    cho = kcs_ui.req_choice("Change: 1=Block 2=Aft limit 3=Forward limit 4=Stiffening 5=Stiffener margin 6=Stiffener position", 6)

  defdbm['Block'] = deflist['Block']
  defdbm['AftLim'] = deflist['AftLim']
  defdbm['ForLim'] = deflist['ForLim']
  defdbm['Stiff'] = deflist['Stiff']
  defdbm['StiOff'] = deflist['StiOff']
  defdbm['StiPos'] = deflist['StiPos']
  defdbm.close()


#------------------------------------------------------------------------------
#  Menu interface Methods
#------------------------------------------------------------------------------

def getCaption():
  return "Defaults"

def getMenu():
  return 10

def getPosition():
  return -2

def run():
  changeDefaults()

#-----------------------------------------------------------------------------
#   Change parameters
#-----------------------------------------------------------------------------
if __name__ == "__main__":
  print getCaption()
  print getMenu(), getPosition()
  run()
