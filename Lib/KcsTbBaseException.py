## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#      NAME:
#          KcsTbBaseException.py
#
#      PURPOSE:
#          The base class for exceptions raised by vitesse functionality
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#
#           strFunctionName     string        name of vitesse function that raised exception
#           strModuleName       string        name of module the function belongs to
#           strError            string        error string
#
#      METHODS:

import types

class TbBaseException(Exception):

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class
#
#      INPUT:
#          Parameters:
#
   def __init__(self):
      self.strFunctionName  = ''
      self.strModuleName    = ''
      self.strError         = ''

# -----------------------------------------------------------------------------------------------------------------
#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

   def __repr__(self):
      return 'Funtion: %s\nModule:%s\nError:%s' % (self.strFunctionName, self.strModuleName, self.strError)
