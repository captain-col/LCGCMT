from lcg.aa import config
import os,shutil

class ghostPackage:

  def __init__(self, cmt, projRoot=''):
    self.cfg = config.config()
    self.cmt = cmt
    self.projRoot = projRoot
    if not self.projRoot : self.projRoot = self.cfg.lcg_lcgcmtroot_dir

  def allInterfacesCreate(self):
    all_interface_dirs = os.listdir(self.cfg.lcg_lcgcmtroot_dir + os.sep + 'LCG_Interfaces')

    os.chdir(self.projRoot)
    pkg = 'LCG_AllInterfaces'
    pkgcmt = pkg + os.sep + 'cmt'
    if os.path.isdir(pkgcmt) : self.allInterfacesRemove()
    else                     : os.makedirs(pkgcmt)
    os.chdir(pkgcmt)
    f = open('requirements','w')
    f.write('package LCG_AllInterfaces\n\n')
    map(lambda x: f.write('use %s v* LCG_Interfaces\n' % x), all_interface_dirs)
    f.close()

  def allInterfacesCollectVersions(self, cmtconfig='') :
    versdict = {}
    if cmtconfig : os.putenv('CMTCONFIG',cmtconfig)
    self.cmt.init_macros()
    for m in self.cmt.macros.keys() :
      if m[-15:] == '_native_version' :
        pkgname = m[:-15]
        cfgname = pkgname + '_config_version'
        homename = pkgname + '_home'
        ntvvers = self.cmt.macros[m]
        cfgvers = ''
        pkghome = ''
        if self.cmt.macros.has_key(cfgname) : cfgvers = self.cmt.macros[cfgname]
        if self.cmt.macros.has_key(homename) : pkghome = self.cmt.macros[homename] 
        versdict[pkgname] = (cfgvers,ntvvers,pkghome)
    return versdict


  def allInterfacesRemove(self):
    shutil.rmtree(os.path.join(self.projRoot, 'LCG_AllInterfaces'))
