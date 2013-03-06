
msgLevelDictionary = { 'ALL': 1, 'DEBUG': 10, 'INFO': 20, 'WARNING': 30, 'ERROR': 40, 'FATAL': 50, 'NEVER': 100}

class msg :

  def __init__(self, argv0, msgLevel='ALL', preAmble=''):
    self.argv0 = argv0
    self.preAmble = preAmble
    self.msgLevelDict = msgLevelDictionary
    self.msgLevel = self.msgLevelDict['ALL']
    if msgLevel in self.msgLevelDict.keys() : self.msgLevel = self.msgLevelDict[msgLevel]

  def __printLiteral(self, typ, msg, postReturn, preReturn, txtOnly):
    while msg and msg[-1] == '\n': msg = msg[:-1]
    if preReturn  : print
    if txtOnly    : print '%s' % msg,
    else          : print '%s: %s: %s%s' % ( self.argv0, typ, self.preAmble, msg),
    if postReturn : print

  def __printList(self, typ, msgL, postReturn, preReturn, txtOnly):
    for l in msgL[:-1] : self.__printLiteral(typ, l, True, preReturn, txtOnly)
    self.__printLiteral(typ, msgL[-1], postReturn, preReturn, txtOnly)

  def __printMsg(self, typ, msg, postReturn, preReturn, txtOnly):
    if msg.__class__.__name__ == 'list': self.__printList(typ, msg, postReturn, preReturn, txtOnly)
    else                               : self.__printLiteral(typ, msg, postReturn, preReturn, txtOnly)

  def __preReturn(self, infoLvl):
    if self.msgLevel >= infoLvl : return True
    return False

  def setPreAmble(self, txt):
    self.preAmble = txt

  def setMsgLevel(self, lvl):
    self.msgLevel = lvl

  def fatal(self, msg, postReturn=True, preReturn='NEVER', txtOnly=False):
    if self.msgLevel <= self.msgLevelDict['FATAL']:
      self.__printMsg('FATAL ', msg, postReturn, self.__preReturn(preReturn), txtOnly)
    
  def error(self, msg, postReturn=True, preReturn='NEVER', txtOnly=False):
    if self.msgLevel <= self.msgLevelDict['ERROR']:
      self.__printMsg('ERROR  ', msg, postReturn, self.__preReturn(preReturn), txtOnly)

  def warning(self, msg, postReturn=True, preReturn='NEVER', txtOnly=False):
    if self.msgLevel <= self.msgLevelDict['WARNING']:
      self.__printMsg('WARNING', msg, postReturn, self.__preReturn(preReturn), txtOnly)

  def info(self, msg, postReturn=True, preReturn='NEVER', txtOnly=False):
    if self.msgLevel <= self.msgLevelDict['INFO']:
      self.__printMsg('INFO   ', msg, postReturn, self.__preReturn(preReturn), txtOnly)

  def debug(self, msg, postReturn=True, preReturn='NEVER', txtOnly=False):
    if self.msgLevel <= self.msgLevelDict['DEBUG']:
      self.__printMsg('DEBUG  ', msg, postReturn, self.__preReturn(preReturn), txtOnly)
  
