## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

##-----------------------------------------------------------------------------
## Name:        ctx_menu2.py
## Purpose:     Python implementation of context menu "Model Info" item
##
## Author:      tscmpr
##
## Created:     2002/23/02
## RCS-ID:      $Id: ctx_menu2.py $
## Licence:
##-----------------------------------------------------------------------------

import kcs_draft
import kcs_ui

from wxPython.wx import *

def run(*args):
   try:
      if not hasattr(kcs_draft, 'ContextPoint'):
          return None
      if kcs_draft.ContextPoint == None:
          return None

      kcs_ui.model_info(kcs_draft.ContextPoint)
      print 'end'
   except Exception, e:
      print e
