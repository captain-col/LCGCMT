from xml.parsers.xmlproc import xmlval
from lcg import msg
import os,sys

#================================================================================
class PackageXmlParser (xmlval.Application):
#--------------------------------------------------------------------------------
  def __init__(self, filename, msgLevel='ALL', pkgName=''):
    self.msgLevel = msgLevel
    self.pkgName = pkgName
    self.msg = msg.msg(os.path.basename(sys.argv[0]), self.msgLevel, '[%s] '%self.pkgName)
    self.filename = filename
    #self.elemstack = []
    self.data = {}
    self.locator = 0
    self.cdata = ''
#--------------------------------------------------------------------------------
  def handle_doctype(self,root,pubID,sysID):
    pass
#--------------------------------------------------------------------------------  
  def doc_start(self):
    self.msg.debug('Parsing Source File %s -' % self.filename, postReturn=False)
#--------------------------------------------------------------------------------
  def doc_end(self):
    self.msg.debug('OK', txtOnly=True)
#--------------------------------------------------------------------------------
  def handle_comment(self,data):
    pass
#--------------------------------------------------------------------------------
  def handle_data(self,data,start,end):
    self.cdata += data[start:end]
#--------------------------------------------------------------------------------
  def handle_start_tag(self,name,attr):
    currdic = self.data
    for stackelem in self.locator.get_elem_stack():
      currdic = currdic[stackelem][-1]
    if currdic.has_key(name):
      currdic[name].append({'attrs':attr})
    else:
      currdic[name] = [{'attrs':attr}]
#--------------------------------------------------------------------------------
  def handle_end_tag(self,name):
    if len(self.cdata):
      currdic = self.data
      for stackelem in self.locator.get_elem_stack():
        currdic = currdic[stackelem][-1]
      currdic[name][-1]['cont'] = self.cdata
      self.cdata = ''
#--------------------------------------------------------------------------------
  def handle_ignorable_data(self, data, start, end):
    pass
#--------------------------------------------------------------------------------
  def handle_pi(self, target, data):
    pass
#--------------------------------------------------------------------------------
  def set_entity_info(self,xmlver,enc,sddecl):
    pass
#--------------------------------------------------------------------------------
  def set_locator(self, locator):
    self.locator = locator  
  

#================================================================================
class xparser:
#--------------------------------------------------------------------------------  
  def __init__(self,msgLevel='ALL',pkgName=''):
    self.msgLevel = msgLevel
    self.pkgName = pkgName
    self.parser = xmlval.XMLValidator()
#--------------------------------------------------------------------------------
  def parseSource(self,sourcefile):
    try:
      parser = xmlval.XMLValidator()
      packParser = PackageXmlParser(sourcefile,self.msgLevel,self.pkgName)
      self.parser.set_application(packParser)
      self.parser.parse_resource(sourcefile)
      return packParser.data['lcg'][0]
    except :
      pass
