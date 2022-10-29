## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

"""MODULE: stringutils v. 1.302
PURPOSE: Define additional string handling utilities not available
directly in the string module"""

import string

def TrimNum(num, prec=-1):
  """TrimNum(num, prec) -> string

Returns the shortest possible string representation of the number 'num'
with trailing zeroes trimmed.
If an optional 'prec' argument is given, the number is first represented with
'prec' decimal digits after the decimal point, before the trimming is tried.
Examples:
TrimNum(1.240)    -> '1.24'
TrimNum(1.288, 2) -> '1.29'
TrimNum(1.0)      -> '1'"""
  try:
    if prec < 0: s = str(num)
    else: s = ("%0." + str(prec) + "f") % num
  except:
    return "****"
  pointPos = string.rfind(s, '.')
  if pointPos == -1: return s
  n = len(s)-1
  while s[n] == '0': n = n-1
  if s[n] != '.': n = n+1
  return s[:n]

# ---------------------------------------------------------------------------

def IsStringAllowed(s, allowed):
  """IsStringAllowed(s, alllowed) -> 0 or 1

Result is 1, if all the characters in string s are in the string 'allowed'.
If not, 0 is returned."""
  res = 1
  for c in s:
    if c not in allowed:
      res = 0
      break
  return res

# ---------------------------------------------------------------------------

def ScanFile(fname, verify_function, flags = ""):
  """Scans the file 'fname', and verifies each line using 'verify_function',
which has to be a function with two parameters:
   def verify_function(line):
returning an integer value (0 - reject, <> 0 - accept).

Available flags:
S - whitespaces are trimmed off before processing
U - line is made uppercase before processing, and an uppercase version is stored, if accepted
u - line is made uppercase before processing, but an original version is stored, if accepted
N - results contains tuples (line_no, line) (default: only lines, without line numbers
1 - first accepted line ends the search

Result:
status - 0 (OK), 1 (file opening error), 2 (file read error)
result - list of accepted line information"""
  UpperCaseOutput = "U" in flags # store uppercase version of string
  UpperCaseInput = UpperCaseOutput or ("u" in flags) # use uppercase version of string
  StripString = "S" in flags # trim whitespaces from the string before sending it to verify_function
  RecordLineNumbers = "N" in flags
  FindOneOnly = "1" in flags

  result = []
  status = 1
  try:
    file = open(fname, "r")
    status = 2
    try:
      row = file.readline()
      line_no = 1
      while row != "":
        if StripString: row = string.strip(row)
        if UpperCaseInput:
          urow = string.upper(row)
          accept = verify_function(urow)
        else:
          accept = verify_function(row)
        if accept:
          if UpperCaseOutput:
            if RecordLineNumbers:
              result.append((line_no, urow))
            else:
              result.append(urow)
          elif RecordLineNumbers:
            result.append((line_no, row))
          else:
            result.append(row)
          if FindOneOnly: break
        row = file.readline()
        line_no = line_no + 1

      status = 0
    finally:
      file.close()
  except:
    pass
  return (status, result)
