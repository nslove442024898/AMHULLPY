## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

#-----------------------------------------------------------------------------
#   Class ReferenceSymbol - defining a note reference symbol
#-----------------------------------------------------------------------------
class ReferenceSymbol:

  def __init__(self, font=8, number=1, height=12.0):
    self.font = int(font)
    self.number = int(number)
    self.height = float(height)

  def getRecord(self):
    return (1, self.font, self.number, 0, 0, 0.0, 0.0, 0.0, 0.0, self.height, "")

#-----------------------------------------------------------------------------
#   Class Symbol - defining a free note symbol
#-----------------------------------------------------------------------------
class Symbol:

  def __init__(self, font=8, number=7, height=4.0, conn=0, u=0.0, v=0.0, rot=0.0, mirr=0):
    self.font = int(font)
    self.number = int(number)
    self.height = float(height)
    self.u = float(u)
    self.v = float(v)
    self.conn = int(conn)
    self.rot = float(rot)
    self.mirr = int(mirr)

  def position(self, u, v):
    self.u = float(u)
    self.v = float(v)

  def connection(self, conn):
    self.conn = int(conn)

  def mirror(self, mirr):
    self.mirr = int(mirr)

  def getRecord(self):
    return (2, self.font, self.number, self.conn, self.mirr, self.u, self.v, self.rot, 0.0, self.height, "")

#-----------------------------------------------------------------------------
#   Class Text - defining a free note text
#-----------------------------------------------------------------------------
class Text:

  def __init__(self, text=" ", height=3.5, font=0, u=0.0, v=0.0, slant=90.0, aspect=1.0):
    self.text = str(text)
    self.height = float(height)
    self.font = int(font)
    self.u = float(u)
    self.v = float(v)
    self.slant = float(slant)
    self.aspect = float(aspect)

  def position(self, u, v):
    self.u = float(u)
    self.v = float(v)

  def getRecord(self):
    return (11, self.font, 0, 0, 0, self.u, self.v, self.slant, self.aspect, self.height, self.text)

#-----------------------------------------------------------------------------
#   Class TextInSymbol - defining a note text placed by a symbol text position
#-----------------------------------------------------------------------------
class TextInSymbol:

  def __init__(self, text=" ", height=3.5, textpos=1, font=0, slant=90.0, aspect=1.0):
    self.text = str(text)
    self.height = float(height)
    self.conn = textpos
    self.font = int(font)
    self.slant = float(slant)
    self.aspect = float(aspect)

  def getRecord(self):
    return (12, self.font, 0, self.conn, 0, 0.0, 0.0, self.slant, self.aspect, self.height, self.text)

#
#-----------------------------------------------------------------------------
#  Self test
#-----------------------------------------------------------------------------
#
if __name__ == "__main__":

  print "testing ReferenceSymbol"
  ref = ReferenceSymbol(8, 1, 3)
  print ref.getRecord()

  print "testing Symbol"
  symb = Symbol(8, 7, 12)
  symb.position(5.0, 0.5)
  symb.connection(2)
  symb.mirror(2)
  print symb.getRecord()

  print "testing Text"
  text = Text("hello note", 5)
  text.position(0, -6)
  print text.getRecord()

  print "testing TextInSymbol"
  symbtext = TextInSymbol(text="hello symbol", textpos=2, font=3)
  print symbtext.getRecord()
