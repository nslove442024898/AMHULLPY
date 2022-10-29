## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#      NAME:
#          KcsPythonUtil.py
#
#      PURPOSE:
#          The PythonUtil represents python utilities class
#

import string
import sys

class PythonUtil:
   def __init__(self):
      pass

   def AppendPythonPath(self, path):
      for item in sys.path:
         if string.upper(item) == string.upper(path):
            return
      sys.path.append(path)
