import os,string,sys,cmt,time
from lcg import msg
from lcg.aa import config
from lcg.aa.spi import checkPackageXml, lcgdb_fill, ghostPackage
from datetime import date

import cgi,MySQLdb

class fill_mysql:

  def __init__(self, msgLevel,reldate=''):
    cmtextra = os.environ.get('CMTEXTRATAGS')
    if not cmtextra : cmtextra = ''
    if not cmtextra or 'NOPYLCG' not in map(lambda x: x.strip(),cmtextra.split(',')) :
      if cmtextra : cmtextra += ','
      cmtextra += 'NOPYLCG'
      os.environ['CMTEXTRATAGS'] = cmtextra
    self.cfg = config.config()
    self.argv0 = sys.argv[0]
    self.lcgcmtroot = self.cfg.lcg_lcgcmtroot_dir
    self.all_interface_dirs_lower = []
    self.all_interface_dirs = []
    self.all_builder_dirs = []
    self.interface_dirs = []
    self.builder_dirs = []
    self.pkg_low2real_dict = {'cmt':'CMT'}
    self.pkg_vers_dict = {}
    self.cmt = cmt.CMT()
    self.msgLevel = msgLevel
    self.msg = msg.msg(os.path.basename(self.argv0), self.msgLevel)

    self.lcgcmt             = {}
    self.lcgcmt['general']  = {}
    self.lcgcmt['plat_def'] = {}
    self.lcgcmt['pkg']      = {}

    self.reldate = time.time()
    if reldate : self.reldate = time.mktime(date(reldate[0],reldate[1],reldate[2]).timetuple())
      

  def filter_out(self,x):
    if x in self.filterItems : return False
    return True

  def checkInterfacesAndBuilders(self):
    os.chdir(self.lcgcmtroot)

    self.all_interface_dirs = os.listdir(os.curdir + os.sep + 'LCG_Interfaces')
    self.all_interface_dirs_lower = map(string.lower, self.all_interface_dirs)
    self.all_builder_dirs = os.listdir(os.curdir + os.sep + 'LCG_Builders')

    self.filterItems = ['CVS','.svn','LCG_BuildPolicy','LCG_BuildRelease']

    self.interface_dirs = filter(self.filter_out, self.all_interface_dirs)
    self.builder_dirs   = filter(self.filter_out, self.all_builder_dirs)

    comp_interface_dirs = map (lambda x: string.lower(x), self.interface_dirs)
    comp_builder_dirs   = map (lambda x: string.lower(x), self.builder_dirs)
    flt_bld = comp_builder_dirs
    flt_int = comp_interface_dirs

    self.filterItems = flt_bld
    comp_interface_dirs = filter(self.filter_out, comp_interface_dirs)
    self.filterItems = flt_int
    comp_builder_dirs = filter(self.filter_out, comp_builder_dirs)

    if comp_builder_dirs : self.msg.warning('Directories found in LCG_Builders which do not appear in LCG_Interfaces: %s' %comp_builder_dirs)
    if comp_interface_dirs :
      self.msg.warning('Directories found in LCG_Interfaces which do not appear in LCG_Builders: %s ' % comp_interface_dirs)
      self.msg.warning('Only the information in LCG_Builders will be used for filling the database')

    self.msg.info('Using the following packages for filling mysql: %s' % self.builder_dirs)

    for x in self.interface_dirs+self.builder_dirs :
      if x not in self.pkg_low2real_dict.keys() :
        if self.cfg.isProject(x) : self.pkg_low2real_dict[x] = x
        else                     : self.pkg_low2real_dict[x.lower()] = x

  def processGeneralInfo(self,pkgData) :
    self.cmt.init_macros()
    self.cmt.init_sets()

    lcgver = self.cmt.macros['LCG_config_version']
    self.lcgcmt['general']['name'] = lcgver

    pkg = pkgData.get('package')[0]

    relfound = False
    for x in pkg.get('note'):
      if x['attrs']['version'] == lcgver :
        relfound = True
        dt = x['attrs']['date'].split('-')
        self.lcgcmt['general']['rel_date'] = time.mktime((int(dt[0]),int(dt[1]),int(dt[2]),0,1,0,0,0,0))
        self.lcgcmt['general']['motivation'] = x['cont']

    if not relfound :
      self.msg.error('No release info found for %s in LCG_Builders/LCGCMT/xml/package.xml'%lcgver)
      self.lcgcmt['general']['rel_date'] = time.mktime((0,0,0,0,0,0,0,0,0))
      self.lcgcmt['general']['motivation'] = ''

  def checkPlatforms(self):
    pass

  def genLcgcmtPlatDict(self):

    for p in self.cfg.release_platform_tags :
      if p.count("_") >= 2 : # "old" platform style
        pelems = p.split('_')    
        self.lcgcmt['plat_def'][p]         = {}
        self.lcgcmt['plat_def'][p]['os']   = pelems[0]
        self.lcgcmt['plat_def'][p]['arch'] = pelems[1]
        self.lcgcmt['plat_def'][p]['comp'] = pelems[2]
      else : # "new" platform style
        pelems = p.split("-")
        self.lcgcmt['plat_def'][p]         = {}
        self.lcgcmt['plat_def'][p]['os']   = pelems[1]
        self.lcgcmt['plat_def'][p]['arch'] = pelems[0]
        self.lcgcmt['plat_def'][p]['comp'] = pelems[2]

      # FIXME - do we want to have debug info here?

    self.lcgcmt['platforms'] = self.cfg.release_platform_tags

  def processPlatforms(self):
    self.genLcgcmtPlatDict()


  def genLcgcmtPkgDict(self, pkgData) :

    pkg = pkgData.get('package')[0]

    deps = [] # pkg.get('dependencies')[0]
    cont = pkg.get('contact')
    home = pkg.get('homepage')[0]['cont']
    desc = pkg.get('description')[0]['cont']
    lice = pkg.get('license')[0]['cont']
    ldes = ''
    if pkg.get('longDescription') :
      ldes = pkg['longDescription'][0]['cont']

    pkgAtt = pkg['attrs']
    catg = pkgAtt.get('category')
    lang = pkgAtt.get('language')
    ispr = pkgAtt.get('project')
    name = pkgAtt.get('name')
    if name == 'cmt_itself' : name = 'cmt'
    vers = pkgAtt.get('version')

    if not vers : return

    if string.lower(ispr) == 'true' : ispr = 1
    else                            : ispr = 0

    self.lcgcmt['pkg'][name] = {}
    self.lcgcmt['pkg'][name]['version'] = {}
    self.lcgcmt['pkg'][name]['version'][vers] = {}
    self.lcgcmt['pkg'][name]['version'][vers]['dep'] = deps
                 ### if package is new, add: ###
    self.lcgcmt['pkg'][name]['contact'] = {}
    for cnt in cont :
      cntlst = cnt['cont'].split()
      self.lcgcmt['pkg'][name]['contact'][' '.join(cntlst[:-1])] = cntlst[-1]
    self.lcgcmt['pkg'][name]['homepage'] = home
    self.lcgcmt['pkg'][name]['short_descrip'] = desc
    self.lcgcmt['pkg'][name]['long_descrip'] = ldes
    self.lcgcmt['pkg'][name]['category'] = catg
    self.lcgcmt['pkg'][name]['language'] = lang
    self.lcgcmt['pkg'][name]['afs_relpath'] = pkgAtt.get('afsrel')

    self.lcgcmt['pkg'][name]['is_project'] = ispr

                 ### if version is new, add: ###
    self.lcgcmt['pkg'][name]['version'][vers]['platform'] = {}
    for pname in self.cfg.release_platform_tags :
      srctb = pkgAtt['tarfilename']
      bintb = ''
      if pname in self.cfg.tarball_platform_tags :
        bintb = self.cfg.build_pkg_tarball_name(self.pkg_low2real_dict[name],vers,pname)
      self.lcgcmt['pkg'][name]['version'][vers]['platform'][pname] = {}
      self.lcgcmt['pkg'][name]['version'][vers]['platform'][pname]['src_tarball'] = srctb
      self.lcgcmt['pkg'][name]['version'][vers]['platform'][pname]['bin_tarball'] = bintb

  def enhancePackage(self, pkg, data):
    # needed for LCG_destdir
    os.putenv('CMTSITE','CERN')
    os.chdir(self.lcgcmtroot + os.sep + 'LCG_Builders' + os.sep + pkg + os.sep + 'cmt')
    self.cmt.init_macros()
    self.cmt.init_sets()
    pkgAttrs = data['package'][0]['attrs']
    pkgAttrs['name'] = self.cmt.macros['package']
    pkgAttrs['version'] = self.cmt.macros[pkg+'_build_config_version']
    pkgAttrs['afsrel'] = os.popen('cmt show set_value LCG_destdir').read()[:-1]
    pkgAttrs['tarfilename'] = os.popen('cmt show set_value LCG_tarfilename').read()[:-1]

    #Pkg = self.all_interface_dirs[self.all_interface_dirs_lower.index(pkg)]
    #os.chdir(self.lcgcmtroot + os.sep + 'LCG_Interfaces' + os.sep + Pkg + os.sep + 'cmt')
    #elf.cmt.init_macros()

  def processPackage(self, pkg):
    os.chdir(self.lcgcmtroot + os.sep + 'LCG_Builders' + os.sep + pkg + os.sep + 'cmt')
    cpx = checkPackageXml.checkPackageXml(msgLevel=self.msgLevel)
    pkgData = cpx.check()
    if pkgData:
      if pkg == 'LCGCMT' : self.processGeneralInfo(pkgData)
      self.enhancePackage(pkg, pkgData)
      self.genLcgcmtPkgDict(pkgData)


  def collectAllPkgVersions(self):

    gp = ghostPackage.ghostPackage(self.cmt)
    gp.allInterfacesCreate()

    cmtconfig_save = os.getenv('CMTCONFIG')
    for conf in self.cfg.release_platform_tags:
      self.pkg_vers_dict[conf] = gp.allInterfacesCollectVersions(conf)

    os.putenv('CMTCONFIG',cmtconfig_save)

    gp.allInterfacesRemove()
      

  def fill(self,test=False):
    
    self.checkInterfacesAndBuilders()
    self.collectAllPkgVersions()

    self.filterItems = self.cfg.not_lcgaa_packages
    filter(self.filter_out, self.builder_dirs)
    if test:
      self.processPackage('python')
      self.processPackage('LCGCMT')
    else:
      map ( self.processPackage, self.builder_dirs )
    self.checkPlatforms()
    self.processPlatforms()

    cf = lcgdb_fill.confFill(self.lcgcmt, self.msgLevel)
    cf.dbFill()


if __name__ == '__main__':

  fm = fill_mysql(msgLevel='INFO',reldate=(1971,11,27))
  fm.fill(test=False)
