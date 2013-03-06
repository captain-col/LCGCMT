
import lcg.config, os.path, re, cmt, string

import sys

from subprocess import Popen, PIPE

class config(lcg.config.config) :

  def __init__(self):
    
    self.msg = lcg.msg.msg('LCG AA Configuration')

    lcg.config.config.__init__(self)

    self.cmt = cmt.CMT()

    # the names of the LCG/AA projects
    self.lcg_projects = ['LCGCMT','RELAX','CORAL', 'COOL','ROOT']
    self.not_lcgaa_packages = ['GAUDI']

    # important directories
    self.lcg_lcgcmtroot_dir   = os.sep.join(os.path.dirname(lcg.aa.config.__file__).split(os.sep)[:-4])+os.sep
    self.lcg_distNew_dirname  = 'distNew4'
    self.lcg_external_dir     = ''
    self.lcg_release_dir      = ''
    self.lcg_distribution_dir = ''
    self.lcg_distNew_dir      = ''

    # retrieve macros from LCG_Settings
    sav_dir = os.path.realpath(os.curdir)
    os.chdir(self.lcg_lcgcmtroot_dir + 'LCG_Settings' + os.sep + 'cmt')
    self.cmt.init_macros()
    if self.lcg_external_dir == '' and self.cmt.macros.has_key('LCG_external') :
      self.lcg_external_dir = self.normalize_path(self.cmt.macros['LCG_external'])
    if self.lcg_release_dir == '' and self.cmt.macros.has_key('LCG_releases') :
      self.lcg_release_dir = self.normalize_path(self.cmt.macros['LCG_releases'])
    os.chdir(sav_dir)

    self.lcg_distribution_dir = self.lcg_external_dir + os.sep + 'distribution'
    self.lcg_distNew_dir = self.lcg_external_dir + os.sep + self.lcg_distNew_dirname

    # actual lcg tags
    self.all_platform_tags = [
      'i686-slc5-gcc43-opt',
      'i686-slc5-gcc43-dbg',
      'x86_64-slc5-icc11-opt',
      'x86_64-slc5-icc11-dbg',
      'x86_64-slc5-gcc43-opt',
      'x86_64-slc5-gcc43-dbg',
      'x86_64-slc5-gcc46-opt',
      'x86_64-slc5-gcc46-dbg',
      'x86_64-slc6-gcc46-opt',
      'x86_64-slc6-gcc46-dbg',
      'x86_64-mac106-gcc42-opt',
      'x86_64-mac106-gcc42-dbg'
      ]
    self.release_platform_tags = [
      'i686-slc5-gcc43-opt',
      'i686-slc5-gcc43-dbg',
      'x86_64-slc5-icc11-opt',
      'x86_64-slc5-icc11-dbg',
      'x86_64-slc5-gcc43-opt',
      'x86_64-slc5-gcc43-dbg',
      'x86_64-slc5-gcc46-opt',
      'x86_64-slc5-gcc46-dbg',
      'x86_64-slc6-gcc46-opt',
      'x86_64-slc6-gcc46-dbg',
      'x86_64-mac106-gcc42-opt',
      'x86_64-mac106-gcc42-dbg'
      ]

    self.tarball_platform_tags = [
      'i686-slc5-gcc43-opt',
      'i686-slc5-gcc43-dbg',
      'x86_64-slc5-gcc43-opt',
      'x86_64-slc5-gcc43-dbg',
      'x86_64-slc6-gcc46-opt',
      'x86_64-slc6-gcc46-dbg',
      'x86_64-mac106-gcc42-opt'
     ]
    
    self.old_platform_tags = [
      'osx104_ia32_gcc401',
      'osx104_ia32_gcc401_dbg',
      'osx104_ppc_gcc401',
      'osx104_ppc_gcc401_dbg',
      'slc3_ia32_gcc323',
      'slc3_ia32_gcc323_dbg'
      'slc4_amd64_gcc41',
      'slc4_amd64_gcc41_dbg', 
      'slc4_ia32_gcc41',
      'slc4_ia32_gcc41_dbg',
      ]

    # checks
    for t in self.release_platform_tags :
      if t not in self.all_platform_tags :
        msg.error('Consistency check: release tag %s not in container of all tags' % t)

    for t in self.tarball_platform_tags :
      if t not in self.release_platform_tags :
        msg.error('Consistency check: tarball tag %s not in container of release tags' % t)

    for t in self.old_platform_tags :
      if t in self.all_platform_tags :
        msg.error('Consistency check: old platform tag %s is part of container of all tags' % t)


    # compiler settings
    # variables
    self.compiler = ''
    self.compilerMax = 0
    self.compilerMaj = 0
    self.compilerMin = 0

    # checks
    if self.isWin32 :

      pass

    else :

      # try gcc
      p = Popen('gcc --version', shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, close_fds=True) 
      i,o,e = p.stdin, p.stdout, p.stderr

      err = e.readlines()
      if len(err) : self.msg.error(err)
      else :
        self.compiler = 'gcc'
        patt = re.compile('.*\s(\d+)\.(\d+)(\.(\d+))*\s.*')
        mobj = patt.match(o.readlines()[0])
        self.compilerMax = int(mobj.group(1))
        self.compilerMaj = int(mobj.group(2))
        self.compilerMin = int(mobj.group(4))

    # lcg tag
    # variables
    self.lcg_tag = ''
    self.lcg_tag_dbg = ''

    # setup
    if self.isLinux :

      if self.osReleaseStr in ('slc3', 'slc4', 'slc5', 'slc6') : self.lcg_tag += '%s' % self.osReleaseStr
      else : self.msg.error('Trying to setup tag info, unknown string for OS %s' % self.osReleaseStr)

      if self.is32bit : self.lcg_tag += '_ia32'
      elif self.is64bit : self.lcg_tag += '_amd64'

      if self.compiler == 'gcc' :
        if self.compilerMax == 3 and self.compilerMaj == 2 and self.compilerMin == 3 :
          self.lcg_tag += '_gcc%s%s%s' % (self.compilerMax, self.compilerMaj, self.compilerMin)
        else                       : self.lcg_tag += '_gcc%s%s' % ( self.compilerMax, self.compilerMaj)

      else : self.msg.warning('Nothing known about compiler %s' % self.compiler)

    elif self.isMacOS :

      self.lcg_tag += 'osx%s%s' % ( self.osMaxRelease, self.osMajRelease )

      if self.processor == 'powerpc' : self.lcg_tag += '_ppc'
      elif self.processor == 'i386'  : self.lcg_tag += '_ia32'
      else : self.msg.error('Processor type %s unknown' % self.processor )

      if self.compiler == 'gcc' :
        if self.compilerMax == 4 and self.compilerMaj == 0 and self.compilerMin == 1 : self.lcg_tag += '_gcc401'
        else : self.lcg_tag += '_gcc%s%s' % (self.compilerMax, self.compilerMaj)

    elif self.isWin32 :

      pass

    
    self.lcg_tag_dbg = '%s_dbg' % self.lcg_tag


    # licenses
    self.licenseURLs = {
                        '4SUITE'  : 'http://4suite.org/COPYRIGHT.doc',
                        'APACHE'  : 'http://www.apache.org/licenses/',
                        'BOOST'   : 'http://boost.org/more/license_info.html',
                        'BLAS'    : 'http://www.netlib.org/blas/faq.html#2',
                        'BSD'     : 'http://www.opensource.org/licenses/bsd-license.php',
                        'BZ2LIB'  : 'http://service-spi.web.cern.ch/service-spi/external/bz2lib/_SPI/LICENSE',
                        'CGAL'    : 'http://www.cgal.org/license.html',
                        'CMT'     : 'http://www.cecill.info/licences/Licence_CeCILL_V2-en.html',
                        'CMAKE'   : 'http://www.cmake.org/HTML/Copyright.html',
                        'CNRI'    : 'http://www.opensource.org/licenses/pythonpl.php',
                        'CXORACLE': 'http://www.python.net/crew/atuining/cx_Oracle/LICENSE.txt',
                        'CYGWIN'  : 'http://cygwin.com/licensing.html',
                        'GCCXML'  : 'http://www.gccxml.org/HTML/Copyright.html',
                        'GPL'     : 'http://www.gnu.org/copyleft/gpl.html',
                        'LAPACK'  : 'http://www.netlib.org/lapack/COPYING',
                        'LCGAA'   : '',
                        'LGPL'    : 'http://www.gnu.org/licenses/lgpl.html',
                        'LIBPNG'  : 'http://www.libpng.org/pub/png/src/libpng-LICENSE.txt',
                        'LLVM'    : 'http://llvm.org/releases/2.5/LICENSE.TXT',
                        'MATPLOTLIB': 'http://matplotlib.sourceforge.net/users/license.html',
                        'MIT'     : 'http://www.opensource.org/licenses/mit-license.php',
                        'MYSQL'   : 'http://www.mysql.com/company/legal/licensing/opensource-license.html',
                        'ORACLE'  : 'http://www.oracle.com/corporate/license/agreements.html',
                        'PCRE'    : 'http://www.pcre.org/license.txt',
                        'PYTHON'  : 'http://www.opensource.org/licenses/PythonSoftFoundation.php',
                        'SCONS'   : 'http://service-spi.web.cern.ch/service-spi/external/scons/_SPI/LICENSE.txt',
                        'SQLITE'  : 'http://www.sqlite.org/copyright.html',
                        'SUBVERSION': 'http://subversion.tigris.org/license-1.html',
                        'X11'     : 'http://www.xfree86.org/3.3.6/COPYRIGHT2.html',
                        'UNKNOWN' : '',
                        }
    
    self.licenses = self.licenseURLs.keys()

  def normalize_path(self,path):
    return path.replace('\\',os.sep)

  def build_pkg_tarball_name(self,pkg,ver,plat):
    if self.isProject(pkg) and string.upper(pkg) != 'ROOT' :
      return '%s__LCG_%s.tar.gz' % (ver, plat)
    else :
      return '%s_%s__LCG_%s.tar.gz' % ( pkg,ver,plat )

  def isProject(self,pkg):
    if string.upper(pkg) in self.lcg_projects : return 1
    return 0

