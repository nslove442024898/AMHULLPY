## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_util1.py
#
#      PURPOSE:
#
#          This program checks SB_PYTHON and changes the value
#
import kcs_util

env = 'SB_PYTHON'
def_value = '/users/python/vitesse'
try:
   cur_value = kcs_util.TB_environment_get(env)
   if cur_value != def_value:
      kcs_util.TB_environment_set(env,def_value)
      print 'SB_PYTHON set to ' + def_value
except:
  print kcs_util.error
