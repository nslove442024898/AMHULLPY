## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import kcs_util
#
# The trigger is called when the Filter Active function is invoked.
# Its purpose is to enable for user to select among predefined filters.
#
# Input:
#    - None
#
# Return:
#    - ok/abort
#    - filter name
#

def pre():
#
#  Here you can add customized functions e.g. widget from which user can select among
#  a set of predefined filters.
#  A filter can be a file of model data, status information etc. used for matching
#  model objects later in a drag & drop operation.
#
   result = []
   result.append(kcs_util.trigger_ok())
   result.append("CURRFILT")
   return result
