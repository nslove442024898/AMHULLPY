## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_modelstruct01.py
#
#      PURPOSE:
#
#          This example shows how to use modelstruct functions
#

import sys
import kcs_ui
import kcs_util
import kcs_modelstruct

from KcsStringlist import Stringlist
from KcsPoint3D import Point3D

#-------------------------------------------------------------------------------------------------------------
def PrintModelStructError():                      # prints modelstruct exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_modelstruct.error)
   print kcs_modelstruct.error
   print sys.exc_info()[1]

#-------------------------------------------------------------------------------------------------------------
def GetPoint3D(prompt, point):                                                 # allows user to specify point 3D
   res, x = kcs_ui.real_req(prompt + ' X:', point.X)
   if res == kcs_util.ok():
      res, y = kcs_ui.real_req(prompt + ' Y:', point.Y)
      if res == kcs_util.ok():
         res, z = kcs_ui.real_req(prompt + ' Z:', point.Z)
         if res == kcs_util.ok():
            point.X = x
            point.Y = y
            point.Z = z
            return 1
   return 0

#-------------------------------------------------------------------------------------------------------------
try:           # main
   # build actions list
   actions = Stringlist('Create new block')
   actions.AddString('Delete existing block')
   actions.AddString('Create new system')
   actions.AddString('Delete existing system')
   actions.AddString('Create new module')
   actions.AddString('Delete existing module')

   while 1:
      res = kcs_ui.choice_select('Modelstruct functions', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:                                 # create new block
               name = ''
               resp, name = kcs_ui.string_req('Block name:', name)
               if resp == kcs_util.ok():
                  min = Point3D()
                  max = Point3D()
                  if GetPoint3D('Min restriction point, coordinate ', min):
                     if GetPoint3D('Max restriction point, coordinate ', max):
                        kcs_modelstruct.block_new(name, min, max)
            elif res[1] == 2:                               # delete block
               name = ''
               resp, name = kcs_ui.string_req('Block name:', name)
               if resp == kcs_util.ok():
                  kcs_modelstruct.block_delete(name)
            elif res[1] == 3:                               # create new system
               name = ''
               descr = ''
               resp, name = kcs_ui.string_req('System name:', name)
               if resp == kcs_util.ok():
                  resp, descr = kcs_ui.string_req('System description:', descr)
                  resp, code = kcs_ui.int_req('Surface Preparation Code:', -1)
                  if resp == kcs_util.ok():
                     kcs_modelstruct.system_new(name, descr, code)
                  else:
                     kcs_modelstruct.system_new(name, descr)
            elif  res[1] == 4:                              # delete system
               name = ''
               resp, name = kcs_ui.string_req('System name:', name)
               if resp == kcs_util.ok():
                  kcs_modelstruct.system_delete(name)
            elif res[1] == 5:                               # create new module
               name = ''
               resp, name = kcs_ui.string_req('Module name:', name)
               if resp == kcs_util.ok():
                  kcs_modelstruct.module_new(name)
            elif  res[1] == 6:                              # delete module
               name = ''
               resp, name = kcs_ui.string_req('Module name:', name)
               if resp == kcs_util.ok():
                  kcs_modelstruct.module_delete(name)
         else:
            break;
      except:
         PrintModelStructError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]



