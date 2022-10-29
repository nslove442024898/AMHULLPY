## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

import string

max_ncomp = 25

#-----------------------------------------------------------------------------
#   getGeoInit - initiate a coordiate clause
#-----------------------------------------------------------------------------
def getGeoInit(axis, prefix):
  coordinit = ""
  if type(axis) == type(0):
    if axis == 1:
      coordinit = "X=" + prefix
    elif axis == 2:
      coordinit = "Y=" + prefix
    elif axis == 3:
      coordinit = "Z=" + prefix
    elif axis == -1:
      coordinit = "U=" + prefix
    elif axis == -2:
      coordinit = "V=" + prefix
    else:
      coordinit = prefix
  return coordinit

#-----------------------------------------------------------------------------
#   getGeo - Get a principal plane clause (single value)
#-----------------------------------------------------------------------------

def getGeo(axis, prefix, coord):
  coordstr = getGeoInit(axis, prefix)
  if type(coord) == type(0):
    coordstr = coordstr + str(coord)
  elif type(coord) == type(""):
    coordstr = coordstr + coord
  return coordstr

#-----------------------------------------------------------------------------
#   getGeoRepSSE - Get a principal plane repetition clause
#-----------------------------------------------------------------------------

def getGeoRepSSE(axis, prefix, start, step, end):
  coordstrrep = []
  div = divmod( (end-start), step)
  totcoord = int(div[0]) + 1
  print totcoord
  base = 0
  while( totcoord > 0):
    if totcoord > max_ncomp:
      ncoord = max_ncomp
      totcoord = totcoord - ncoord
    else:
      ncoord = totcoord
      totcoord = 0
    coordstr = getGeoInit(axis, prefix)
    coordstr = coordstr + str(start + base*step)
    if ncoord > 1:
       coordstr = coordstr + "(" + str(step) + ")" + str(start + (base+ncoord-1)*step)
    base = base + ncoord
    coordstrrep.append(coordstr)
  return coordstrrep

#------------------------------------------------------------------------------
#  getGeoRepT - get a repetition term from a value tuple
#------------------------------------------------------------------------------
def getGeoRepT(axis, prefix, numb):

  def step_rep(prefix,start,step,end):
    if step == 0:
      srep = prefix + str(start)
    elif abs(step) == 1:
      srep = prefix + str(start) + "()" + str(end)
    else:
      srep = prefix + str(start) + "(" + str(step) + ")" + str(end)
    return srep

  strrep = []
  rep = getGeoInit(axis, "")
  state = 0
  start = 0
  step = 0
  end = 0
  for ind in range(len(numb)):
    if state == 0:
      start = numb[ind]
      state = 1
    elif state == 1:
      end = numb[ind]
      step = end - start
      state = 2
    elif state == 2:
      if numb[ind] - end == step:
        end = numb[ind]
        state = 3
      else:
        rep = rep + prefix + str(start) + ","
        start = end
        end = numb[ind]
        step = end - start
    elif state == 3:
      if numb[ind] - end == step:
        end = numb[ind]
      else:
        rep = rep + step_rep(prefix,start,step,end) + ","
        start = numb[ind]
        state = 1
    if divmod(ind,max_ncomp)[1] == 0 and ind > 0:
      rep = rep[:-1]
      strrep.append(rep)
      rep = getGeoInit(axis, "")

  if state == 1:
    rep = rep + prefix + str(start)
  elif state == 2:
    rep = rep + prefix + str(start) + "," + prefix + str(end)
  elif state == 3:
    rep = rep + step_rep(prefix,start,step,end)
  strrep.append(rep)

  return strrep

#-----------------------------------------------------------------------------
#   getRef - Get a component reference clause
#-----------------------------------------------------------------------------

def getRef(objname, compno=0, refl=0):
  refstr = ""
  if objname != "":
    refstr = refstr + "'" + objname + "'"
  if type(compno) == type(0) and compno != 0:
    refstr = refstr + ", " + str(compno)
  if refl == 1:
    refstr = refstr + ", REF"
  return refstr

#-----------------------------------------------------------------------------
#   getDefSurf - Get a default surface clause
#-----------------------------------------------------------------------------

def getDefSurf(refl=0):
  refstr = "'__HULLFORM__'"
  if refl == 1:
    refstr = refstr + ", REF"
  return refstr

#------------------------------------------------------------------------------
#  expandGeoRep - expand hull repetition clause
#------------------------------------------------------------------------------
def expandGeoRep(irepterm):
  pos = []
  numb = []
  offset = []
  prefix = ''
#
#  Remove white spaces
#
  srepterm = string.split(irepterm)
  repterm = string.joinfields(srepterm,"")
  for char in repterm[:]:
    if string.find( string.uppercase, char) >= 0:
      prefix = prefix + char
    else:
      break

  def expand_brep( prefix, term, pos, numb, offset):
    offstr = ''
    lpr = len(prefix)
    term = term[lpr:]
    lp = string.find( term, '(')
    rp = string.find( term, ')')

    op = string.find( term, '+')
    if op == -1:
      op = string.find( term[rp+2:], '-')
      if op != -1:
        op = op + rp+2
    if op != -1:
      offstr = term[op:]
      term = term[:op]

    if (lp > -1) & (lp < rp):
      try:
        first = string.atof( term[:lp])
      except:
        first = 0
      try:
        last = string.atof( term[rp+1:])
      except:
        last = 0
      try:
        step = string.atof( term[lp+1:rp])
      except:
        if first > last:
          step = -1
        else:
          step = 1
      try:
        nstep = int((last - first)/step) + 1
      except:
        nstep = 0
      coord = first
      print first, step, last, nstep
      for i in range(nstep):
        val = str(coord)
        if val[-2:] == ".0":
          val = val[:-2]
        if offstr != '':
          val = val + offstr
        pos.append( prefix + val)
        numb.append( coord)
        try:
          offset.append(string.atof( offstr))
        except:
          offset.append(0.0)
        coord = coord + step
    elif lp == -1 & rp == -1:
      pos.append( prefix + term)
      if offstr != '':
        pos[-1] = pos[-1] + offstr
      try:
        numb.append( string.atof( term))
      except:
        numb.append("")
      try:
        offset.append(string.atof( offstr))
      except:
        offset.append(0.0)

    return offset

  terms = string.splitfields(repterm, ",")
  for term in terms:
    expand_brep(prefix,term,pos,numb,offset)

  result = []
  result.append(pos)
  result.append(numb)
  result.append(offset)
  return result

#
#-----------------------------------------------------------------------------
#  Start of main body
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":

#  print getGeo(1,300)
#  print getGeoRepSSE(1,"",0,800,21000)
#  print getGeoRepSSE(1,"",-800,-800,-21000)
  numb = [1,2,4,5,6,7,8,10,11,12]
  print getGeoRepT(2,"LP",numb)
  numb = [1,2,3,4,5,6,7,9,10,11,12,13,14,15,17,18,19,20,21,22,23,25,26,27,28,29,30,31,33,34,35,36,37,38,39,41,42,43,44,45,46,47,49,50,51,52,53,54,55,57,58,59,60]
  print getGeoRepT(3,"",numb)
