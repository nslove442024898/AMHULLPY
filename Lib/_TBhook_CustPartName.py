## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#  _TBhook_CustPartName - Customized Part Name
#
#  If this script is found in the PYTHONPATH it will be used to create partnames
#  automatically. The signature of the interface methods must not be changed.
#
#  This script is called when a partname has been created according to
#  customer defined partname rules. All input parameters used by the partname rules
#  plus the resulting partname are supplied to this script. The partname may then be
#  altered by Python commands in this script.
#
#  Input:
#  Project           - Project name.
#  Assembly          - Assembly reference.
#  Block             - Block name.
#  Module            - Outfitting module name.
#  System            - Outfitting system name.
#  Drawing           - Drawing name.
#  Location          - Location code.
#  PositionName      - Position name used instead of position number.
#  PositionNo        - Position number of the part.
#  BracketPositionNo - Position number of profiles on a bracket.
#  SymmetryCode
#  BuiltProfile      - Built profile code
#                      = 1 for the web part
#                      = 2 for the flange part
#  GPS1              - General purpose strings 1-4
#  GPS2
#  GPS3
#  GPS4
#  TribonPartName    - Name of part on part databank.
#  StoringCode       - Tribon storing code
#  RulePartName      - Part name according to partname rules.
#
#  Output:
#  CustPartName      - Customized part name
#
#
import string

#-----------------------------------------------------------------------------
#  Interface method - must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def getPartName(Project,Assembly,Block,Module,System,Drawing,Location,PositionName,PositionNo,BracketPositionNo,SymmetryCode,BuiltProfile,GPS1,GPS2,GPS3,GPS4,TribonPartName,StoringCode,RulePartName):

  CustPartName = RulePartName
#-----------------------------------------------------------------------------
#
# The partname created according to Part Name Control in this example
# may be viewed as consisting of three substrings delimited by a delimiter.
# The last substring is the lowest assembly name followed by position number.
# When lowest assembly name equals 'A' the position number should be suppressed.
#-----------------------------------------------------------------------------
  Delimiter = '-'
  SplitList = string.splitfields(CustPartName,Delimiter)
  if len(SplitList) > 2:
#-----------------------------------------------------------------------------
#   Split the partname in substrings FStr, MStr and LStr
#-----------------------------------------------------------------------------
    FStr = SplitList[0]
    LStr = SplitList[-1]
    SplitList = SplitList[1:-1]
    MStr = string.joinfields(SplitList,Delimiter)
#-----------------------------------------------------------------------------
#   If the last string consists of 'A' followed by numbers
#   then suppress the numbers
#-----------------------------------------------------------------------------
    if LStr[0] == 'A':
      PosStr = LStr[1:]

      try:
        PosNo = eval(PosStr)
        LStr = 'A'
      except:
        PosNo = -1
#-----------------------------------------------------------------------------
#   Join substrings FStr, MStr and LStr to compose the customized partname
#-----------------------------------------------------------------------------
    CustPartName = FStr + Delimiter + MStr + Delimiter + LStr

  return CustPartName

#
#-----------------------------------------------------------------------------
#  Self test when run as top level script
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
  print "_TBhook_CustPartName"
  print getPartName("","121-BK40A-A","BK001","","","","","",35,0,1,0,"","","","","BK400-2-1P",0,"121-BK40A-A35")
  print getPartName("","141-BK40P-AB","BK001","","","","","",35,0,1,0,"","","","","BK400-3-1S",0,"141-BK40P-AB35")
  print getPartName("","121-BK40A-B","BK001","","","","","",35,0,1,0,"","","","","BK400-4-1P",0,"121-BK40A-B35")
