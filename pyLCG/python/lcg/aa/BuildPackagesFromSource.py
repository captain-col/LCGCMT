#!/usr/bin/env python
from AFSConfiguration import *
from PackageInstallation import *
from checkLogFiles import *

class Main(object):

    def __init__(self,projects=None,force=False):
        self.afs=AfsConfiguration()
        self.pi=PackageInstallation()
        self.force=force
        if projects==None:
            self.afs.chargeProjects()
            self.pi._projects=self.afs._projects
            self.pi.createHierarchy()
        else:
            self.afs.chargeProjectsFromList(projects)
            self.afs.createHierarchyFromList()
            self.pi._projects=self.afs._projects



    def showErrors(self):
        file=open(self.logDir)

    def installInteraction(self,project):
        if self.afs.projectAlreadyInstalled(project)==True:
            print "Project "+project._name +" is already installed!"
            return False
        else:
                    self.afs.removeSymbolicLink(project)
                    self.pi.getConfig(project)
                    result=raw_input("Project "+project._name+" has been configured, do you want to install it ?(y or n) ")
                    while result not in ("y","n"):
                        result=raw_input("Project "+project._name+" has been configured, do you want to install it ?(y or n) ")
                    if result=='y':
                        self.pi.installProjects(project)
                        return True

    def installInteractionForced(self,project):
        if self.afs.projectAlreadyInstalled(project)==True:
            print "Project "+project._name +" is already installed"
            return False
        else:
            self.afs.removeSymbolicLinkForced(project)
            self.pi.getConfig(project)
            self.pi.installProjects(project)
            return True



    def installPackage(self,project):
         builders=".."+os.sep+".."+os.sep+".."+os.sep+".."+os.sep+"LCG_Builders"+os.sep
         if len(project._dependences)==0:
                 if project._isInstalled==False:
                     if self.installInteraction(project):
                         file=builders+project._name+"/cmt/logs/"+project._name+"_"+project._platform+"_"+"make.log"
                         log=LogChecker(True,file,project._platform)
                         log.checkFiles()
         else:
             for p in project._dependences:
                 pr=self.pi.getProject(p)
                 if pr==None:
                     result=raw_input("Project "+p+" is going to be installed as a symbolic link ?(y or n) ")
                     while result not in ("y","n"):
                         result=raw_input("Project "+p+" is going to be installed as a symbolic link ?(y or n) ")
                     if result=='y':
                         if self.afs.symblinkAlreadyInstalled(p)==False:
                             self.pi.createSymLink(p)
                         else:
                             print "Symbolic link already created"
                 else:
                     self.installPackage(pr)
             if self.installInteraction(project):
                 #print "Before generating the log files2"
                 file=builders+project._name+"/cmt/logs/"+project._name+"_"+project._platform+"_"+"make.log"
                 log=LogChecker(True,file,project._platform)
                 log.checkFiles()

    def installPackageForced(self,project):
         builders=".."+os.sep+".."+os.sep+".."+os.sep+".."+os.sep+"LCG_Builders"+os.sep
         if len(project._dependences)==0:
                 #print "There are not dependences"
                 if project._isInstalled==False:
                     if self.installInteractionForced(project):
                         file=builders+project._name+"/cmt/logs/"+project._name+"_"+project._platform+"_"+"make.log"
                         log=LogChecker(True,file,project._platform)
                         log.checkFiles()
         else:
             for p in project._dependences:
                 #print "Before getting the dependences of "+project._name
                 pr=self.pi.getProject(p)
                 #print "Dependences of "+project._name+" is "+p
                 if pr==None:
                         if self.afs.symblinkAlreadyInstalled(p)==False:
                             self.pi.createSymLink(p)
                         else:
                             print "Symbolic link already created"
                 else:
                     self.installPackageForced(pr)
             if self.installInteractionForced(project):
                 file=builders+project._name+"/cmt/logs/"+project._name+"_"+project._platform+"_"+"make.log"
                 log=LogChecker(True,file,project._platform)
                 log.checkFiles()

    def installPackages(self):
        for i in range(len(self.afs._projects)):
            project=self.afs._projects[i]
            if self.force == False:

                self.installPackage(project)
            else:
                self.installPackageForced(project)



    def checkAfs(self):
         for i in range(len(self.afs._projects)):
            project=self.afs._projects[i]
            print project._name
            #if self.afs.projectAlreadyInstalled(project)==True:
               # print "Project "+project._name +" is already installed"
                #return False
            #else:
            if self.force==False:
                    self.afs.checkProjectVolume(project)
            else:
                    self.afs.checkProjectVolumeForced(project)

    def releasePackages(self):
        for i in range(len(self.afs._projects)):
            project=self.afs._projects[i]
            if self.force==False:
                self.afs.release(project)
            else:
                self.afs.releaseForced(project)
# --------------------------------------------------------------------------------
def usage():

    print sys.argv[0],"[--projects] --action =[afs,install,release] [--force]"

    return
# ================================================================================
if __name__ == "__main__":
    import getopt
    options = sys.argv[1:]
    try:
        opts, args = getopt.getopt(options, 'h',
                                   ['help','action=','projects=','force'])
    except getopt.GetoptError:
        usage()
        sys.exit(-2)
    projects=None
    force=False
    action=""
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('--projects',):
            projects=a.split()
        if o in ('--action',):
            action=a.strip()
        if o in ('--force',):
            force=True

    if action not in('afs','release','install'):
        print "Action should be afs or install or release"
        sys.exit(-2)
    main=Main(projects,force)

    if action=='afs':
        main.checkAfs()
    if action=='install':
        main.installPackages()
    if action=='release':
        main.releasePackages()
