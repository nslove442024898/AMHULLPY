## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#
#          kcs_ex_ui2.py
#
#      PURPOSE:
#
#          This program displays a message that has to be confirmed
#
import kcs_ui

msg = 'This is a confirm box\nwith\nmultiple\nlines'
try:
  kcs_ui.message_confirm(msg)
except:
  print kcs_ui.error
