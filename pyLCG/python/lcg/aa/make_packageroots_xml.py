from xml.dom.minidom import Document
from optparse import OptionParser
from lcg import msg
from lcg.aa.spi import ghostPackage
import os,sys,cmt

class make_packageroots_xml(object):
  """
  This class creates a xml file with entries per package, the attributes
  of the elements are the package name and the root directory of the package
  in the LCG/AA environment of a certain LCGCMT version. This could be used
  by other clients to receive the exact location of the LCG/AA packages and
  incorporate it into their build environment. 
  """

  def __init__(self,loc,cfg,verb,dry):
    self.location = loc
    self.cmtconfig = cfg
    self.verb = verb
    self.dry = dry
    self.msg = msg.msg(os.path.basename(sys.argv[0]))
    self.indent = 2

    if not self.location : self.location = os.path.realpath(os.curdir)
    if not self.cmtconfig :
      if os.environ.has_key('CMTCONFIG') : self.cmtconfig = os.environ.get('CMTCONFIG')
      else :
        self.msg.error('environment $CMTCONFIG not found and no -c/--cmtconfig passed, exiting')
        sys.exit(1)

    self.filename = 'packagedict-%s.xml'%self.cmtconfig

  def create(self):
    gp = ghostPackage.ghostPackage(cmt.CMT())
    gp.allInterfacesCreate()
    pkgdict = gp.allInterfacesCollectVersions(self.cmtconfig)
    gp.allInterfacesRemove()

    doc = Document()

    pkgs = doc.createElement("packages")
    doc.appendChild(pkgs)

    for p in pkgdict :
    
      # Create the main <card> element
      pkg = doc.createElement("pkg")
      pkg.setAttribute("name", p)
      pkg.setAttribute('path', pkgdict[p][2])
      pkgs.appendChild(pkg)

    # Print our newly created XML
    ff = os.path.join(self.location,self.filename)
    f = open(ff,'w')
    f.write(doc.toprettyxml(indent=" "*self.indent))
    f.close()
    self.msg.info('Wrote file '+ff) 

if __name__ == '__main__' :

  parser = OptionParser()

  parser.add_option('-l', '--location',  action='store',       dest='location',  help='the location of the output file (default local dir)' )
  parser.add_option('-c', '--cmtconfig', action='store',       dest='cmtconfig', help='set the platform tag (otherwise use $CMTCONFIG)' )
  parser.add_option('-v', '--verbose',   action='store_true',  dest='verbose',   help='print more info' )
  parser.add_option('-d', '--dry',       action='store_true',  dest='dry',       help='dry run, no commands will be executed' )

  (opts,args) = parser.parse_args()

  if args : parser.error('The script does not take arguments')

  mp = make_packageroots_xml(opts.location,opts.cmtconfig,opts.verbose,opts.dry)
  mp.create()
