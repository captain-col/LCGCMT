import optparse,sys,re,os,time,platform,socket
import lcg.aa.config

class processSh :

  def __init__(self, options):
    self.argv0  = sys.argv[0]
    self.varpat = re.compile('\${[A-Za-z_]+}')
    self.osenv  = os.environ
    self.rem    = '# ' + '*'*78 + '\n'

    self.incVars = options.varincludes
    self.excVars = options.varexcludes
    self.incInfo = options.infincludes
    self.excInfo = options.infexcludes

    self.pinfo = options.pinfo
    self.pvars = options.pvars
    self.pscrpt = options.pscrpt
    self.pexpnd = options.pexpnd

    self.pall = True
    if self.pinfo or self.pvars or self.pscrpt or self.pexpnd : self.pall = False

    self.infolst = {'Hostname': socket.gethostname(),
                    'IP'      : socket.gethostbyname(socket.gethostname()),
                    'Time'    : time.ctime(),
                    'Uname'   : ' '.join(platform.uname()),
                    'PATH'    : os.environ['PATH']
                   }

    for i in self.incInfo :
      try:
        self.infolst[i] = os.environ[i]
      except KeyError,e :
        print '%s: WARNING: variable %s not found' % (self.argv0, i)

    self.varmax  = 0
    self.filehdl = None
    self.filenam = ''
    self.filelns = []
    self.filelno = 0
    self.filevrs = {}

  def reset(self):
    self.varmax  = 0
    self.filehdl = None
    self.filenam = ''
    self.filelns = []
    self.filelno = 0
    self.filevrs = {}

    map(self.fillVars, self.incVars)

  def fillVars(self, v):
    while v[0]  in ('$',' ','{') : v = v[1:]
    while v[-1] in (' ', '}') : v = v[:-1]
    if not self.filevrs.has_key(v):
      if self.osenv.has_key(v): self.filevrs[v] = self.osenv[v]
      else: print '%s: WARNING: Environment variable %s found in script %s, line %s, not part of environment' % (self.argv0, v, self.filenam, self.filelno) 

  def extractVars(self, line):
    self.filelno += 1
    exvars = self.varpat.findall(line)
    map(self.fillVars, exvars)

  def vmax(self, x):
    self.varmax = max(self.varmax,x)

  def printInfo(self):
    inf = self.rem
    kmax = 0

    infKeys = self.infolst.keys()
    map(infKeys.remove, self.excInfo)

    for k in infKeys : kmax = max(kmax, len(k))
    for k in infKeys : inf += '%s : %s\n' % (k.ljust(kmax), self.infolst[k])

    return inf[:-1]

  def printVars(self):
    vs = self.rem
    map(self.vmax, map(len, self.filevrs.keys()))
    for v in self.filevrs:
      vs += '%s: %s\n' % (v.ljust(self.varmax+1), self.filevrs[v])
    return vs[:-1]

  def printFile(self, expand=False):
    pf = self.rem
    for l in self.filelns:
      if expand: 
        lvars = self.varpat.findall(l)
        for v in lvars :
          pv = v[2:-1]
          if pv not in self.excVars : l = l.replace(v,self.filevrs[pv])
      pf += l
    return pf[:-1]

  def processFile(self, filename):
    self.reset()
    self.filenam = filename
    try:
      self.filehdl = open(self.filenam,'r')
    except Exception, e:
      print '%s: ERROR: opening file %s: %s' % (self.argv0, self.filenam, e)

    map(self.filelns.append, self.filehdl.readlines())
    self.filehdl.close()

    map(self.extractVars, self.filelns)

    if self.pall or self.pinfo  : print self.printInfo()
    if self.pall or self.pvars  : print self.printVars()
    if self.pall or self.pscrpt : print self.printFile()
    if self.pall or self.pexpnd : print self.printFile(expand=True)

if __name__ == '__main__':

  op = optparse.OptionParser()

  op.add_option('-V', '--include_variable', action='append', type='string', dest='varincludes', default=[])
  op.add_option('-v', '--exclude_variable', action='append', type='string', dest='varexcludes', default=[])
  op.add_option('-I', '--include_info',     action='append', type='string', dest='infincludes', default=[])
  op.add_option('-i', '--exclude_info',     action='append', type='string', dest='infexcludes', default=[])

  op.add_option('-a', '--print-info'           , action='store_true', dest='pinfo',  default='False')
  op.add_option('-b', '--print-variables'      , action='store_true', dest='pvars',  default='False')
  op.add_option('-c', '--print-script'         , action='store_true', dest='pscrpt', default='False')
  op.add_option('-d', '--print-script-expanded', action='store_true', dest='pexpnd', default='False')
  
  (options,args) = op.parse_args()
  
  p = processSh(options)
  map( p.processFile, args )
