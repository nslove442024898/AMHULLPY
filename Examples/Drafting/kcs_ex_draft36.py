## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft36.py
#
#      PURPOSE:
#
#          This example shows how to use placvol_new function
#

import sys
import kcs_ui
import kcs_util
import kcs_draft
import kcs_placvol

import KcsStringlist
import KcsElementHandle
import KcsTransformation3D
import KcsPoint3D
import KcsVector3D

#-------------------------------------------------------------------------------------------------------------
def PrintPlacvolError():                                            # prints exception on console and output window
   kcs_ui.message_noconfirm('Error code: '+kcs_placvol.error)
   print kcs_placvol.error

#-------------------------------------------------------------------------------------------------------------
def BuildActionsList(unplacedname, placedname, point, uVector, vVector):   # build actions list
   # build actions list
   actions = KcsStringlist.Stringlist('Unplaced name: ' + unplacedname)
   actions.AddString('Place name: ' + placedname)
   actions.AddString('point:' + str(point.X) + ' ' + str(point.Y) + ' ' + str(point.Z))
   actions.AddString('uVector:' + str(uVector.X) + ' ' + str(uVector.Y) + ' ' + str(uVector.Z))
   actions.AddString('vVector:' + str(vVector.X) + ' ' + str(vVector.Y) + ' ' + str(vVector.Z))
   actions.AddString('Place volume')
   return actions

#-------------------------------------------------------------------------------------------------------------
def Get3Doubles(prompt, x, y, z):                  # prompts user to input 3 doubles (coordinates)
   res, x = kcs_ui.real_req(prompt+' X', x)
   if res == kcs_util.ok():
      res, y = kcs_ui.real_req(prompt+' Y', y)
      if res == kcs_util.ok():
         res, z = kcs_ui.real_req(prompt+' Z', z)
         if res == kcs_util.ok():
            return (1, x, y, z)
   return (0, x, y, z)

#-------------------------------------------------------------------------------------------------------------
try:           # main
   unplacedname = ''
   placedname = ''
   point = KcsPoint3D.Point3D()
   uVector = KcsVector3D.Vector3D();
   vVector = KcsVector3D.Vector3D();

   actions = BuildActionsList(unplacedname, placedname, point, uVector, vVector)
   while 1:

      res = kcs_ui.choice_select('Place volume', '', actions)
      try:
         if res[0]==kcs_util.ok():
            if res[1] == 1:         # key in unplaced volume name
               nameres, unplacedname = kcs_ui.string_req('Unplaced volume name:', unplacedname)
               actions = BuildActionsList(unplacedname, placedname, point, uVector, vVector)
            elif res[1] == 2:       # key in placed volume name
               nameres, placedname = kcs_ui.string_req('Placed volume name:', placedname)
               actions = BuildActionsList(unplacedname, placedname, point, uVector, vVector)
            elif res[1] == 3:       # key in placement point 3D
               res, x, y, z = Get3Doubles('Key in point coordinates:', point.X, point.Y, point.Z)
               if res:
                  point.SetCoordinates(x, y, z);
                  actions = BuildActionsList(unplacedname, placedname, point, uVector, vVector)
            elif res[1] == 4:       # key in U vector for placement
               res, x, y, z = Get3Doubles('Key in U vector coordinates:', uVector.X, uVector.Y, uVector.Z)
               if res:
                  uVector.SetComponents(x, y, z);
                  actions = BuildActionsList(unplacedname, placedname, point, uVector, vVector)
            elif res[1] == 5:       # key in V vector for placement
               res, x, y, z = Get3Doubles('Key in V vector coordinates:', vVector.X, vVector.Y, vVector.Z)
               if res:
                  vVector.SetComponents(x, y, z);
                  actions = BuildActionsList(unplacedname, placedname, point, uVector, vVector)
            elif res[1] == 6:       # place unplaced volume
               name = kcs_placvol.placvol_new(unplacedname, point, uVector, vVector, placedname)
               kcs_ui.message_noconfirm('Placed volume name:' + name)
         else:
            break;
      except:
         print sys.exc_info()[1]
         PrintPlacvolError()

   kcs_ui.message_noconfirm('Script interrupted')

except:
   print sys.exc_info()[1]
   print kcs_draft.error;

