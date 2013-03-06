#!/usr/bin/env python
from AFSConfiguration import *
import shutil
import distutils.dir_util
import os
import platform
import string

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

class Synchronization (object):

    def __init__(self,all=False,externals=False,internals=False,nightlies=False,dest="",list=None,justBinaries=False):
        self._dir=".."+os.sep+".."+os.sep+".."+os.sep+".."+os.sep+"LCG_Interfaces"+os.sep
        self._builders=".."+os.sep+".."+os.sep+".."+os.sep+".."+os.sep+"LCG_Builders"+os.sep
        self._projects=[] 	
        self._all=all
        self._externals=externals
        self._internals=internals
        self._nightlies=nightlies
        self._list=list
        self._justBinaries=justBinaries
        self._dict={}
        self._slot=""
        self._day=""
        self._dest=dest
        if platform.system() in ("Linux","Darwin"):
              self._cmdsep=";"
              self._cmtconfig="echo $CMTCONFIG"
        else:
              self._cmdsep="&"
              self._cmtconfig="echo %CMTCONFIG%"
        self.createDictionary()      
        if self._list==None:
          pass
          self.chargeProjects()    
         
        else:
             self.chargeProjectsFromList()
       
        self.sincrhonize()
            
     #Stores into the dict array the project names copied from LCG_Configuration, this includes the external and the "nightlies" projects        
    def createDictionary(self):
       
        dir=".."+os.sep+".."+os.sep+".."+os.sep+".."+os.sep+"LCG_Configuration"+os.sep+"cmt"+os.sep+"requirements"
                
        if self._nightlies:
            
            cmd="less "+dir+ " | grep LCG_NGT_SLT_NAME"
            input,output,err=os.popen3(cmd)
            line=output.readline()
            line=line.split()
            self._slot=line[2].split('"')[1]

       
            cmd="less "+dir+ " | grep LCG_NGT_DAY_NAME"
            input,output,err=os.popen3(cmd)
            line=output.readline()
            line=line.split()
            self._day=line[2].split('"')[1]
       
       
        cmd ="less "+dir+"  | grep macro "
        input,output,err=os.popen3(cmd)
        lines=output.readlines()
        
        for line in lines:
            line=line.split()
            line=line[1].split("_config")
            name=line[0]
            if name.lower() not in self._dict.keys():
                self._dict[name.lower()]=name
                #print "ADDED:",name
                
        input=os.listdir(self._dir)
        for name in input:
            if name.lower() not in self._dict.keys():
               self._dict[name.lower()]=name
              # print "ADDED:",name
            

    def chargeProjectsFromList(self):
        for name in list:
            line=name.upper()
            internal_project=0
            if line in ("COOL","CORAL","GAUDI","GAUDIATLAS","POOL","ROOT","RELAX", "LCGCMT"):
                    internal_project=1
                    if line in ('LCGCMT', 'GAUDI','GAUDIATLAS'):
                         dir=self._builders+line+os.sep+"cmt"+os.sep
                    else:     
                        dir=self._dir+line+os.sep+"cmt"+os.sep
                    if platform.system() in ("Linux","Darwin"):

                        if self._nightlies:


                            base=os.sep+"build"+os.sep+"nightlies"+os.sep+self._slot+os.sep+self._day
                 
            else:
                 
                    dir=self._dir+os.sep+self._dict[line.lower()]+os.sep+"cmt"+os.sep
            cmdDir='cd '+dir
            if line in ('GAUDI','GAUDIATLAS'):
                cmd=cmdDir+self._cmdsep+"cmt show set_value LCG_destdir"
                input,base_dir,err=os.popen3(cmd)
                base_dir=base_dir.readline()
                base_dir=base_dir.replace("/",os.sep)
                base_dir_aux=base_dir.split(os.sep)
                version=base_dir_aux[len(base_dir_aux)-1]
                proj=base_dir_aux[len(base_dir_aux)-2]
                plat=""
                
                
                if version!="":

                   p=Project(proj.strip(),base_dir.strip(), proj.strip(), version.strip(), plat.strip())
                   self._projects.append(p)
                

            elif line not in("gcc", "gmp", "mpfr", "roofit") :


       
                cmd=cmdDir+self._cmdsep+"cmt show macro_value "+self._dict[line.lower()]+"_home"
                print "CMD BASE_DIR IS ",cmd
                input,base_dir,err=os.popen3(cmd)
                base_dir=base_dir.readline()
               
                base_dir=base_dir.replace("/",os.sep)
                base_dir_aux=base_dir.split(os.sep)
                print "BASE DIR IS ",base_dir
                if len(base_dir_aux)<=1:
                    continue
                proj=self._dict[line.lower()]
                
                if proj=="LCGCMT":
                   plat="" 
                   version=base_dir_aux[len(base_dir_aux)-1].split('/')[0]
                  
                elif proj=="ROOT":
                    version=base_dir_aux[len(base_dir_aux)-3]
                    plat=base_dir_aux[len(base_dir_aux)-2].split('/')[0]
                   
                else:
                    version=base_dir_aux[len(base_dir_aux)-2]
                    plat=base_dir_aux[len(base_dir_aux)-1].split('/')[0]
                    proj=base_dir_aux[len(base_dir_aux)-3]
                print proj,version,plat
                
                
                
                if nightlies and internal_project:
                    base_dir=base



                if version!="":

                       p=Project(proj.strip(),base_dir.strip(), proj.strip(), version.strip(), plat.strip())
                       self._projects.append(p)
                      # print "Added "+p._name



    def chargeProjects(self):
        
        input=os.listdir(self._dir)
        input.append("LCGCMT")
        input.append("GAUDI")
        input.append("GAUDIATLAS")
        select=False
        for line in input:
            line=line.strip()
            
            if self._all:
                select=True
                if line not in ("COOL","CORAL","GAUDI","GAUDIATLAS","POOL","ROOT","RELAX", "LCGCMT"):
                   line=line.lower()
            elif self._externals:
                 select=line not in ("COOL","CORAL","GAUDI","GAUDIATLAS","POOL","ROOT","RELAX", "LCGCMT")
                 line=line.lower()
            elif self._internals:
                   select=line  in ("COOL","CORAL","GAUDI","GAUDIATLAS","POOL","ROOT","RELAX", "LCGCMT")
                   
            dir=self._dir+self._dict[line.lower()]+os.sep+"cmt"+os.sep
            
            if line in ("COOL","CORAL","GAUDI","GAUDIATLAS","POOL","ROOT","RELAX", "LCGCMT"):
                if line in ("LCGCMT", "GAUDI","GAUDIATLAS"):
                    dir=self._builders+self._dict[line.lower()]+os.sep+"cmt"+os.sep
                    
                    if platform.system() in ("Linux","Darwin"):
                        if self._nightlies:                            
                            base=os.sep+"build"+os.sep+"nightlies"+os.sep+self._slot+os.sep+self._day
              
            cmdDir='cd '+dir

            if line in ('GAUDI','GAUDIATLAS'):
                cmd=cmdDir+self._cmdsep+"cmt show set_value LCG_destdir"
                input,base_dir,err=os.popen3(cmd)
                base_dir=base_dir.readline()
                base_dir=base_dir.replace("/",os.sep)
                base_dir_aux=base_dir.split(os.sep)
                version=base_dir_aux[len(base_dir_aux)-1]
                proj=base_dir_aux[len(base_dir_aux)-2]
                plat=""
                if version!="":
                   p=Project(proj.strip(),base_dir.strip(), proj.strip(), version.strip(), plat.strip())
                   self._projects.append(p)
            elif select and line not in("gcc", "gmp", "mpfr", "roofit") :
                

                cmd=cmdDir+self._cmdsep+"cmt show macro_value "+self._dict[line.lower()]+"_home"
               
                input,base_dir,err=os.popen3(cmd)
                base_dir=base_dir.readline()
                print "BASE DIR IS ",base_dir
                base_dir=base_dir.replace("/",os.sep)
                base_dir_aux=base_dir.split(os.sep)
                print " LEN IS ",len(base_dir_aux)
                if len(base_dir_aux)<=1:
                    continue
                proj=self._dict[line.lower()]
                if proj=="LCGCMT":
                    version=base_dir_aux[len(base_dir_aux)-1]
                    plat=""
                elif proj=="ROOT":
                     version=base_dir_aux[len(base_dir_aux)-3]
                     plat=base_dir_aux[len(base_dir_aux)-2]
                else:     
                    version=base_dir_aux[len(base_dir_aux)-2]
                    plat=base_dir_aux[len(base_dir_aux)-1]
                    proj=base_dir_aux[len(base_dir_aux)-3]
                
                                   
                if nightlies and self._internals:
                    base_dir=base.strip()
                if version !="":
                        p=Project(proj.strip(), base_dir.strip(), proj.strip(), version.strip(), plat.strip())


                        self._projects.append(p)

    def sincrhonize(self):
        
        for p in self._projects:

            name=p._name

            if self._dest!="":
               if name in ('LCGCMT','GAUDI','GAUDIATLAS'):
                    destBase=self._dest+os.sep+name+os.sep

              
               elif name=="ROOT" or platform.system() in ("Microsoft", "Windows"):
                    destBase=self._dest+os.sep+name+os.sep+p._version+os.sep+p._platform+os.sep
                    
               else:
                   print "In else destbase is "
                   destBase=self._dest+os.sep+name+os.sep+p._version+os.sep
                   print destBase 
                


            else:

                print "Missing destination folder"
                os.exit(-1)
            dest=destBase
            if os.path.exists(dest):
                print dest, "is already is already installed"
                continue
            base=p._base   
                    
            base=base.strip()

            
            try:
                           aux=base.replace("\\","\\\\")
                           base=base
                           #print "Before copying ",base, " in ",dest
                           if os.path.exists(aux):
                               
                               cmd="mkdir -p"+dest
                               os.system(cmd)
                               
                           if platform.system() in ("Microsoft","Windows"):
                               cmd="xcopy /s "+base+" "+dest
                               print cmd
                           else:    
                               cmd="rsync -avz "+base+" "+dest
                           os.system(cmd)
                           
                           if name=="ROOT":
                               
                               aux=base.split("/")
                               size=len(aux)
                               aux[size-1]="roottest"
                               base=string.join(aux,"/")
                               
                               cmd="mkdir -p "+dest
                               os.system(cmd)
                               
                               if platform.system() in ("Microsoft","Windows"):
                                   cmd="xcopy /s "+base+" "+dest
                               else:    
                                   cmd="rsync -avz "+base+" "+dest
                               
                               os.system(cmd)
                           
                           print "done"
            except Exception,detail:
                       try:
                               print detail
                               if os.path.isdir(base):
                                  cmd="mkdir -p "+dest
                                  os.system(cmd)
                               if platform.system() in ("Microsoft","Windows"):
                                   cmd="xcopy /s "+base+" "+dest
                               else:    
                                   cmd="rsync -avz "+base+" "+dest
                               os.system(cmd)
                               
                       except Exception, detail:
                              print detail
            if not self._justBinaries:
                
                try:
                                   base=p._base.replace(p._platform,"")
                                   destSrc=dest.replace(p._platform,"")
                                   destSrc+=os.sep+'src'
                                   base+=os.sep+'src'
                                   if os.path.isdir(base):
                                      cmd="mkdir -p "+dest
                                      os.system(cmd)
                                   if platform.system() in ("Microsoft","Windows"):
                                       cmd="xcopy /s "+base+" "+dest
                                   else:    
                                       cmd="rsync -avz "+base+" "+dest   
                                   
                                   os.system(cmd)
                         
                          
                         
                         
                except Exception,detail:
                               print detail
         
         
    
    
    



# --------------------------------------------------------------------------------
def usage():

    print sys.argv[0]," --all|--externals|--projects [nightlies & dest] [list=]"

    return
# ================================================================================


if __name__ == "__main__":


    import getopt
    options = sys.argv[1:]
    if options==[]:
        usage()
        sys.exit(-2)
    try:
        opts, args = getopt.getopt(options, 'h',
                                   ['help','all', 'externals','projects','nightlies','dest=','list=','bin'])
    except getopt.GetoptError:
        usage()
        sys.exit(-2)

    all=False
    externals=False
    projects=False
    justBinaries=False
    list=None
    nightlies=False
    dest=""
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
        if o in ('--all',):
            all=True
        if o in ('--externals',):
            externals=True
        if o in ('--projects',):
            projects=True
        if o in ('--nightlies',):
            nightlies=True
        if o in ('--dest',):
            dest=a.strip()
        if o in ('--list',):
            list=a.split()
        if o in ('--bin',):
            justBinaries=True

    if nightlies and dest=="":
            usage()
            sys.exit(-2)

    syn=Synchronization(all,externals,projects,nightlies,dest,list,justBinaries)

