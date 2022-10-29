#
#      NAME:
#          KcsStringlist.py
#
#      PURPOSE:
#          The Stringlist class holds information about a list of strings
#
#          Do NOT change the names of the attributes, they are used by
#          the Vitesse interface. Users may only add or change methods
#
#      ATTRIBUTES:
#          StrList              The string list

class Stringlist:

#
#      METHOD:
#          __init__
#
#      PURPOSE:
#          To create an instance of the class set the first string
#
#      INPUT:
#          Parameters:
#          inString              The first string
#
     def __init__(self, inString):
        self.StrList = [inString]

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

     def __repr__(self):
         return 'Stringlist: %s' % self.StrList


#
#      METHOD:
#          AddString
#
#      PURPOSE:
#          Add a new string to the list
#
#      INPUT:
#          Parameters:
#          inString          The new string

     def AddString(self, inString):
        self.StrList.append(inString)
