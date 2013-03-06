#!/usr/bin/env python
import os,sys,time
#import subprocess

class PackageInstallation(object):

    def __init__(self):
        self._projects=[]
        self._dir=".."+os.sep+".."+os.sep+".."+os.sep+".."+os.sep+"LCG_Builders"+os.sep
        self._dirInterfaces=".."+os.sep+".."+os.sep+".."+os.sep+".."+os.sep+"LCG_Interfaces"+os.sep

    def createHierarchy(self):
        for project in self._projects:
            dir=self._dir+project._name+"/cmt/"
            cmd="cd "+dir +" ; cmt show uses "
            out,input,err=os.popen3(cmd)
            for i in input:
                if i.find("LCG_Interfaces")!=-1:
                    words=i.split()
                    if words[0]!="#":
                        dep=words[1]
                        project._dependences.append(dep.lower())
                        #print dep

    def getProject(self,name):
        for project in self._projects:
            if project._name==name: return project
        return None

    def getConfig(self,project):
         dir=self._dir+project._name+"/cmt/"
         cmd ="cd "+dir+" ; cmt pkg_get > /dev/null 2>&1"
         ret=os.system(cmd)
         cmd ="cd "+dir+" ; cmt pkg_config > /dev/null 2>&1"
         ret=os.system(cmd)
         if ret!=0:
            print "Error during the execution of "+cmd
         project._isConfigured=True

    def install(self,project):
         if project._isConfigured==False:
            self.getConfig(project)
         dir=self._dir+project._name+"/cmt/"
         cmd ="cd "+dir+" ; cmt pkg_make > /dev/null 2>&1"
         ret=os.system(cmd)
         if ret!=0:
            print "Error during the execution of "+cmd
         cmd ="cd "+dir+" ; cmt pkg_install > /dev/null 2>&1"
         ret=os.system(cmd)
         if ret!=0:
            print "Error during the execution of "+cmd
         cmd ="cd "+dir+" ; cmt pkg_loginstall > /dev/null 2>&1"
         ret=os.system(cmd)
         if ret!=0:
            print "Error during the execution of "+cmd

         project._isInstalled=True
         print project._name +" has been installed"

    def installProjects(self,project):
            if project._isInstalled==False :
                self.installProject(project)

    def createSymLink(self,dep):
                    dir=self._dirInterfaces
                    dir+=dep+"/cmt"
                    cmd ="cd "+dir+" ; cmt show macro "+dep+"_home"
                    out,input,err=os.popen3(cmd)
                    input=input.readline()
                    words=input.split("'")
                    project_home=words[1]
                    steps=project_home.split("/")
                    external=steps[0]
                    external=external.split("(")[1].split(")")[0]
                    version=steps[2]
                    version=version.split("(")[1].split(")")[0]
                    config=steps[3]
                    config=config.split("(")[1].split(")")[0]
                    cmd="cd "+dir+" ; cmt show set_value "+external
                    out,externaldir,err=os.popen3(cmd)
                    cmd="cd "+dir+" ; cmt show set_value "+version
                    out,versiondir,err=os.popen3(cmd)
                    cmd="cd "+dir+" ; cmt show set_value "+config
                    out,configdir,err=os.popen3(cmd)
                    externaldir=externaldir.readline().strip()
                    versiondir=versiondir.readline().strip()
                    configdir=configdir.readline().strip()
                    link_dir=externaldir+"/"+dep+"/"+versiondir+"/"+configdir
                    dir ="/afs/cern.ch/sw/lcg/external/"
                    cmd ="dir"+link_dir
                    if os.path.isdir(cmd)==False:
                        cmd ="cd "+dir+" ; ln -s "+link_dir+" ./"+dep
                        ret=os.system(cmd)
                    else :
                        print dir+link_dir+" is already installed"

    def installProject(self,project):

        if project._isInstalled==False:
            self.install(project)



