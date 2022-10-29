## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
"""This example shows how to modify shell plate properties
by using:
   kcs_chm.plate_prop_get()
   kcs_chm.plate_prop_set()
   KcsShPlateProp.ShPlateProp()

Attributes in the ShPlateProp instance set to None,
will not be changed when using the plate_prop_set function.
This way the plate_prop_get function is not necessary for
changing properties for a shell plate.

This example will recreate the plate and then ask if the user
wants to store or skip the plate.
"""
import kcs_chm
import kcs_ui
import kcs_util
import kcs_draft

import KcsModel
import KcsPoint2D
import KcsShPlateProp

def run():
   point = KcsPoint2D.Point2D()
   model = KcsModel.Model()
   res = kcs_util.ok()
   while res == kcs_util.ok():
      model.SetName('')
      res,point = kcs_ui.point2D_req('Indicate Plate',point)
      if res == kcs_util.ok():
         model, aa, bb = kcs_draft.model_identify(point, model)
         getProp = kcs_chm.plate_prop_get(model)
         print getProp
         prop = KcsShPlateProp.ShPlateProp()
         prop.SetGPS_2('AAbbCC')
         prop.SetThickness(5)
         prop.SetDestination('Test Destination');
         print prop
         resprop = kcs_chm.plate_prop_set(model, prop)
         print resprop
         kcs_chm.recreate(model)
         ans = kcs_ui.answer_req('Shell Plate Properties', 'Store the plate?')
         if ans == kcs_util.yes():
            kcs_chm.store(model)
         else:
            kcs_chm.skip(model)

if __name__ == "__main__":
   run()
