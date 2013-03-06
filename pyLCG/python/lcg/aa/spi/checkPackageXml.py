import os,sys,cmt,shutil,xparser,urllib
import lcg.msg
import lcg.aa.config

class checkPackageXml :

  def __init__(self, msgLevel='ALL'):

    self.argv0 = sys.argv[0]
    self.cmt = cmt.CMT()

    self.cfg = lcg.aa.config.config()

    self.pkgRoot = self.cmt.macros['PACKAGE_ROOT']
    self.pkgName = self.pkgRoot.split(os.sep)[-1]

    self.msgLevel = msgLevel
    self.msg = lcg.msg.msg(os.path.basename(self.argv0), self.msgLevel, '[%s] '% self.pkgName)

    if 'LCG_Builders' not in self.pkgRoot.split(os.sep) :
      self.msg.debug('Package %s is not a builder package - skipping' % self.pkgRoot)
    
    self.xmlDir = '%s%sxml' % (self.cmt.macros['PACKAGE_ROOT'], os.sep)
    self.dtdDir = '%s%sxml' % (self.cmt.macros['LCG_BUILDPOLICYROOT'], os.sep)
    self.xmlFileBase = 'package.xml'
    self.dtdFileBase = 'package.dtd'
    self.xmlFile = '%s%s%s' % ( self.xmlDir, os.sep, self.xmlFileBase)
    self.dtdFile = '%s%s%s' % ( self.dtdDir, os.sep, self.dtdFileBase)

    self.err = 0
    self.data = None

  def xmlFileExists(self):
    self.msg.debug('Check existance of file %s -' % self.xmlFile, postReturn=False)
    if not os.path.isfile(self.xmlFile) :
      self.msg.error('file %s does not exist' % self.xmlFile, preReturn='INFO')
    else :
      self.msg.debug('OK',txtOnly=True)
      return 1
    return 0

  def copyDTD(self):
    self.msg.debug('Copying DTD file %s to %s -' % (self.dtdFile, self.xmlDir), postReturn=False)
    if not os.path.isfile(self.dtdFile) :
      self.msg.error('Could not find DTD file %s' % self.dtdFile, preReturn='INFO')
    elif not os.path.isdir(self.xmlDir) :
      self.msg.error('Destination directory %s does not exist' % self.xmlDir, preReturn='INFO')
    else:
      shutil.copyfile(self.dtdFile,self.xmlDir+os.sep+self.dtdFileBase)
      self.msg.debug('OK',txtOnly=True)
      return 1
    return 0
      
  def readXml(self):
    self.msg.debug('Reading %s file - ...' % self.xmlFileBase)
    parser = xparser.xparser(self.msgLevel,self.pkgName)
    self.data = parser.parseSource(self.xmlFile)
    if self.data:
      self.msg.debug('Reading %s file - OK' % self.xmlFileBase)
      return 1
    else :
      self.msg.error('Reading %s file - FAILED' % self.xmlFileBase)
      self.err = 1
      return 0

  def checkXmlData(self):

    err = 0
    self.msg.debug('Checking contact person -', postReturn=False)
    pers = self.data['package'][0]['contact'][0]['cont']
    if len(pers.split()) < 3 or pers.split()[-1].find('@') == -1:
      self.msg.warning('Format of contact person should be <Given Name> <Surname> <email>, found %s' % pers, preReturn='INFO')
      err = 1
      self.err = 1
    if err : self.msg.error('Checking contact person - FAILED')
    else   : self.msg.debug('OK',txtOnly=True)

    err = 0
    self.msg.debug('Checking homepage -', postReturn=False)
    hpg = self.data['package'][0]['homepage'][0]['cont']
    try :
      urllib.urlopen(hpg)
    except Exception,e:
      self.msg.error('Could not contact URL %s, error was: %s' % (hpg, e), preReturn='INFO')
      err = 1
      self.err = 1
    if err : self.msg.error('Checking homepage - FAILED')
    else   : self.msg.debug('OK',txtOnly=True)

    err = 0
    self.msg.debug('Checking description -', postReturn=False)
    desc = self.data['package'][0]['description'][0]['cont']
    if len(desc.split()) < 5 :
      self.msg.warning('Description less than 5 words', preReturn='INFO')
      err = 1
      self.err = 1
    if err : self.msg.error('Checking description - FAILED')
    else   : self.msg.debug('OK',txtOnly=True)

    err = 0
    self.msg.debug('Checking license -', postReturn=False)
    lic = self.data['package'][0]['license'][0]['cont']
    lic = lic.strip()
    if not lic :
      self.msg.warning('No license information found', preReturn='INFO')
      err = 1
      self.err = 1
    if lic not in self.cfg.licenses :
      self.msg.warning('License %s not in list of licenses %s, re-name license or enhance LCG/AA license file' % ( lic, self.cfg.licenses ), preReturn='INFO')
      err = 1
      self.err = 1
    if err : self.msg.error('Checking license - FAILED')
    else   : self.msg.debug('OK',txtOnly=True)
      

  def check(self):

    self.msg.debug('*'*80)
    self.msg.info('processing package')
    self.msg.debug('CHECK PACKAGE "%s" - STARTING' % self.pkgRoot)
    if self.xmlFileExists() :
      if self.copyDTD() :
        if self.readXml() :
          self.checkXmlData()
    if self.err: self.msg.error('ERRORS occured during parsing package %s' % self.pkgRoot)
    else       : self.msg.debug('CHECK PACKAGE "%s" - FINISHED' % self.pkgRoot)
    self.msg.debug('*'*80)

    return self.data


if __name__ == "__main__" :

  cpx = checkPackageXml()
  cpx.check()
