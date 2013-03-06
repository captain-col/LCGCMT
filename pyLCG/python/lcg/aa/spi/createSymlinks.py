import sys,cmt,os
from optparse import OptionParser
from lcg import msg
from lcg.aa import config
from lcg.aa.spi import ghostPackage

class create_symlinks :

  def __init__(self,fr,to,msgLvl,dry,pkg):
    self.fr = fr
    self.to = to
    self.cmt = cmt.CMT()
    self.dry = dry
    self.pkg = pkg
    self.cfg = config.config()
    self.msg = msg.msg(os.path.basename(sys.argv[0]), msgLevel=msgLvl)

  def afs_actions(self,dir):
    cmd = 'afs_admin vos_release `pwd`'
    self.msg.debug('Executing %s' % cmd)
    if self.dry : self.msg.info('Dry run: in %s executing %s' % (dir,cmd))
    else:
      self.msg.debug('in %s executing %s' % (dir,cmd))
      os.system(cmd)

  def run(self):

    self.msg.debug('Creating ghost package for all interfaces')
    gp = ghostPackage.ghostPackage(self.cmt)
    gp.allInterfacesCreate()
    self.msg.debug('Collecting all version numbers for the interfaces, using tag name ', self.fr)
    packages = gp.allInterfacesCollectVersions(self.fr)
    self.msg.debug('Versions for interfaces collected: ', packages)
    gp.allInterfacesRemove()
    self.msg.debug('Removing ghost package for all interfaces')

    pkgKeys = []
    if self.pkg :
      pkgKeys = [self.pkg]
    else:
      pkgKeys = packages.keys()
      pkgKeys = filter(lambda x: not self.cfg.isProject(x), pkgKeys)
    self.msg.debug('List of all packages: %s' % pkgKeys)

    for pkg in pkgKeys :
      self.msg.setPreAmble('[%s] ' % pkg)
      pkgdir = packages[pkg][2].replace('\\', os.sep)
      inafs = False
      if pkgdir.find('/cern.ch/') != -1 :
        pkgdir = pkgdir.replace('/cern.ch/','/.cern.ch/')
        inafs = True
      elif pkgdir.find('/.cern.ch/') != -1 : inafs = True
      if os.path.split(pkgdir)[-1] == self.fr :
        pkgdir = os.sep.join(os.path.split(pkgdir)[:-1])
      else:
        self.msg.error('directory %s does not contain "from" tagname as last entry, skipping' % pkgdir)
      self.msg.debug('Using external root directory' + pkgdir)
      if os.path.isdir(pkgdir):
        os.chdir(pkgdir)
        if not os.path.islink(self.to) :
          if not os.path.isdir(self.to) :
            cmd = 'ln -s %s %s' % (self.fr, self.to)
            if not self.dry :
              os.system(cmd)
              if os.path.islink(self.to) :
                if inafs : self.afs_actions(pkgdir)
                self.msg.info('Symlink %s->%s created' % (self.fr, self.to))
              else : self.msg.error('creation of symlink %s->%s failed' % (self.fr, self.to))
            else : self.msg.info('Dry run: in %s executing %s' % (pkgdir, cmd))
          else : self.msg.warning('%s is a directory' % self.to)
        else : self.msg.warning('%s symlink in %s exists' % (self.to, pkgdir))
      else : self.msg.warning('directory %s does not exist, skipping package' % pkgdir)

if __name__ == '__main__':

  msgLvls = msg.msgLevelDictionary.keys()

  parser = OptionParser()

  parser.add_option('-f', '--from',    action='store',      dest='fr',     help='the source tag name (required)' )
  parser.add_option('-t', '--to',      action='store',      dest='to',     help='the symlink name to create (required)' )
  parser.add_option('-l', '--msgLvl',  action='store',      dest='msgLvl', help='message level [%s]' % msgLvls )
  parser.add_option('-d', '--dry',     action='store_true', dest='dry',    help='dry run' )
  parser.add_option('-p', '--pkg',     action='store',      dest='pkg',    help='run for a single package')

  (opts,args) = parser.parse_args()

  if args                       : parser.error('The script does not take arguments')
  if not opts.fr                : parser.error('No option -f/--from given, please provide')
  if not opts.to                : parser.error('No option -t/--to given, please provide')
  if opts.msgLvl not in msgLvls : parser.error('Option -l/--msgLvl not in %s' % msgLvls)

  cs = create_symlinks(opts.fr, opts.to, opts.msgLvl, opts.dry, opts.pkg)
  cs.run()
