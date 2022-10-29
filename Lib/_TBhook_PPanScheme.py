## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.
#
#  _TBhook_PPanScheme - Vitesse plane panel scheme hook
#
#  If this script is found in the PYTHONPATH it will be used to format
#  plane panel scheme statements.
#
import string

#-----------------------------------------------------------------------------
#  Interface method - SplitIntoLines -
#  must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def SplitIntoLines( stmt):
#
# Add <br> for a line break in stmt
#

# In this example a line break is added for each slash in a boundary or curve
# statement longer than 72 characters

  if (string.find( stmt, "BOU") == 0 or string.find( stmt, "CUR") == 0) and \
     len(stmt) > 72:
    stmtSplit = string.split( stmt, "/ ")
    stmt = string.join( stmtSplit, "/<br>")
  return stmt

#-----------------------------------------------------------------------------
#  Interface method - FormatLine -
#  must not be changed regading input parameters & returns
#-----------------------------------------------------------------------------

def FormatLine( line):
#
# Add <b>...</b> around e.g. keywords to make the show up bold in the editor
#

# In this example the panel location is made bold

  if line[:3] == "PAN":
    sep = ", SBP,"
    if string.find(line, sep) == -1:
      sep = ", SP,"
      if string.find(line, sep) == -1:
        sep = ", P,"
        if string.find(line, sep) == -1:
          sep = ", S,"
          if string.find(line, sep) == -1:
            sep = ""
    if sep != "":
      lineSplit = string.split( line, sep)
      sep = sep[2:-1]
      sep = ", <b>" + sep + "</b>,"
      line = string.join( lineSplit, sep)
  return line

#
#-----------------------------------------------------------------------------
#  Self test when run as top level script
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
  print "PPanScheme - SplitIntoLines"
  print SplitIntoLines("PAN, 'TEST', P, BLO='BLO', DT=102, X=FR30;")
  print SplitIntoLines("BOU, SUR=1/ 'BASIC-DECK1'/ Y=LP13/ 'BASIC-TANKTOP';")
  print SplitIntoLines("BOU, SUR=1, ZMIN=3000, ZMAX=7000/ 'BASIC-DECK1'/ Y=LP13+450/ 'BASIC-TANKTOP';")
  print SplitIntoLines("CUR,  'C1', CLO, R=100, 'BASIC-DECK1', DIR=SB, M1=300, SID=FOR/ R=100, LIM=2, M1=300/ U=FR4-200, V=300, T=135;")
  print "PPanScheme - FormatLine"
  print FormatLine("PAN, 'TEST', P, BLO='BLO', DT=102, X=FR30;")
  print FormatLine("BOU, SUR=1, ZMIN=3000, ZMAX=7000/ 'BASIC-DECK1'/ Y=LP13+450/ 'BASIC-TANKTOP';")
