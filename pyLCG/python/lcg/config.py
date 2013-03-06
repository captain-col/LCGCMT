
import lcg.msg
import sys, os, platform

class config :

  def __init__(self) :

    self.msg = lcg.msg.msg('LCG Configuration')

    # check operating system
    # variables in this section
    self.isWin32 = 0
    self.isMacOS = 0
    self.isLinux = 0

    # checks
    if   sys.platform in ['darwin',]         : self.isMacOS = 1
    elif sys.platform in ['linux','linux2',] : self.isLinux = 1
    elif sys.platform in ['win32',]          : self.isWin32 = 1

    # set lib path name
    self.libpathname = ''
    if self.isMacOS   : self.libpathname = 'DYLD_LIBRARY_PATH'
    elif self.isLinux : self.libpathname = 'LD_LIBRARY_PATH'
    elif self.isWin32 : self.libpathname = 'PATH'

    # check processor type
    self.processor = ''
    self.architecture = ''

    # checks
    self.processor = platform.processor()
    self.architecture = platform.architecture()

    # check architecture
    self.is32bit = 0
    self.is64bit = 0

    if platform.architecture()[0] == '32bit' : self.is32bit = 1
    if platform.architecture()[0] == '64bit' : self.is64bit = 1


    # check processor endianess
    # variables in this section
    self.isBigEndian    = 0
    self.isLittleEndian = 0

    # checks
    if   sys.byteorder == 'big'    : self.isBigEndian = 1
    elif sys.byteorder == 'little' : self.isLittleEndian = 1

    # check operating system version
    # variables in this section
    self.osMaxRelease = 0
    self.osMajRelease = 0
    self.osMinRelease = 0
    self.osReleaseStr = ''

    # checks
    if self.isMacOS :
      verList = map(lambda x: int(x), platform.release().split('.'))
      if len(verList) > 2:

        self.osMaxRelease = 10
        self.osMajRelease = verList[0]-4
        self.osMinRelease = verList[1]

        if self.osMaxRelease == 10:
          if   self.osMajRelease == 3: self.osReleaseStr = 'Panther'
          elif self.osMajRelease == 4: self.osReleaseStr = 'Tiger'
          elif self.osMajRelease == 5: self.osReleaseStr = 'Leopard'
          elif self.osMajRelease == 6: self.osReleaseStr = 'Snow Leopard'
          else : self.msg.error('Second number of os release no %s unknown' % verList)
        else : self.msg.error('First number of os release no %s unknown' % verList)
      else : self.msg.error('Trouble reading os relase, expected a list of min len 3, got' % verList)

    elif self.isLinux :

      if os.path.isfile('/etc/issue') :
        issue = open('/etc/issue','r')
        firstl = issue.readline().split()
        if ' '.join(firstl[:5]) == 'Scientific Linux CERN SLC release' :
          self.osReleaseStr = 'slc'+firstl[5].split('.')[0]
          self.osMaxRelease = firstl[5].split('.')[0]
          self.osMajRelease = firstl[5].split('.')[1]
        issue.close()

    elif self.isWin32 :

      pass

    # check afs availability
    # variables in this section
    self.hasAFS = 0
    self.p_afs = ''

    if 1 : # check afs availability

      if self.isWin32 :

        if os.environ().has_key('AFS') :

          self.p_afs = os.environ()['AFS']
          self.msg.info('Found environment variable AFS, setting self.p_afs to %s' % self.p_afs)

        else :

          self.p_afs = 'E:'
          self.msg.warning('No environment variable AFS found, setting self.p_afs to %s' % self.p_afs)

    # checks
