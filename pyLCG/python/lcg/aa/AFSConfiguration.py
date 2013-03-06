#!/usr/bin/env python
import os, sys

class Project(object):

    def __init__(self, name, base, proj, version, platform):
        self._name=name
        self._base=base
        self._proj=proj
        self._version=version
        self._platform=platform
        self._isInstalled=False
        self._isConfigured=False
        self._isReleased=False
        self._dependences=[]


class AfsConfiguration(object):

    def __init__(self):
        self._projects=[]
        self._dir=".."+os.sep+".."+os.sep+".."+os.sep+".."
    def chargeProjectsFromList(self, projects):
         for project in projects:
            line=project.strip()
            if line.islower() and line not in("gcc", "gmp", "mpfr", "roofit") :

                dir=self._dir+"/LCG_Builders/"+line+"/cmt/"

                cmdDir='cd '+dir
                cmd=cmdDir+" ; cmt show set_names"
                out, sets, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_basedir"
                out, base, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_pkgdest_pkgname"
                out, proj, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_pkgdest_vername"
                out, version, err=os.popen3(cmd)
                cmd=cmdDir+" ; echo $CMTCONFIG"
                out, platform, err=os.popen3(cmd)
                version=version.readline().strip()
                proj=proj.readline().strip()
                platform=platform.readline().strip()
                for set in sets:
                    set=set.strip()
                    if set=="LCG_destdir" and version!="":
                        p=Project(line, base.readline().strip(), proj, version, platform)
                        self._projects.append(p)

    def projectAlreadyInstalled(self, p):

        dir=self._dir+"/LCG_Builders/"
        dir+=p._name+"/cmt"
        cmd ="cd "+dir+" ; cmt show set_value LCG_pkgdest_pkgname"

        out, input, err=os.popen3(cmd)
        input=input.readline()
        input=input.strip()
        if input.strip()!="":

              dir+=p._name+"/cmt"
              cmd ="cd "+dir+" ; cmt show set_value LCG_pkgdest_vername"
              out, version, err=os.popen3(cmd)
              version=version.readline().strip()

              if version!="":
                  dir=p._base+"/"+input+"/"+version+"/"+p._platform
              else:
                  dir=p._base+"/"+input+"/"+p._version+"/"+p._platform


        else:
             dir=p._base+"/"+p._name+"/"+p._version+"/"+p._platform


        if os.path.exists(dir)==True:
            if os.path.islink(dir)==True:
                print "Is a symbolic link"
                return False
            return True
        return False

    def symblinkAlreadyInstalled(self, p):


        dir=self._dir+"/LCG_Builders/"
        dir+=p+"/cmt"
        cmd ="cd "+dir+" ; cmt show set_value LCG_pkgdest_pkgname"

        out, input, err=os.popen3(cmd)
        input=input.readline()
        input=input.strip()
        cmd=cmd ="cd "+dir+" ; echo $CMTCONFIG"
        out, platform, err=os.popen3(cmd)
        platform=platform.readline()
        platform=platform.strip()

        dir ="/afs/cern.ch/sw/lcg/external/"
        if input.strip()!="":
                  dir+=input+"/"+platform


        else:
             dir+=p+"/"+platform

        if os.path.isdir(dir)==True:
            return True
        return False

    def getProjectName(self, name):
         out, input, err=os.popen3("ls  "+self._dir+"/LCG_Builders/")
         for line in input:
            line=line.strip()

            if line.islower() and line ==name:
                dir=self._dir+"/LCG_Builders/"+line+"/cmt/"

                cmdDir='cd '+dir
                cmd=cmdDir+" ; cmt show set_names"
                out, sets, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_basedir"
                out, base, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_pkgdest_pkgname"
                out, proj, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_pkgdest_vername"
                out, version, err=os.popen3(cmd)
                cmd=cmdDir+" ; echo $CMTCONFIG"
                out, platform, err=os.popen3(cmd)
                version=version.readline().strip()
                proj=proj.readline().strip()
                platform=platform.readline().strip()
                for set in sets:
                    set=set.strip()
                    if set=="LCG_destdir" and version!="":
                        p=Project(line, base.readline().strip(), proj, version, platform)
                        self._projects.append(p)

    def createHierarchyFromList(self):
        for project in self._projects:
            dir=self._dir+"/LCG_Builders/"+project._name+"/cmt/"
            cmd="cd "+dir +" ; cmt show uses "
            out, input, err=os.popen3(cmd)
            for i in input:
                if i.find("LCG_Interfaces")!=-1:
                    words=i.split()
                    if words[0]!="#":
                        dep=words[1]
                        project._dependences.append(dep.lower())
                        self.getProjectName(dep.lower())

    def chargeProjects(self):
        out, input, err=os.popen3("ls "+self._dir+"/LCG_Builders/")
        for line in input:
            line=line.strip()
            if line.islower() and line not in("gcc", "gmp", "mpfr", "roofit") :
                dir=self._dir+"/LCG_Builders/"+line+"/cmt/"
                cmdDir='cd '+dir
                cmd=cmdDir+" ; cmt show set_names"
                out, sets, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_basedir"
                out, base, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_pkgdest_pkgname"
                out, proj, err=os.popen3(cmd)
                cmd=cmdDir+" ; cmt show set_value LCG_pkgdest_vername"
                out, version, err=os.popen3(cmd)
                cmd=cmdDir+" ; echo $CMTCONFIG"
                out, platform, err=os.popen3(cmd)
                version=version.readline().strip()
                proj=proj.readline().strip()
                platform=platform.readline().strip()

                for set in sets:
                    set=set.strip()
                    if set=="LCG_destdir" and version!="":
                        p=Project(line, base.readline().strip(), proj, version, platform)
                        self._projects.append(p)

    def showProjects(self):
        for i in range(len(self._projects)):
            print self._projects[i]._name, self._projects[i]._pkgbindir

    def removeSymbolicLink(self, p):
            dir=p._base+"/"+p._proj+"/"+p._version
            dir2=dir+"/"+p._platform
            if os.path.islink(dir2)==False:
                print p._proj +" is not a symbolic link"
            else:
                print p._proj+" is  a symbolic link. It will be removed"
                cmd="cd "+dir +" ; rm "+p._platform
                result=raw_input("Are you sure you want to execute "+cmd+" ? (y or n)")
                while result not in ("y", "n"):
                    result=raw_input("Are you sure you want to execute "+cmd+" ? (y or n)")
                if result =="y":
                    ret=os.system(cmd)
                    if ret!=0:
                            print "Error during the execution of "+cmd

    def removeSymbolicLinkForced(self, p):
            dir=p._base+"/"+p._proj+"/"+p._version
            dir2=dir+"/"+p._platform
            if os.path.islink(dir2)==False:
                print p._proj +" is not a symbolic link"
            else:
                print p._proj+" is  a symbolic link. It will be removed"
                cmd="cd "+dir +" ; rm "+p._platform
                ret=os.system(cmd)
                if ret!=0:
                    print "Error during the execution of "+cmd


    def checkProjectVolume(self, p):
            basedir="/afs/.cern.ch/sw/lcg/external"
            dir=basedir+"/"+p._proj+"/"+p._version
            dir2=dir+"/"+p._platform

            cmd = "fs lq "+dir
            print cmd
            out, result, err=os.popen3(cmd)
            line =result.readline()
            line2 =result.readline()
            print line, line2
            if line2 =="":
                print "Base is "+p._base+" Project is "+p._proj+" version is "+p._version
                print dir+" is not created "
                result=raw_input("You need to create the volume "+dir+" are you sure ? (y or n)")
                while result not in ("y", "n"):
                    result=raw_input("You need to create the volume "+dir+" are you sure ? (y or n)")
                if result=='y':
                    volume_name= raw_input("Enter the name of the volume ")
                    volume_name=volume_name.strip()
                    size=raw_input("Enter the size of the new volume")
                    cmd="cd "+dir+" ; afs_admin create -q"+size+" K . "+volume_name
                    result=raw_input("Are you sure you want to execute "+cmd+" ? (y or n)")
                    while result not in ("y", "n"):
                            result=raw_input("You need to create the volume "+dir+" are you sure ? (y or n)")
                    if result =="y":
                        ret=os.system(cmd)
                        if ret!=0:
                            print "Error during the execution of "+cmd
                        pass

            else:
                print dir+" has been created "
                files=os.listdir(dir)
                installedPlatforms=0
                for i in files:
                    i=i.strip()
                    if i.startswith("slc4") or i.startswith("win32") or i.startswith("os") or i.startswith("i686") or i.startswith("x86"):
                        if os.path.islink(dir+"/"+i):

                            pass
                        else:
                            installedPlatforms+=1


                if installedPlatforms ==0:
                    installedPlatforms=1
                print line2
                words=line2.split()
                quota=words[1]
                quota=int(quota)
                used= words[2]
                used=float(used)
                quotaNeeded=float(used/installedPlatforms)
                newTotalQuota=float(quotaNeeded+used)
                incrementQuota=newTotalQuota>quota
                print str(quota), str(quotaNeeded), str(newTotalQuota), str(incrementQuota)
                decimal=quotaNeeded-int(quotaNeeded)
                if decimal >=0.5:
                    quotaNeeded=int(quotaNeeded)+1
                else:
                    quotaNeeded=int(quotaNeeded)
                if incrementQuota==0:
                       print "There are enough space"
                else:
                    print "You need to add "+str(quotaNeeded)+ " K space"
                    dirsq="/afs/.cern.ch/sw/lcg/external/"+p._proj+"/"+p._version
                    cmd="cd "+dirsq+" ; afs_admin sq `pwd`"+" +"+str(quotaNeeded)+"K"
                    result=raw_input("Are you sure you want to execute "+cmd+" ? (y or n)")
                    while result not in ("y", "n"):
                           result=raw_input("Are you sure you want to execute "+cmd+" ? (y or n)")
                    if result =="y":
                        ret=os.system(cmd)
                        if ret!=0:
                            print "Error during the execution of "+cmd
                        pass

    def checkProjectVolumeForced(self, p):
            basedir="/afs/.cern.ch/sw/lcg/external"
            dir=basedir+"/"+p._proj+"/"+p._version
            dir2=dir+"/"+p._platform

            cmd = "fs lq "+basedir+"/"+p._proj+"/"+p._version
            out, result, err=os.popen3(cmd)
            line =result.readline()
            line2 =result.readline()
            if line2 =="":
                print "Base is "+p._base+" Project is "+p._proj+" version is "+p._version
                print dir+" is not created "
                volume_name= raw_input("Enter the name of the volume ")
                volume_name=volume_name.strip()
                size=raw_input("Enter the size of the new volume")
                cmd="cd "+dir+" ; afs_admin create -q"+size+" K . "+volume_name
                ret=os.system(cmd)
                if ret!=0:
                        print "Error during the execution of "+cmd

            else:
                print dir+" has been created "
                files=os.listdir(dir)
                installedPlatforms=0
                for i in files:
                      if i.startswith("slc4") or i.startswith("win32") or i.startswith("os") or i.startswith("i686") or i.startswith("x86"):

                        if os.path.islink(dir+"/"+i):
                            print i+" Is symbolic link"
                        else:
                            installedPlatforms+=1
                            print i+" Is not a symbolic link"

                if installedPlatforms ==0:
                    installedPlatforms=1
                print line2
                words=line2.split()
                quota=words[1]
                quota=int(quota)
                used= words[2]
                used=float(used)
                quotaNeeded=float(used/installedPlatforms)
                newTotalQuota=float(quotaNeeded+used)
                incrementQuota=newTotalQuota>quota
                print str(quota), str(quotaNeeded), str(newTotalQuota), str(incrementQuota)
                decimal=quotaNeeded-int(quotaNeeded)
                if decimal >=0.5:
                    quotaNeeded=int(quotaNeeded)+1
                else:
                    quotaNeeded=int(quotaNeeded)
                if incrementQuota==0:
                       print "There are enough space"
                else:
                    print "You need to add "+str(quotaNeeded)+ " K space"
                    dirsq="/afs/.cern.ch/sw/lcg/external/"+p._proj+"/"+p._version
                    cmd="cd "+dirsq+" ; afs_admin sq `pwd`"+" +"+str(quotaNeeded)+"K"
                    ret=os.system(cmd)
                    if ret!=0:
                        print "Error during the execution of "+cmd

    def releaseForced(self, p):
            base="/afs/cern.ch/sw/lcg/external"
            dir=base+"/"+p._proj+"/"+p._version
            cmd = "fs lq "+p._base+"/"+p._proj+"/"+p._version
            out, result, err=os.popen3(cmd)
            print err.readline()
            line =result.readline()
            print line
            line2 =result.readline()

            if line2!="":
                volume=line2.split()[0]
                print "Volume is "+volume+" Project is "+p._name
                parts=volume.split(".")
                if len(parts)==4:
                #if volume.endswith("readonly") or volume.endswith("readonl"):
                    print p._name+" Is not read only"
                    cmd="cd "+dir+" ; afs_admin create_replica "+volume
                    ret=os.system(cmd)
                    if ret!=0:
                            print "Error during the execution of "+cmd
                else:
                            dir="/afs/.cern.ch/sw/lcg/external/"+p._proj+"/"+p._version
                            cmd="cd "+dir+" ; afs_admin v_r `pwd`"
                            ret=os.system(cmd)
                            if ret!=0:
                                    print "Error during the execution of "+cmd


    def release(self, p):
            base="/afs/cern.ch/sw/lcg/external"
            dir=base+"/"+p._proj+"/"+p._version
            cmd = "fs lq "+p._base+"/"+p._proj+"/"+p._version
            out, result, err=os.popen3(cmd)
            print err.readline()
            line =result.readline()
            print line
            line2 =result.readline()

            if line2!="":
                volume=line2.split()[0]
                print "Volume is "+volume+" Project is "+p._name
                parts=volume.split(".")
                if len(parts)==4:
                #if volume.endswith("readonly") or volume.endswith("readonl"):
                    print p._name+" Is not read only"
                    cmd="cd "+dir+" ; afs_admin create_replica "+volume
                    result=raw_input("Are you sure you want to execute "+cmd+ "(y or n)")
                    while result not in ("y", "n"):
                        result=raw_input("Are you sure you want to execute "+cmd+ "(y or n)")
                    if result=="y":
                        ret=os.system(cmd)
                        if ret!=0:
                            print "Error during the execution of "+cmd
                else:
                            dir="/afs/.cern.ch/sw/lcg/external/"+p._proj+"/"+p._version
                            cmd="cd "+dir+" ; afs_admin v_r `pwd`"
                            result=raw_input("Are you sure you want to execute "+cmd+"(y or n)")
                            while result not in ("y", "n"):
                                result=raw_input("Are you sure you want to execute "+cmd+ "(y or n)")
                            if result=="y":
                                ret=os.system(cmd)
                                if ret!=0:
                                    print "Error during the execution of "+cmd
