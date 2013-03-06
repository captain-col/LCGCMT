#!/usr/bin/env python
import sys


class SortFile:
    def __init__(self,target,fileName):
        self._target=target
        self._fileName=fileName
        self._buffer=100*[None]
        self._lineEnding="\r\n"
        self._counter=0
        
    def sortFile(self):
        file= open(self._fileName,"r")
        print "File name is ",self._fileName
        lineList=file.readlines()
        file.close()
        fileLenght=len(lineList)
        
        index=0
        task=""
        line=lineList[index]

        while index<fileLenght:
            
            if line.find("#-")!=-1:
                line1=line
                index+=1
                print "INDEX IS, TOTAL IS ",index,len(lineList)
                line=lineList[index]
                
                if line.find(self._target)==-1:
                    continue
                task+=line1
                task+=line
               
                
                print "Line before task_number is ",line
                task_number=line.split()[1].split("(")[1].split("/")[0]
                task_number=int(task_number)
                index+=1
                task+=lineList[index]
                index+=1
                line=lineList[index]
                
                while line.find("#-")==-1 and index<fileLenght:
               
                    task+=line
                    index+=1
                
                    if index<fileLenght:
                        line=lineList[index]
                
                
                task+=line
               
                if self._buffer[task_number]==None:
                    self._counter+=1
                    print "SELF.COUNTER IS, task_number is ",self._counter,task_number,task==None
                self._buffer[task_number]=task
                task=""
                continue
            
            index+=1
            if index<fileLenght:
                line=lineList[index]
                
    def writeFile(self):
        
        file=open(self._fileName+self._target,"w")
        i=1
        file.write("#----------------Results for target "+self._target+self._lineEnding)
        
        while i<= self._counter:
            print "i,counter,buffer",i,self._counter,self._buffer[i]
            file.write(self._buffer[i])
            i+=1

        file.close()    
            

def usage():
    print ""
    print "usage: ",sys.argv[0]," [--target '<target_name>'][--file '<file_name>'] "
    print ""
    return
                

if __name__=="__main__":
    import getopt
    options = sys.argv[1:]
    if len(options)==0:
            usage()
            sys.exit(-2)
    try:
            opts, args = getopt.getopt(options, 'hs:m:p:',['help','target=','file='])
    except getopt.GetoptError, e:
           print e.msg
           usage()
           sys.exit(-2)
    target=""
    file=""
    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()
    
        if o in ("--target"):
            target=a

        if o in ("--file"):
            file=a

    sf=SortFile(target,file)
    sf.sortFile()
    sf.writeFile()
