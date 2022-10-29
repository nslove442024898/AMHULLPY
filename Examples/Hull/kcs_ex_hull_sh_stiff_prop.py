## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
"""This example shows how to modify shell stiffener properties
by using:
   kcs_chm.sh_stiff_prop_get()
   kcs_chm.sh_stiff_prop_set()
   KcsShStiffProp.ShStiffProp()

If any of the attributes in the ShStiffProp instance is set to None,
then this property will not be changed when using the
sh_stiff_prop_set function. This way the sh_stiff_prop_get function
is not necessary for changing properties for a shell stiffener.

This example will recreate the stiffener and then ask if the user
wants to store or skip the siffener.
"""
import kcs_chm
import kcs_ui
import kcs_util
import kcs_draft

import KcsModel
import KcsPoint2D
import KcsShStiffProp

def run():
   point = KcsPoint2D.Point2D()
   model = KcsModel.Model()
   res = kcs_util.ok()
   while res == kcs_util.ok():
      model.SetName('')
      res,point = kcs_ui.point2D_req('Indicate Stiffener',point)
      if res == kcs_util.ok():
         model, aa, bb = kcs_draft.model_identify(point, model)
         getProp = kcs_chm.stiffener_prop_get(model)
         print getProp
         prop = KcsShStiffProp.ShStiffProp()
         prop.SetUseStiffenerData(1)
         prop.SetGPS_2('AAbbCC')
         prop.SetProfileType(10)
         prop.SetProfileParameter(200)
         prop.SetProfileParameter(12)
         print prop
         resprop = kcs_chm.stiffener_prop_set(model,prop)
         print resprop
         kcs_chm.recreate(model)
         ans = kcs_ui.answer_req('Shell Stiffener Properties', 'Store the stiffener?')
         if ans == kcs_util.yes():
            kcs_chm.store(model)
         else:
            kcs_chm.skip(model)

if __name__ == "__main__":
   run()
