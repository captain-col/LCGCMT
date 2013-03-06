
import cmt,os,sys,string
from optparse import OptionParser
from lcg.aa.spi import ghostPackage
from lcg.aa import config
from lcg import msg

class make_tarballs :

  def __init__(self,lcgcmt,cmtconfig,pkglist,verbose,force,dry):

    self.cfg = config.config()
    self.argv0 = sys.argv[0]
    self.msg = msg.msg(os.path.basename(self.argv0))
    self.dry = dry
    self.verbose = verbose
    self.force = force

    if cmtconfig :
      self.msg.error('option -c/--cmtconfig not implemented yet, please set $CMTCONFIG')
      sys.exit(1)

    self.package_results = {}
    self.project_results = {}
    self.packages = {}
    self.sel_packages = pkglist
    self.cmtconfig = cmtconfig
    self.lcgsystem = ''
    self.tarball_platform_tags = self.cfg.tarball_platform_tags
    self.tarball_platform_tags += ['src','doc']    
    if os.environ.has_key('CMTCONFIG') :
      self.cmtconfig = os.environ['CMTCONFIG']
      if self.cmtconfig not in self.cfg.tarball_platform_tags :
        self.msg.error('%s is not a tar platform, change $CMTCONFIG' % self.cmtconfig)
        sys.exit(1)
      if self.cmtconfig[-4:] == '_dbg' :
        self.lcgsystem = self.cmtconfig[:-4]
      else:
        self.lcgsystem = self.cmtconfig
    else:
      self.msg.error('environment variable CMTCONFIG not set, please set')
      sys.exit(1)
      
    self.start_dir = os.path.realpath(os.curdir)
    self.lcgcmt_dir = ''
    if lcgcmt : self.lcgcmt_dir = lcgcmt
    else      : self.lcgcmt_dir = self.cfg.lcg_lcgcmtroot_dir
    self.cmt = cmt.CMT()

  def collect_packages(self):
    gp = ghostPackage.ghostPackage(self.cmt)
    gp.allInterfacesCreate()

    self.packages = gp.allInterfacesCollectVersions()

    gp.allInterfacesRemove()

  def retrieve_package_home(self,package):
    cmtdir = self.lcgcmt_dir+os.sep+'LCG_Interfaces'+os.sep+package+os.sep+'cmt'
    if os.path.isdir(cmtdir):
      os.chdir(cmtdir)
      self.cmt.init_macros()
      macro_name = package + '_home'
      if self.cmt.macros.has_key(macro_name):
        return self.cfg.normalize_path(self.cmt.macros[macro_name])
      else:
        self.msg.warning('macro %s does not exist' %  macro_name)
        return ''
    else:
      self.msg.warning('directory %s does not exist' % cmtdir)
      return ''

  def tarball_exists(self,tarball_name):
    return os.path.isfile(self.cfg.lcg_distribution_dir+os.sep+tarball_name)

  def enter_results(self,pkg,res,str):
    if self.cfg.isProject(pkg) : self.project_results[pkg] = (res,str)
    else                        : self.package_results[pkg] = (res,str)

  def make_tarball(self,package,srctar=False):
    # This has to be at the very start because it also picks up some
    # more cmt macros (LCG_releases, LCG_external)
    if package == 'LCGCMT':
        pkg_home = self.cfg.lcg_release_dir + os.sep + 'LCGCMT' + os.sep + 'LCGCMT_' + self.cmt.macro_value('LCG_config_version')
        pkg_natv = self.cmt.macro_value('LCG_config_version')
    else:
        pkg_home = self.retrieve_package_home(package)
        pkg_natv = self.packages[package][1]

    tag = ''
    if srctar : tag = 'src'
    else:
      if self.cfg.isProject(package) : tag = self.cmtconfig
      else                           : tag = self.lcgsystem

    if package == 'LCGCMT': tarball_name = 'LCGCMT_' + self.cmt.macro_value('LCG_config_version') + '.tar.gz'
    else: tarball_name = self.cfg.build_pkg_tarball_name(package,pkg_natv,tag)
    
    if self.tarball_exists(tarball_name) and not self.force :
      if self.verbose : self.msg.info('tarball %s already exists' % tarball_name)
      self.enter_results(package,True,'tarball exists')
      return

    if srctar : pkg_home = string.split(pkg_home, pkg_natv)[0]+pkg_natv+os.sep+'src'
    if pkg_home :

      if os.path.isdir(pkg_home) and not pkg_home.startswith('/usr'):
        bindir = ''
        incdir = ''
        cmddir = ''
        if self.cfg.isProject(package) :
          bindir = string.split(pkg_home,self.cfg.lcg_release_dir)[1][1:]
          incdir = os.path.join(os.path.split(bindir)[0],'include')
          cmddir = self.cfg.lcg_release_dir
        else                        :
          bindir = string.split(pkg_home,self.cfg.lcg_external_dir)[1][1:]
          cmddir = self.cfg.lcg_external_dir

        os.chdir(cmddir)
        if os.path.isdir(bindir) :
          if incdir and os.path.isdir(incdir) : bindir += ' ' + incdir
          cmd = 'tar cvfzh %s%s%s %s' % (self.cfg.lcg_distNew_dir ,os.sep, tarball_name, bindir)
          if self.dry or self.verbose: self.msg.info('In %s executing: %s' % (os.path.realpath(os.curdir), cmd))
          if not self.dry : os.system(cmd)
          
          os.chdir(self.cfg.lcg_distribution_dir)
          if not os.path.isfile(tarball_name):
            cmd = 'ln -s %s%s%s%s%s %s' % (os.pardir, os.sep, self.cfg.lcg_distNew_dirname, os.sep, tarball_name, tarball_name)
            if self.dry or self.verbose: self.msg.info('In %s executing: %s' % (os.path.realpath(os.curdir), cmd))
            if not self.dry : os.system(cmd)
          else:
            self.msg.warning('Symlink for %s already exists' %  tarball_name)
          
          self.enter_results(package,True,'tarball created')

        else:
          self.msg.warning('platform directory %s does not exist' % bindir)
          self.enter_results(package,False,'no installation')
      else:
        self.msg.warning('directory %s does not exist' % pkg_home)
        self.enter_results(package,False,'no installation')
    else:
      self.msg.warning('Could not find %s in interface package' % pkg_home)
      self.enter_results(package,False,'interface error')

  def print_results(self):

    mxlen = 0
    for x in xrange(len(self.packages.keys())) : mxlen = max(len(self.packages.keys()[x]), mxlen)

    if self.project_results:
      print 'SUMMARY:'
      print
      print 'LCG/AA projects'
      print
      pkgkeys = self.project_results.keys()
      pkgkeys.sort()
      for x in pkgkeys :
         res = 'OK  '
         if not self.project_results[x][0] : res = 'FAIL'
         print '%s\t%s\t%s' % (x.ljust(mxlen), res, self.project_results[x][1])

    if self.package_results:
      print
      print 'External software'
      print
      pkgkeys = self.package_results.keys()
      pkgkeys.sort()
      for x in pkgkeys :
         res = 'OK  '
         if not self.package_results[x][0] : res = 'FAIL'
         print '%s\t%s\t%s' % (x.ljust(mxlen), res, self.package_results[x][1])

    print
    print
    

  def run(self) :

    self.collect_packages()

    pkg_list = self.packages.keys()

    srctar = False
    if self.cmtconfig == 'src' and not self.sel_packages :
      pkg_list = self.cfg.lcg_projects
      srctar = True
    elif self.sel_packages : pkg_list = self.sel_packages

    #pkg_list = filter( lambda x: not self.cfg.isProject(x), pkg_list )

    map(lambda x: self.make_tarball(x,srctar), pkg_list)


    self.print_results()



if __name__ == '__main__':


  parser = OptionParser()

  parser.add_option('-a', '--all',       action='store_true',  dest='all',       help='create tarballs for all tarball platforms' )
  parser.add_option('-c', '--cmtconfig', action='store',       dest='cmtconfig', help='set the platform tag (otherwise use $CMTCONFIG)' )
  parser.add_option('-p', '--package',   action='append',      dest='pkglist',   help='add a package to build (always one pkg per option)' )
  parser.add_option('-l', '--lcgcmt',    action='store',       dest='lcgcmt',    help='the source directory of LCGCMT' )
  parser.add_option('-v', '--verbose',   action='store_true',  dest='verbose',   help='print more info' )
  parser.add_option('-q', '--quiet',     action='store_false', dest='verbose',   help='print no info' )
  parser.add_option('-f', '--force',     action='store_true',  dest='force',     help='force the building of the tar balls' )
  parser.add_option('-d', '--dry',       action='store_true',  dest='dry',       help='dry run, no commands will be executed' )

  (opts,args) = parser.parse_args()

  if args : parser.error('The script does not take arguments')

  if opts.all :
    p = config.config().tarball_platform_tags
    p.append('src')
    for x in p :
      os.environ['CMTCONFIG'] = x
      mt = make_tarballs(opts.lcgcmt, opts.cmtconfig, opts.pkglist, opts.verbose, opts.force, opts.dry)
      mt.run()
  else:
    mt = make_tarballs(opts.lcgcmt, opts.cmtconfig, opts.pkglist, opts.verbose, opts.force, opts.dry)
    mt.run()
