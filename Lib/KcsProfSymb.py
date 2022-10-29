## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#-----------------------------------------------------------------------------
#  Get profile symbol from profile type
#-----------------------------------------------------------------------------

def getSymb( type):
  if type == 10:
    symb = 56
  elif 20 <= type and type <= 23:
    symb = 42
  elif 30 <= type and type <= 33:
    symb = 43
  elif type == 35:
    symb = 57
  elif type == 36:
    symb = 58
  elif 37 <= type and type <= 38:
    symb = 43
  elif 40 <= type and type <= 43:
    symb = 44
  elif type == 50:
    symb = 45
  elif 51 <= type and type <= 55:
    symb = 46
  elif type == 56:
    symb = 48
  elif type == 60:
    symb = 49
  elif 61 <= type and type <= 62:
    symb = 95
  elif type == 63:
    symb = 51
  elif type == 64:
    symb = 52
  elif type == 65:
    symb = 53
  elif 70 <= type and type <= 72:
    symb = 54
  elif 73 <= type and type <= 74:
    symb = 55
  elif type == 97:
    symb = 59
  elif type == 98:
    symb = 47
  else:
    symb = 41
  return symb

#
#-----------------------------------------------------------------------------
#  Start of main body
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":
  for type in range(100):
    print type, ": ", getSymb(type)
