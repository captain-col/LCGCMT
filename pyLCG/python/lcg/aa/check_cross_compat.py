#!/usr/bin/env python
import os,time

class Checker(object):

    def __init__(self):
        self._libs=[]
        self._fulllibs=[]
        self._nolibs=[]
        self._dir='../../../../LCG_Interfaces' 


    def find_dependencies(self):
        packages=os.listdir(self._dir)
        for p in packages:
            dir=self._dir+os.sep+p+os.sep+"cmt"
            cmdir="cd "+dir+" ; "
            cmd="cd "+dir+" ; cmt show macro_value "+p+"_home"
            input,out,err=os.popen3(cmd)
            pkg_home=out.readline().strip()
            if pkg_home == "" : 
                print "no proper value found for %s_home, skipping package %s" % (p,p)
                continue
            else :
                print "processing package",p
            if pkg_home[-1] != os.sep : pkg_home += os.sep
            bindir=pkg_home+"bin"+os.sep

            bins = []

            if os.path.isdir(bindir) : map(lambda x: bins.append(bindir+x), os.listdir(bindir))

            input,outp,error = os.popen3('find %s -name "*.so*"' % pkg_home)

            map(lambda x: bins.append(x[:-1]), outp.readlines())

            eout = error.read()
            if len(eout) : print eout

            purebins = []
            for b in bins :
                if os.path.islink(b) and os.path.realpath(b) in bins : continue
                else : purebins.append(b)
            
            for b in purebins :
                cmd = cmdir + " cmt run ldd " + b
                input,output,error = os.popen3(cmd)
                for l in output.readlines() :
                    ls = l.split()
                    if len(ls) and ls[-1][:3] == '(0x' and ls[-1][-1] == ')' :  # if the last entry in the line looks like an address we found a valid line (0x123456789)
                        libname = ls[0]
                        libfound = ''
                        if len(ls) > 2 and ls[2][:3] != '(0x' : libfound = ls[2]
                        self._fulllibs.append('%s:%s:%s:%s' % (p, b, libname, libfound))
                        libshort = libfound
                        if not len(libshort) : libshort = libname
                        if libshort not in self._libs:
                            self._libs.append(libshort)
                    else :
                        self._nolibs.append('%s:%s:%s' % (p, b, l))
                                              

    def print_dependencies(self): 
        cmtconfig=os.getenv('CMTCONFIG')
        print "writing result files"
        fs = open("LCG_dependencies_%s_short" % cmtconfig, 'w')
        map ( lambda x: fs.write(x+'\n'), self._libs)
        fs.close()
        ff = open("LCG_dependencies_%s_full" % cmtconfig, 'w')
        map ( lambda x: ff.write(x+'\n'), self._fulllibs)
        ff.close()
        fe = open("LCG_dependencies_%s_error" % cmtconfig, 'w')
        map ( lambda x: fe.write(x), self._nolibs)
        fe.close()

if __name__ == "__main__":
    c=Checker()
    c.find_dependencies()
    c.print_dependencies()
