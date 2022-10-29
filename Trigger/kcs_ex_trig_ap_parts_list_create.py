## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import os
import string
import kcs_util
#
#  Take as input the two csv files generated by Assembly parts list program.
#  Set Tribon EV's TBW_APL_CSV1 and TBW_APL_CSV2 pointing at the csv files.
#  Run the AssemblyList.xls MS Excel macro to produce formated files.
#  The Excel macro is located in the customise directory of Tribon installation.
#  AssemblyList.xls is a sample macro delivered for further customisation.
#

def post(*args):
   csv1 = args[0]
   csv2 = args[1]

   binDir = kcs_util.TB_environment_get('SB_SYSTEM')
   custDir = string.replace(binDir,'\\bin','\\customise')
   prog = custDir + '\AssemblyList.xls'

   kcs_util.TB_environment_set('TBW_APL_CSV1',csv1)
   kcs_util.TB_environment_set('TBW_APL_CSV2',csv2)

   os.startfile(prog)

   result = kcs_util.trigger_ok()
   return result
