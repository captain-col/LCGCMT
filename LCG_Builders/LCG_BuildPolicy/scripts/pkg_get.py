import cmt,sys,os,shutil
import time, subprocess, shlex

class pkg_get :
    def __init__(self):
        # argv0 needed for msgs
        self.argv0 = sys.argv[0]
        # the cmt instance
        self.cmt = cmt.CMT()
        # the fallback directory for tar balls (afs)
        self.LCG_tardir_fallback = ''
        # a list of source files to be copied
        self.source_files = []
        self.LCG_cvsdir = ''
        # needed sets / macros
        macros = ('package', 'LCG_sourcefiles', 'LCG_get','LCG_cvsdir')
        sets   = ('LCG_tardir', 'LCG_tarfilename', 'LCG_builddir', 'LCG_tarurl', 'LCG_package_config_version', 'LCG_CVSROOT', 'LCG_SVNROOT', 'LCG_svnpath', 'LCG_svndir', 'LCG_svntag', 'LCG_svnfolder', 'LCG_CheckoutDir' , 'LCG_cvstag', "LCG_cvsproj")
        # getting macros and sets
        for m in macros:
            try:
                self.__dict__[m] = self.cmt.macros[m]
            except Exception,e: pass
     
        for s in sets:
            try:
                self.__dict__[s] = self.cmt.sets[s]
            except Exception,e: pass
            #print self.argv0, ': WARNING: no set "'+s+'" being defined:', e.__class__, e
        if self.__dict__.has_key('LCG_sourcefiles') :
            self.source_files = map(lambda x: x.strip(), self.LCG_sourcefiles.split(';'))
        elif self.__dict__.has_key('LCG_tarfilename'):
            self.source_files = [self.LCG_tarfilename.strip()]

    def setup(self):
        if os.path.isdir(self.LCG_builddir) : return
        else:
            try:
                os.makedirs(self.LCG_builddir)
            except Exception,e:
                print self.argv0, ': ERROR: problem creating LCG build directory:', e
                sys.exit(1)

    def get_tardir(self):
        if os.path.isdir(self.LCG_tardir) : return self.LCG_tardir
        elif os.path.isdir(self.LCG_tardir_fallback) :
            print self.argv0, ': WARNING: directory set for LCG_tardir ("%s") does not exist, setting it to %s' % (self.LCG_tardir, self.LCG_tardir_fallback)
            return self.LCG_tardir_fallback
        else :
            print self.argv0, ': WARNING: No access to tar directory (cmt macro "LCG_tardir" set to "%s"), try creating' % self.LCG_tardir
            os.makedirs(self.LCG_tardir)
            return self.LCG_tardir
        return ''

    def get_cp_one(self,src,dst):
        try:
            shutil.copy(src,dst)
        except Exception,e:
            print self.argv0, ': ERROR: Copying file %s to %s: %s' % (src, dst, e)
        if not os.path.isfile(src) :
            print self.argv0, ': ERROR: Copying of file %s to %s failed' % (src, dst)
            sys.exit(1)
        else:
            print self.argv0, ': INFO: File %s copied to %s' % ( src, dst )
        return

    def get_cp(self):
        tardir = self.get_tardir()
        dst = self.LCG_builddir
        for f in self.source_files:
            src = os.path.join(tardir,f)
            self.get_cp_one(src,dst)
            continue
        return

    def get_scp(self):
        print self.argv0, ': ERROR: get method "scp" not implemented yet'
        sys.exit(1)

    def get_http(self):
        tardir = self.get_tardir()
        for file in self.source_files:
            target = os.path.join(tardir,file)
            if not os.path.exists(target): 
                import urllib
                url = self.LCG_tarurl + "/" + file
                print self.argv0, ': INFO: Downloading %s to %s' % ( url, target )
                sys.stdout.flush()
                # if http_proxy set, explicitly use it, works around some Mac OS X issues
                pr = os.getenv('http_proxy')
                if pr:
                    #print 'using http_proxy:',pr
                    u = urllib.URLopener({'http':pr})
                    ret = u.retrieve(url,target)
                else:
                    urllib.urlretrieve(url,target)
                pass
            continue
        return

    def get_root(self):
        os.chdir(self.LCG_builddir)

        if not os.path.exists(self.package):
            try : 
                os.makedirs(self.package)
            except Exception, e:
                print self.argv0, ': ERROR: problem creating directory %s in %s: ' % (self.package, self.LCG_builddir), e
                sys.exit(1)
        os.chdir(self.package)
     
        if self.LCG_package_config_version.find("_today") != -1:
            cmd = 'svn -q co http://root.cern.ch/svn/root/trunk -r "{00:00}" %s' %(os.path.join(self.LCG_CheckoutDir, "root"))
            testcmd = 'svn -q co http://root.cern.ch/svn/roottest/trunk -r "{00:00}" %s' %(os.path.join(self.LCG_CheckoutDir, "roottest"))
            if time.localtime()[3] > 8:
                cmd = 'svn -q co http://root.cern.ch/svn/root/trunk  %s' %(os.path.join(self.LCG_CheckoutDir, "root"))
                testcmd = 'svn -q co http://root.cern.ch/svn/roottest/trunk %s' %(os.path.join(self.LCG_CheckoutDir, "roottest"))
        elif self.LCG_package_config_version.find('patches') != -1:
            rootTag = self.LCG_package_config_version[5:].replace('_','-')
            cmd = 'svn -q co http://root.cern.ch/svn/root/branches/%s  %s' % ("v" + rootTag,os.path.join(self.LCG_CheckoutDir, "root"),)
            testcmd = 'svn -q co http://root.cern.ch/svn/roottest/branches/%s  %s' % ("v" + rootTag,os.path.join(self.LCG_CheckoutDir, "roottest"),)
        else:
            rootTag = self.LCG_package_config_version.replace('.','-')
            cmd = 'svn -q co http://root.cern.ch/svn/root/tags/%s %s' % ('v' + rootTag, os.path.join(self.LCG_CheckoutDir, 'root'))
            # there are no test-tags ending with a,b,c..., so fall back to the base release
            isPatchRelease = rootTag[-1].isalpha()
            if isPatchRelease:
                rootTestTag = rootTag[:-1]
            else:
                rootTestTag = rootTag 
            testcmd = 'svn -q co http://root.cern.ch/svn/roottest/tags/%s %s' % ('v' + rootTestTag, os.path.join(self.LCG_CheckoutDir, 'roottest'))

        print self.argv0, ': INFO: %s' % cmd
        print self.argv0, ': INFO: %s' % testcmd
        for i in range(3):
          os.system(cmd)
          os.system(testcmd)



    def get_cvs(self):
        if not self.LCG_cvsdir:
            self.LCG_cvsdir = self.LCG_package_config_version
        os.chdir(self.LCG_builddir)
        destdir = os.path.join(self.package,self.LCG_cvsdir)
        if not os.path.exists(destdir):
            try : 
                os.makedirs(destdir)
            except Exception, e:
                print self.argv0, ': ERROR: problem creating directory %s in %s: ' % (self.package, self.LCG_builddir), e
                sys.exit(1)
        os.chdir(self.package)
        cmd = 'cvs -q -d %s co -N -d %s -r %s %s.release' % ( self.LCG_CVSROOT, self.LCG_cvsdir, self.LCG_package_config_version, self.package.lower())
        print self.argv0, ': INFO: %s' % cmd
        args = shlex.split(cmd)
        Failure = True
        retry = 0
        offset = 5
        threshold = 1800
        while Failure and retry < threshold:
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            text, errors = p.communicate()
            if errors:
                print  errors, "Error on checkout. Retrying in 5 seconds "
                retry += offset
                time.sleep(offset)
            else:
                Failure = False


        #inp,out,err = os.popen3('CVS -d %s co -d %s -r %s %s.release' % ( self.LCG_CVSROOT, self.LCG_package_config_version, self.LCG_package_config_version, self.package.lower()))
        #er2 = err.read()
        #ou2 = out.read()
        #inp.close()
        #err.close()
        #out.close()
        #if er2 :
        #  print self.argv0, ': ERROR: Checking out project %s\n%s' % ( self.package, er2 )
        #print ou2

    
    def get_cvs_generic(self):
        """
            Generic way of checking out cvs repository

            cvs -q -d LCG_CVSROOT co -N -d self.LCG_cvsdir -r LCG_cvstag LCG_cvsproj
            
            LCG_CVSROOT - env
            self.LCG_cvsdir - dir under LCG_builddir/package (that is /build/LCG or /build/nightlies/<slot>/<day>/<proj> (etc)
            LCG_cvstag - tag to check out (env)
            LCG_cvsproj - project to check out
            

        """
        os.chdir(self.LCG_builddir)
        if not os.path.exists(self.package):
            try : 
                os.makedirs(self.package)
            except Exception, e:
                print self.argv0, ': ERROR: problem creating directory %s in %s: ' % (self.package, self.LCG_builddir), e
                sys.exit(1)
        os.chdir(self.package)
        cmd = 'cvs -q -d %s co -N -d %s -r %s %s' % ( self.LCG_CVSROOT, self.LCG_cvsdir, self.LCG_cvstag, self.LCG_cvsproj)
        print self.argv0, ': INFO: %s', cmd
        os.system(cmd)
 
    def cvs_gaudi(self):
        if self.LCG_cvstag == "GAUDI_HEAD": self.LCG_cvstag = "HEAD"
        self.get_cvs_generic()

    def get_svn_generic(self) :
        os.chdir(self.LCG_builddir)
        if not os.path.exists(self.package):
            try : 
                os.makedirs(self.package)
            except Exception, e:
                print self.argv0, ': ERROR: problem creating directory %s in %s: ' % (self.package, self.LCG_builddir), e
                sys.exit(1)
        os.chdir(self.package)
        try:
            cmd = 'svn -q --non-interactive checkout %s/%s/%s %s' % ( self.LCG_SVNROOT, self.LCG_svnpath, self.LCG_svntag, self.LCG_svnfolder)
        except AttributeError:
            cmd = 'svn -q --non-interactive checkout %s/%s/%s' % ( self.LCG_SVNROOT, self.LCG_svnpath, self.LCG_svntag)
        print self.argv0, ': INFO: %s', cmd
        os.system(cmd)

 
    def svn_gaudi(self):
        self.get_svn_generic()
 

    def cvs_geant4(self):
        os.chdir(self.LCG_builddir)
        destdir = os.path.join(self.package,self.LCG_package_config_version)
        if not os.path.exists(destdir):
            try :
                os.makedirs(destdir)
            except Exception, e:
                print self.argv0, ': ERROR: problem creating directory %s in %s: ' % (self.package, self.LCG_package_config_version), e
                sys.exit(1)
        os.chdir(self.package)
      
        prot= 'ext'
        if sys.platform == 'linux2': prot='gserver'
        userNameVar='USER'
        if sys.platform == 'win32': userNameVar='USERNAME'
              
        command="cvs -d :"+prot+":"+os.environ[userNameVar]+"@geant4.cvs.cern.ch:/cvs/Geant4 checkout -l -d "+self.LCG_package_config_version+" geant4"

        print self.argv0, ': INFO: %s' % command
        os.system(command)
        os.chdir(self.LCG_package_config_version)

        # checkout module benchmarks within geant4
        command="cvs -d :"+prot+":"+os.environ[userNameVar]+"@geant4.cvs.cern.ch:/cvs/Geant4 checkout -l benchmarks"
        os.system(command)
        
        import urllib
        used_tags = open('gettags.txt', 'w')
        
        tags_url= 'http://geant4.cern.ch/cgi-bin/bonsai/nightly/gettaglist.cgi?version=' + self.LCG_package_config_version
        if os.environ['geant4_tagsdb'] == "g4tags":
            tags_url = "http://sftweb.cern.ch/geant4/geant4tags/cvs/%s"%self.LCG_package_config_version
        file = urllib.urlopen(tags_url).read()
        used_tags.write(file)
        used_tags.close()
        
        numbers=file.split('\n')
            
        for line in numbers:
            try:
                #print os.path.realpath(os.curdir)
                sys.stdout.write(os.path.realpath(os.curdir)+'\n')
                if line.startswith('#'): continue
                module,tag = line.split()
                command="cvs -qq -d :"+prot+":"+os.environ[userNameVar]+"@geant4.cvs.cern.ch:/cvs/Geant4 update -d -P -r " + tag + " " + module
                #print self.argv0, ': INFO: %s' % command
                sys.stdout.write('%s: INFO:\n\t %s\n' % (self.argv0, command))
                sys.stdout.flush()
                os.system(command)
            except:
                continue

    def svn_geant4(self):
        os.chdir(self.LCG_builddir)
        destdir = os.path.join(self.package,self.LCG_package_config_version)
        if not os.path.exists(destdir):
            try :
                os.makedirs(destdir)
            except Exception, e:
                print self.argv0, ': ERROR: problem creating directory %s in %s: ' % (self.package, self.LCG_package_config_version), e
                sys.exit(1)
        os.chdir(self.package)

        cern_svn_repos= 'svn+ssh://svn.cern.ch/reps'

        os.chdir(self.LCG_package_config_version)

        if  self.LCG_package_config_version.endswith("_branch") :
            command="svn checkout svn+ssh://svn.cern.ch/reps/geant4/branches/geant4/_symbols/%s ."%(self.LCG_package_config_version)
            print command
            sys.stdout.flush()
            os.system(command)
            command="svn checkout svn+ssh://svn.cern.ch/reps/g4tests/tags/benchmarks/_symbols/%s benchmarks"%(os.environ['geant4_benchmarks'])
            print command
            sys.stdout.flush()
            os.system(command)
            return
        
        import urllib
        tags_url = "http://sftweb.cern.ch/geant4/geant4tags/gettaglist/%s"%self.LCG_package_config_version
        used_tags = open('gettags.txt', 'w')
        taglist = urllib.urlopen(tags_url).read()
        used_tags.write(taglist)
        used_tags.close()

        replace_dot_with_geant4 = lambda str:str.replace(".", "geant4",1)
        remove_dot_slach = lambda str:str.replace("./", "",1)

        class modes:
            NONE = 0
            CHECKOUT = 1 
            ROOT_UPDATE = 2
            SPECIAL_CHECKOUT = 3
            CATEGORIES = 4

        def checkout(line):
            repository, global_name = line.split()
            command = "svn checkout %s/%s/tags/geant4/_symbols/%s . -N"%(cern_svn_repos, repository, global_name)
            return command

        def root_update(line):
            what, = line.split()
            what = remove_dot_slach(what)
            command = "svn update %s"%what
            return command

        def special_checkout(line):
            repository, name, path, origin_path = line.split()
            command = "svn checkout %s/%s/tags/%s/_symbols/%s %s"%(cern_svn_repos, repository, origin_path, name, path)
            return command

        def switch(line):
            temp = line.split()
            file = None;
            if len(temp) == 4: status, repository, name, path = temp
            elif len(temp) == 5: status, repository, name, path, file = temp

            origin_path = replace_dot_with_geant4(path)
            if file:
                if os.path.exists(path+"/"+file):
                    command = "svn switch %s/%s/tags/%s/_symbols/%s/%s %s"%(cern_svn_repos, repository, origin_path, name, file, path+"/"+file)
                else:
                    if not os.path.exists(path): os.makedirs(path)
                    command = "svn cp %s/%s/tags/%s/_symbols/%s/%s %s"%(cern_svn_repos, repository, origin_path, name, file, path+"/"+file)
            else:
                if os.path.exists(path) :
                    command = "svn switch %s/%s/tags/%s/_symbols/%s %s"%(cern_svn_repos, repository, origin_path, name, path)
                else:
                    os.makedirs(path)
                    command = "svn co %s/%s/tags/%s/_symbols/%s %s"%(cern_svn_repos, repository, origin_path, name, path)
            return command

        mode = modes.NONE;
        lines = taglist.split('\n')
        for line in lines:
            if line.startswith('#') or line == '': continue
            elif line == "CHECKOUT SECTION": mode = modes.CHECKOUT
            elif line == "ROOT UPDATE SECTION": mode = modes.ROOT_UPDATE
            elif line == "SPECIAL CHECKOUT SECTION": mode = modes.SPECIAL_CHECKOUT
            elif line == "CATEGORIES SECTION": mode = modes.CATEGORIES
            else:
                if mode == modes.CHECKOUT: command = checkout(line)
                elif mode == modes.ROOT_UPDATE: command = root_update(line) 
                elif mode == modes.SPECIAL_CHECKOUT: command = special_checkout(line)
                elif mode == modes.CATEGORIES: command = switch(line)
                
                print command
                sys.stdout.flush()
                if os.system(command) == 1: return 1
            #command = "rm -rf `find . -type d -name .svn`"
            #os.system(command) 

    def get(self):
        if self.LCG_get == 'cp'     : self.get_cp()
        elif self.LCG_get == 'scp'  : self.get_scp()
        elif self.LCG_get == 'http' : self.get_http()
        elif self.LCG_get == 'cvs'  : self.get_cvs()
        elif self.LCG_get == 'svn'  : self.get_svn_generic()
        elif self.LCG_get == 'root'  : self.get_root()
        elif self.LCG_get == "cvs_generic": self.get_cvs_generic()
        elif self.LCG_get == "cvs_gaudi": self.cvs_gaudi()
        elif self.LCG_get == "svn_gaudi": self.svn_gaudi()
        elif self.LCG_get == "cvs_geant4": self.cvs_geant4()
        elif self.LCG_get == "svn_geant4": self.svn_geant4()
        else : print self.argv0, ': ERROR: Method %s (value of cmt set LCG_get) not supported' % self.LCG_get

if __name__ == '__main__':
    pg = pkg_get()
    pg.get()
