## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
import kcs_util

def post(*args):
   return kcs_util.trigger_ok()
   
def pre(*args):
   return kcs_util.trigger_ok()
