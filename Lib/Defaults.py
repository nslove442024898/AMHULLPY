## Copyright 1974 to current year. AVEVA Solutions Limited and its subsidiaries. All rights reserved in original code only.

"""Default file handling classes v.1.310"""

import string
import kcs_util
import kcs_ui
import KcsStringlist

OK = kcs_util.ok()

# --------------------------------------------------------
# Validating functions
# --------------------------------------------------------

def LowerLimitCheck(value, args):
  res = value >= args
  if res == 0:
    kcs_ui.message_confirm("Input should be >= " + str(args) + "!")
  return (res, value)

def UpperLimitCheck(value, args):
  res = value <= args
  if res == 0:
    kcs_ui.message_confirm("Input should be <= " + str(args) + "!")
  return (res, value)

def RangeCheck(value, args):
  res = args[0] <= value <= args[1]
  if res == 0:
    kcs_ui.message_confirm("Input should lie between " + str(args[0]) + " and " + str(args[1]) + "!")
  return (res, value)

# Default validating function accepting automatically the input
def __ValidateOK__(value, args):
  return (1, value)

# --------------------------------------------------------

class DefaultFileItem:
  """Base class for any kind of defaults
Attributes:
   name      - name of the default
   init      - initial value
   value     - current value
   question  - question asked, when prompting for a new value
   fValidate - additional validating function (1 - test passed, 0 - test failed)
   fArgs     - arguments to the validating function"""

  def __init__(self, name, init_value, Question=""):
    """Constructor method:

name       - default name
init_value - initial value for the default
Question   - question asked, when prompting for the new value of the default"""
    self.name = name
    self.value = init_value
    self.init = init_value # Should be valid!
    if Question == "":
      self.question = "Input " + name
    else:
      self.question = Question
    self.SetValidate()

  def SetValidate(self, func=__ValidateOK__, args=None):
    """Defines an additional validating function, and its arguments.
Validation function should have the form:
    Validate(val, args) -> (status, new value)

where status can be either 1 (test passed) or 0 (test failed), and
additionally the function can decide to return a modified value 'val'
as 'new value'.
NOTE! When an exception is raised during the execution of the validating
function, the input is treated as rejected!

The default func argument causes the validation to be removed"""
    self.fValidate = func
    self.fArgs = args

  def ValidateItem(self, val):
    """<object>.ValidateItem(val) -> (status, new value)

Performs additional validation by calling the fValidate function.
status can be either 1 (passed) or 0 (failed)."""
    try:
      res = self.fValidate(val, self.fArgs)
    except:
      res = (0, val)
    return res

  def StrToItem(self, svalue):
    """<object>.StrToItem(svalue) -> (status, item's value)

Performs conversion from a string to an item's type.
Returns a tuple. If status is 1 (NON-ZERO), conversion was successful.
Status of 0, OR AN EXCEPTION means, that the conversion failed!
Should be redefined in child classes"""
    pass

  def ItemToStr(self):
    """<object>.ItemToStr() -> string

Returns the string representation of the item"""
    return str(self.value)

  def SetFromString(self, svalue):
    """<object>.SetFromString(svalue) -> status

Tries to convert the string 'svalue' to the item's data type.
If successful, sets the default's value to the converted value.
Returns 1, if the conversion was successful, or 0, if it failed"""
    try:
      status, val = self.StrToItem(svalue)
    except:
      status = 0
    if status:
      status, val = self.ValidateItem(val)
    if status:
      self.value = val
    return status

  def Prompt(self):
    """<object>.Prompt() -> (status, data)

Asks the user for a new value for the default. Returns the status of OK
to indicate success.
Should be redefined in child classes"""
    pass

  def EditItem(self):
    """<object>.EditItem() -> status

Edits the current value of an item. If not cancelled, and successful,
returns 1, or 0, if the user cancelled the edit."""
    while 1:
      try:
        res = self.Prompt()
      except:
        return 0
      if res[0] == OK:
        res = self.ValidateItem(res[1])
        if res[0] != 0:
          self.value = res[1]
          return 1
      else:
        return 0

  def ResetItem(self):
    """Resets the default's value to the initial value"""
    self.value = self.init

  def UpdateInitial(self):
    """Saves current value as the default initial value"""
    self.init = self.value

# --------------------------------------------------------------------

class StrDefItem(DefaultFileItem):
  """Default with a string value"""
  def StrToItem(self, svalue):
    return (1, string.strip(svalue))
  def Prompt(self):
    res = kcs_ui.string_req(self.question, self.value)
    return (res[0], string.strip(res[1]))
# --------------------------------------------------------------------

class UpStrDefItem(DefaultFileItem):
  """Default with a uppercase string value"""
  def StrToItem(self, svalue):
    return (1, string.upper(string.strip(svalue)))
  def Prompt(self):
    res = kcs_ui.string_req(self.question, self.value)
    return (res[0], string.upper(string.strip(res[1])))

# --------------------------------------------------------------------

class IntDefItem(DefaultFileItem):
  """Default with an integer value"""
  def StrToItem(self, svalue):
    return (1, string.atoi(svalue)) # If conversion fails, an exception will be raised!
  def Prompt(self):
    return kcs_ui.int_req(self.question, self.value)

# --------------------------------------------------------------------

class RealDefItem(DefaultFileItem):
  def StrToItem(self, svalue):
    return (1, string.atof(svalue)) # If conversion fails, an exception will be raised!
  def Prompt(self):
    return kcs_ui.real_req(self.question, self.value)

# --------------------------------------------------------------------

class EnumDefItem(DefaultFileItem):
  def __init__(self, name, init_value, alternatives, Question=""):
    """The enumerated default item class should be provided with
alternatives being a Stringlist class instance with the items
to choose from.
In this case self.value is the index of the chosen item in the list,
counting from 1 upwards."""
    self.choices = alternatives
    self.uchoices = map(string.upper, alternatives.StrList)
    DefaultFileItem.__init__(self, name, init_value, Question)
  def ItemToStr(self):
    try:
      s = self.choices.StrList[self.value-1]
    except:
      s = ''
    return s
  def StrToItem(self, svalue):
    # index method can raise an exception, if the given string is not found!
    return (1, self.uchoices.index(string.upper(svalue))+1)
  def Prompt(self):
    return (OK, 1 + self.value % len(self.uchoices))

# --------------------------------------------------------------------

class YesNoDefItem(DefaultFileItem):
  Answer = ['', 'NO', 'YES']      # Standard text representations of N/A, False, True
  NO = ['N', 'NO', 'FALSE', '0']  # Possible text forms of a negative answer
  YES = ['Y', 'YES', 'TRUE', '1'] # Possible text forms of a positive answer
  def __init__(self, name, init_value):
    DefaultFileItem.__init__(self, name, self.TruthValue(init_value))
  def TruthValue(self, val):
    """<object>.TruthValue(val) -> integer

Tries to convert value 'val' to an integer indicating its truth value"""
    if type(val) == type('A'):
      s = string.upper(val)
      if s in self.NO: res = 0
      elif s in self.YES: res = 1
      else: res = -1
    elif val: res = 1
    else: res = 0
    return res
  def StrToItem(self, svalue):
    res = self.TruthValue(svalue)
    return (res != -1, res)
  def ItemToStr(self):
    return self.Answer[self.value + 1]
  def Prompt(self):
    return (OK, 1 - self.value)

# --------------------------------------------------------------------

class Defaults:
  """Managing a list of defaults"""
  def __init__(self, defList, Title, Header):
    self.defaults = defList
    self.use_choice = (len(defList) < 20)
    self.unames = []
    for d in defList:
      self.unames.append(string.upper(d.name))
    self.title = Title
    self.header = Header
    self.CommentChar = '!'
    self.GetChoices()

  def GetDefLine(self, default):
    """<object>.GetDefLine(default) -> string

Returns a string to be displayed in the alternatives window"""
    return default.name + ' = ' + default.ItemToStr()

  def GetChoices(self):
    """Prepares a list of choices for editing defaults"""
    dList = KcsStringlist.Stringlist(self.GetDefLine(self.defaults[0]))
    for d in self.defaults[1:]:
      dList.AddString(self.GetDefLine(d))
    dList.AddString("OK")
    self.nchoices = len(self.defaults) + 1
    self.choices = dList

  def Edit(self, FileName=""):
    """Edit defaults, as long, as the user picks the defaults to edit"""
    OPTIONS = kcs_util.options()
    res = [OK]
    while res[0] == OK:
      if self.use_choice:
        res = kcs_ui.choice_select(self.title, self.header, self.choices)
      else:
        res = kcs_ui.string_select(self.title, self.header, 'Choose a default and click OK', \
                                   self.choices)
      if res[0] == OK:
        ind = res[1]
        if ind < self.nchoices:
          d = self.defaults[ind-1]
          if d.EditItem() == 1:
            self.choices.StrList[ind-1] = self.GetDefLine(d)
        else:
          return OK
      elif res[0] == OPTIONS:
        res = [OK]
        if FileName != "":
          ask = kcs_ui.answer_req(self.title, \
                "Do you want to save current values as defaults?")
          if ask == kcs_util.yes(): self.WriteToFile(FileName)
      else:
        return kcs_util.cancel()

  def GetDefDict(self):
    """Returns a dictionary of all defaults"""
    dict = {}
    for d in self.defaults:
      dict[d.name] = d.value
    return dict

  def __getitem__(self, key):
    """Allows to use the syntax <object>[default name] to retrieve the default values"""
    ukey = string.upper(key)
    try:
      ind = self.unames.index(ukey)
      return self.defaults[ind].value
    except:
      raise KeyError, "Unknown default name: " + key

  def LoadFromFile(self, FileName, UnknownWarning = 1):
    """Updates defaults from a file. Ignores comment lines, unknown keywords.
Result:
  -2 - possibly some unknown keywords, some value errors
  -1 - some unknown keywords, no value errors
   0 - success (no unknown keywords, no value errors)
   1 - file not found (or could not be opened)
   2 - file read error

In most cases the result <= 1 could be considered as a success, if only the program
initializes the defaults structure with initial values suitable for most applications.

If UnknownWarning == 0, the existence of unknown keywords is not recorded in the result, so
there should be no return value of -1."""
    try:
      status = 1 # Error opening the file
      file = open(FileName, "r")
      status = 0 # success
      try:
        row = file.readline()
        while row != "":
          if row[0] != self.CommentChar:
            data = string.splitfields(row, '=', 1)
            key = string.strip(data[0])
            value = string.strip(data[1])
            ukey = string.upper(key)
            try:
              ind = self.unames.index(ukey)
              d = self.defaults[ind]
              if d.SetFromString(value) == 0:
                print "Invalid value for the default %s (%s)!" % (key, value)
                status = -2 # Invalid value of the default
            except:
              if UnknownWarning:
                print "Unknown default name (%s)!" % key
                if status != -2: status = -1
          row = file.readline()
        kcs_ui.message_noconfirm("Defaults loaded from file " + FileName)
      finally:
        file.close()
    except:
      if status == 1:
        s = "Default file %s not found. Default configuration used"
      else:
        s, status = "Error reading default file %s!", 2
      kcs_ui.message_noconfirm(s % FileName)
    self.GetChoices()
    return status

  def WriteToFile(self, FileName):
    """Stores all defaults on a file.
Returns:
  0 - errors writing the file
  1 - success"""
    status = 0 # Error
    try:
      file = open(FileName, "w")
      try:
        for d in self.defaults:
          file.write(d.name + " = " + d.ItemToStr() + "\n")
        status = 1 # Success
        kcs_ui.message_noconfirm("Defaults stored in file " + FileName)
      finally:
        file.close()
    except:
      kcs_ui.message_confirm("Error writing default file %s!" % FileName)
    return status

  def ResetDefaults(self):
    """Resets all the defaults to their initial values"""
    for d in self.defaults:
      d.ResetItem()
    self.GetChoices()

  def UpdateInitial(self):
    """Saves current values of all defaults as their default initial values"""
    for d in self.defaults:
      d.UpdateInitial()
