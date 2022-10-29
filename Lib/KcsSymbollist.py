## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#
#        NAME:
#            KcsSymbollist
#
#        PURPOSE:
#            The Symbollist class holds information about a list of symbols.
#
#        ATTRIBUTES:
#            SymbList              The symbol list
#
#            Do NOT change the names of the attributes, they are used by
#            the Vitesse interface. Users may only add or change methods
#
class Symbollist:

#
#        METHOD:
#             __init__
#
#        PURPOSE:
#             To create an instance of the class and set the first symbol
#
#        INPUT:
#             Parameters:
#             inFont                   The symbol font
#             inSymbol                 The symbol number within that font
#
    def __init__(self,inFont,inSymbol):
        self.SymbList = []
        self.SymbList.append(inFont)
        self.SymbList.append(inSymbol)

#
#      METHOD:
#          __repr__
#
#      PURPOSE:
#          To print the class

    def __repr__(self):
        return 'SymbolList: %s' % self.SymbList


#
#        METHOD:
#             AddSymbol
#
#        PURPOSE:
#             Add a new symbol to the list
#
#        INPUT:
#             Parameters:
#             inFont           The symbol font
#             inSymbol         The symbol number within that font
#

    def AddSymbol(self,inFont,inSymbol):
        self.SymbList.append(inFont)
        self.SymbList.append(inSymbol)
