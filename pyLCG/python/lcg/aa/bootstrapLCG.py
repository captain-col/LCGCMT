import sys,os,shutil,urllib,tarfile,optparse
from encodings import ascii

class bootstrapper:

  def __init__(self,source,dest,platform,get,temp,confstr,gettypes):
    self.source = source
    self.destination = dest
    self.tempDir = temp
    self.platform = platform
    self.get = get
    self.gettypes = gettypes
    self.lcgConfig = confstr
    self.processedFiles = []

    self.pkg_versions = ['python','cmt']

    self.default_distribution_http = 'http://service-spi.web.cern.ch/service-spi/external/distribution/'
    self.default_distribution_cp = '/afs/cern.ch/sw/lcg/external/distribution/'

    self.lcgHome = os.path.join(self.destination,'sw','lcg')
    self.lcgReleases = os.path.join(self.lcgHome,'app','releases')
    self.lcgExternal = os.path.join(self.lcgHome,'external')

    if os.environ.has_key('CMTSITE') and os.environ['CMTSITE'] == 'LOCAL' : self.lcgReleases = self.lcgExternal

    for x in [self.lcgReleases,self.lcgExternal,self.tempDir] :
      if not os.path.isdir(x) : os.makedirs(x)

  def get_file_http(self,fname,mimetype):
    surl = ''
    tmpfile = self.tempDir+os.sep+fname
    if self.source :
      r = urllib.urlopen(self.source+os.sep+fname,tmpfile)
      if r.type != mimetype :
        print 'WARNING r.type', r.type
        r = urllib.urlopen(self.default_distribution_http+os.sep+fname,tmpfile)
        if r.type != mimetype :
          print 'WARNING r.type', r.type

  def get_file_cp(self,fname,mimetype):
    sdir = ''
    if self.source and os.path.isdir(self.source) : sdir = self.source
    elif os.path.isdir(self.default_distribution_cp) : sdir = self.default_distribution_cp
    if sdir : shutil.copy(sdir+os.sep+fname, self.tempDir)
    else : pass # WARNING

  def call_get(self,filename,mimetype):
    for x in self.gettypes:
      fname = 'get_file_'+x
      if self.__class__.__dict__.has_key(fname) :
        self.__class__.__dict__[fname](self,filename,mimetype)
      if mimetype == 'application/x-gzip' and tarfile.is_tarfile(self.tempDir+os.sep+filename) : break

  def extract_lcg_versions(self):
    requirementsFile = os.path.join(self.lcgReleases,'LCGCMT','LCGCMT_'+self.lcgConfig,'LCG_Configuration','cmt','requirements')
    for l in open(requirementsFile,'r').readlines():
      li = l.split()
      if len(li) > 2 :
        pkgname = li[1].split('_')[0]
        pkgnamel = pkgname.lower()
        if pkgnamel in self.pkg_versions and li[1] == pkgname+'_config_version' :
          self.__dict__[pkgnamel+'Version'] = li[2].strip('"')

  def process_pkg(self,pkg,vers,destination):
    destdir = ''
    if pkg == 'LCGCMT' : destdir = os.path.join(destination,pkg,'LCGCMT_'+vers)
    elif pkg == 'cmt'  : destdir = os.path.join(destination,'CMT',vers)
    else               : destdir = os.path.join(destination,pkg,vers,self.platform)
    if not os.path.isdir(destdir) :
      fextra = ''
      if pkg not in ('LCGCMT', 'cmt') : fextra = '__LCG_'+self.platform
      filename = '%s_%s%s.tar.gz' % (pkg,vers,fextra)
      self.call_get(filename,'application/x-gzip')
      tf = tarfile.TarFile.gzopen(name=self.tempDir+os.sep+filename)
      tf.extractall(path=destination)
      self.processedFiles.append(filename)

  def post_process(self) :
    # Finalizing CMT setup
    cmtdir = os.path.join(self.lcgExternal,'CMT',self.cmtVersion,'mgr')
    if os.path.isdir(cmtdir) :
      os.chdir(cmtdir)
      if sys.platform.find('win32') != -1 : os.system('INSTALL.bat')
      else                                :
        os.system('sh INSTALL')
        os.chdir(os.path.join(self.lcgReleases,'LCGCMT','LCGCMT_'+self.lcgConfig,'LCG_Release','cmt'))
        os.system('%s/cmt -tag_add=ATLAS show actions'%os.path.join(self.lcgExternal,'CMT',self.cmtVersion,'Darwin-i386'))

  def run(self):
    self.process_pkg('LCGCMT', self.lcgConfig,     self.lcgReleases)
    self.extract_lcg_versions()
    self.process_pkg('cmt',    self.cmtVersion,    self.lcgExternal)
    self.process_pkg('Python', self.pythonVersion, self.lcgExternal)
    self.post_process()

  def teardown(self):
    for f in self.processedFiles:
      ff = os.path.join(self.tempDir,f)
      if os.path.isfile(ff) : os.remove(ff)
    if not os.listdir(self.tempDir) : os.rmdir(self.tempDir)

def run_bootstrap_lcg() :
  # ways on retrieving the files, each type should be implemented in a function bootstrapper.get_file_<type>(self, fname)
  gettypes=['cp','http']

  op = optparse.OptionParser()

  op.add_option('-s', '--src',         action='store',      dest='src',         help='source location')
  op.add_option('-d', '--dest',        action='store',      dest='dest',        help='destination directory')
  op.add_option('-t', '--temp',        action='store',      dest='temp',        help='temporary directory')
  op.add_option('-p', '--plat',        action='store',      dest='plat',        help='platform string')
  op.add_option('-g', '--get',         action='store',      dest='get',         help='retrieval method %s' %gettypes)
  op.add_option('-q', '--quiet',       action='store_true', dest='quiet',       help='no messages except error')
  op.add_option('-v', '--verbose',     action='store_true', dest='verbose',     help='verbose output')
  op.add_option('-c', '--clean',       action='store_true', dest='cleanup',     help='cleanup afterwards')

  (args,opts) = op.parse_args()

  if len(opts) != 1    : op.error('One option, being the LCG configuration number, is required (e.g. "54c")')

  if not args.plat and os.environ.has_key('CMTCONFIG') : args.plat = os.environ['CMTCONFIG']
  if not args.plat : op.error('Platform configuration string requested, eiher set environment variable "CMTCONFIG" or option -p/--platform')

  if not args.dest : args.dest = os.path.realpath(os.curdir)
  if not args.temp : args.temp = os.path.realpath(os.curdir)+os.sep+'tmp'

  bs = bootstrapper(source=args.src,dest=args.dest,temp=args.temp,platform=args.plat,get=args.get,confstr=opts[0],gettypes=gettypes)
  bs.run()
  if args.cleanup : bs.teardown()
  
if __name__ == '__main__':
  run_bootstrap_lcg()
