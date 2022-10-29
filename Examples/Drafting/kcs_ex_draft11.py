## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_draft11.py
#
#      PURPOSE:
#
#          This program places a text positioned by user, in the current drawing.
#
import kcs_draft
import kcs_ui
import kcs_util
import KcsPoint2D
import CommonSample

#-------------------------------------------------------------------------------------------------------------
try:

   kcs_ui.message_confirm('This script will create a text.')

   text = ''
   linenr = 1

   while 1:
      resp, line = kcs_ui.string_req('Enter text line %d, OC to complete:' % linenr, '')

      if len(text) == 0:
         text = line
      else:
         text = text + '\n' + line

      if kcs_ui.answer_req('Text entering', 'Next line?') != kcs_util.yes():
         break

      elif resp == kcs_util.cancel():
         text = ''
         break

      linenr = linenr + 1

   point = KcsPoint2D.Point2D()
   if len(text) > 0:
      try:
         resp, point = kcs_ui.point2D_req('Select insertion point', point)
         if resp == kcs_util.ok():
            try:
               kcs_draft.text_new(text, point)
            except:
               CommonSample.ReportTribonError(kcs_draft)
      except:
         CommonSample.ReportTribonError(kcs_ui)
   else:
      kcs_ui.message_noconfirm('Text not defined!')

except:
   pass

