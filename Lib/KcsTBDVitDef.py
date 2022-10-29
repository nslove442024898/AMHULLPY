## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import anydbm
import os

#------------------------------------------------------------------------------
#  Internal - Get the dbm
#------------------------------------------------------------------------------

def getDefaultdbm():
  filename = os.getenv('TEMP','C:\TEMP') + "\MenuDef.dbm"
  try:
    defdbm = anydbm.open(filename, 'c')
  except IOError:
    filename = "MenuDef.dbm"
    defdbm = anydbm.open(filename, 'c')
  return defdbm

#------------------------------------------------------------------------------
#  Internal - Get the default dictionary
#------------------------------------------------------------------------------

def getDefaultList( defdbm):
  deflist = {}
  try:
    deflist['Block'] = defdbm['Block']
  except KeyError:
    deflist['Block'] = ""
  try:
    deflist['AftLim'] = defdbm['AftLim']
  except KeyError:
    deflist['AftLim'] = "C"
  try:
    deflist['ForLim'] = defdbm['ForLim']
  except KeyError:
    deflist['ForLim'] = "C"
  try:
    deflist['Stiff'] = defdbm['Stiff']
  except KeyError:
    deflist['Stiff'] = "N"
  try:
    deflist['StiOff'] = defdbm['StiOff']
  except KeyError:
    deflist['StiOff'] = "0"
  try:
    deflist['StiPos'] = defdbm['StiPos']
  except KeyError:
    deflist['StiPos'] = "Y"
  return deflist

#------------------------------------------------------------------------------
#  Get the list of default values
#------------------------------------------------------------------------------

def getDefaults():
  defdbm = getDefaultdbm()
  deflist = getDefaultList( defdbm)
  defdbm.close()
  return deflist


#-----------------------------------------------------------------------------
#   Test when run as main module
#-----------------------------------------------------------------------------
if __name__ == "__main__":
  print "KcsTBDVitDef"
  list = getDefaults()
  print list
