#!/usr/bin/env python
 
import os, sys, re, time, socket
import logging, logging.config

spiScriptDir = os.path.abspath( os.path.dirname( sys.argv[0] ) )
#logging.config.fileConfig(os.path.join(spiScriptDir,"loggers"))
log=logging.getLogger("nightlies.console")
if len(log.handlers) == 0:
	handler = logging.StreamHandler()
	handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
	log.addHandler(handler)
	log.setLevel(logging.INFO)




class LogChecker(object) :

    # --------------------------------------------------------------------------------

    def __init__(self,html,file,platform) :

        self.htmlOut = None
        self.sumLog  = None
        self.logDir  = os.getcwd()+"/www"
        if not os.path.exists(os.getcwd()+"/www"):
            os.makedirs(os.getcwd()+"/www")
        self.errFiles = []
        self.htmlOut = html
        self.files=file
        #self.files.append(file)
        self.verbose = 1
        self.slot    = None
        self.plat=platform
        return

    # --------------------------------------------------------------------------------
    def setHtml(self, html) :
        self.htmlOut = html
        self.verbose = 0
        return
    # --------------------------------------------------------------------------------
    def setSlot(self, slot) :
        self.slot = slot
        return
    # --------------------------------------------------------------------------------

    def checkLog(self,file):

        pkgName = ""
        import re
        # on windows we don't start with a "/"
        prjAfs  = re.compile(".*../../../../LCG_Builders"+"/.*/([A-Za-z].*)/([A-Za-z].*)/logs/(.*)\.log")
        prjAfsMatch = prjAfs.match( os.path.abspath(file) )
        # set defaults for "any" logfile
        pkgName = file
        #plat = "unknown"
        if prjAfsMatch :  # it matches the path, so we can get more info
            pkgName = prjAfsMatch.group(2)
            plat = prjAfsMatch.group(3)
        # ignore logfiles from qmtest
        if pkgName.find("-qmtest") != -1 :
            nWarn, nErr = self.handleQMTestFile(pkgName)
            return nWarn, nErr, 0
        htmlFileName =  file.split("/")[9]+"-log.html"
        if self.verbose > 0 :
            log.info("================================================================================")
            log.info("checking " + pkgName + " on " +  self.plat)
            log.info("    file " +  os.path.abspath(file))
            log.info("================================================================================")
        if (self.htmlOut and self.sumLog ) :
            self.sumLog.write( '<image src="http://cern.ch/pfeiffer/aaLibrarian/colline.gif" width="90%" height="3"></image>\n')
            self.sumLog.write( '<h3>Checking <a href="'+htmlFileName+'"> log file for ' + pkgName + ' on ' + self.plat + '</a></h3>\n' )
            self.sumLog.write( '\n' )
            self.sumLog.write( "<p>\n")

        logFile = open(file, "r")
        lines = logFile.readlines()
        logFile.close()

        shortLog = False
	if ( (len(lines) < 200) and
             (pkgName.find("LCGCMT") == -1) ):
            if (self.htmlOut and self.sumLog ) :
                self.sumLog.write( '<font color="#ff0000"><b>Warning:</b> suspiciously short log file!</font>\n')
                shortLog = True

        reCMTErr = []
        reCMTErr.append( re.compile("Cannot read the requirements file") )

        matchMkErr1 = re.compile('.*make.*\WError\s*1.*')
        matchError  = re.compile('.*\Werror[: ].*', re.I)
        matchError1 = re.compile('^error .*', re.I)
        matchWarn   = re.compile('.*warning[: ].*', re.I)
        matchFailB  = re.compile('\.\.\.failed .*', re.I)  # boost's "...failed" messages
        matchDiskQ  = re.compile('.*isk quota exceeded.*', re.I)
        matchConf  = re.compile('Configuring Project .*', )
        matchBuild = re.compile('Building Project .*', )
        matchTest  = re.compile('Executing all tests .*', )
        matchInst  = re.compile('Installing Project .*', )

        nErr    = 0
        nMkErr  = 0
        nWarn   = 0
        nCMTErr = 0
        errorList = {}
        mkErrList = [] # make is "build" :-)
        warnList  = {}
        actualStep = "init"
        index = -1
        for line in lines:
            index += 1

            mMk = matchConf.match(line)
            if mMk : actualStep = "conf"
            mMk = matchBuild.match(line)
            if mMk : actualStep = "build"
            mMk = matchTest.match(line)
            if mMk : actualStep = "test"
            mMk = matchInst.match(line)
            if mMk : actualStep = "inst"

            # count failed make's (by package)
            mMkE1 = matchMkErr1.match(line)
            if mMkE1 :
                nMkErr += 1
                mkErrList.append(index)

            mErr  = matchError.match(line)
            mErr1 = matchError1.match(line)
            mDskQ = matchDiskQ.match(line)
            if mErr or mErr1 or mDskQ :          # treat errors and disk quota exceeded basically the same way ...

                if mErr or mErr1:               # ... but check the following only for real error messages
                    # ignore compiler flag (this needs more sophistication to not skip real errors)
                    if line.find("-Wno-error") != -1 : continue

                nErr += 1
                if actualStep not in errorList.keys() :
                    errorList[actualStep] = []
                errorList[actualStep].append(index)

            for reCMT in reCMTErr:
                matchCMTErr = reCMT.match(line)
                if matchCMTErr :
                    nCMTErr += 1
                    nErr += 1
                    if actualStep not in errorList.keys() :
                        errorList[actualStep] = []
                    errorList[actualStep].append(index)

            mWarn = matchWarn.match(line)
            if mWarn :
                # ignore genreflex warnings about not supported references
		ignoreWarnings = [
			"genreflex: WARNING: References are not supported as data members",
			"include/boost-1_34_1/boost/date_time/time_facet.hpp:202: warning: unused parameter 'a_ref'",
			"include/boost-1_34_1/boost/date_time/time.hpp:81: warning: unused parameter 'as_offset'",
			"include/boost-1_34_1/boost/date_time/time.hpp:88: warning: unused parameter 'as_offset'",
			"WARNING >> You should provide a target for",
			]


                nWarn += 1
                if actualStep not in warnList.keys() :
                    warnList[actualStep] = []
                warnList[actualStep].append(index)

		for x in ignoreWarnings:
			if line.find(x) != -1:
				nWarn -= 1
				if actualStep in warnList.keys() and index in warnList[actualStep]:
					warnList[actualStep].remove(index)


        # ---------- end analysis of logfile, now prepare output
        summaryFileName =   file.split("/")[9]+"-log.summary"
        sumFil = open( os.path.join(self.logDir, summaryFileName), 'w')
        now = time.time()
        sumFil.write(str(now) + " (" + time.ctime(now) + ") " +  " " + pkgName + " " + self.plat + "\n")
        if shortLog :
            sumFil.write(str(nWarn) + ", " + str(nErr+1) + ", " + str(nMkErr) + ", " + str(nCMTErr) + "\n")
        else:
            sumFil.write(str(nWarn) + ", " + str(nErr) + ", " + str(nMkErr) + ", " + str(nCMTErr) + "\n")
        sumFil.close()
        # print "Summary written to :", summaryFileName

        if self.htmlOut :
            errLines = []
            for key, value in errorList.items():
                for i in value:
                    if i not in errLines:
                        errLines.append(int(i))

            warnLines = []
            groupedWarnings = []
            for key, value in warnList.items():
                for i in value:
                    if i not in warnLines:
                    	warnLines.append(int(i))
                    	if int(i)-1 in warnLines: groupedWarnings.append(int(i))

            htmlFile = open(self.logDir + "/" + htmlFileName, 'w')
            htmlFile.write("<html>\n<head><title>LogCheck for package " + pkgName + " </title></head>\n<body>\n")
            htmlFile.write("<h3>LogCheck for package " + pkgName + " on " + socket.gethostname() +"</h3>\n")

            htmlFile.write('<p>\n')
            htmlFile.write('Warnings   : '+ str(nWarn) +' <br /> ')
            htmlFile.write('Errors     : '+str(nErr)   +' <br /> ')
            htmlFile.write('Make Errors: '+str(nMkErr) +' <br /> ')
            htmlFile.write('CMT  Errors: '+str(nCMTErr)+' <br /> ')
            htmlFile.write('</p>\n')
            # if there were make errors, list a summary of them
            if len(mkErrList) > 0 :
                htmlFile.write("<h3>Summary of make errors:</h3>\n")
                for index in mkErrList:
                    if (self.htmlOut and self.sumLog ) :
                        # htmlFile.write( '<a name="' + pkgName + '"></a>\n')
                        htmlFile.write( "<hr />\n")
                        htmlFile.write( '<a href="'+htmlFileName+'#line_' + str(index) + '">\n' )
                    try:
                        for delta in range(-2,2) :
                            if (self.htmlOut and self.sumLog ) :
                                htmlFile.write( str(index+delta) + " : " + lines[index+delta])
                            # print " ", index+delta, ":", lines[index+delta],
                    except IndexError:
                        pass
                    if (self.htmlOut and self.sumLog ) :
                        htmlFile.write( '</a>\n')
                htmlFile.write("<hr />\n")
            elif len(warnList.keys()) > 0:
            	htmlFile.write("<h3>Summary of warnings:</h3>\n")
                for index in warnList.values()[0]:
                    if index not in groupedWarnings:
	                    if (self.htmlOut and self.sumLog):
	                        htmlFile.write( "<hr />\n")
	                        htmlFile.write( '<a href="'+htmlFileName+'#line_' + str(index) + '">\n' )
	                    try:
	                        for delta in range(-2,2) :
	                            if (self.htmlOut and self.sumLog ) :
	                                htmlFile.write( str(index+delta) + " : " + lines[index+delta])
	                            # print " ", index+delta, ":", lines[index+delta],
	                    except IndexError:
	                        pass
	                    if (self.htmlOut and self.sumLog ) :
	                        htmlFile.write( '</a>\n')
                htmlFile.write("<hr />\n")



            htmlFile.write('<pre>\n')
            for index in range(len(lines)):
                if index in errLines :
                    htmlFile.write('</pre>\n')
                    htmlFile.write('<a name="line_' + str(index) + '">')
                    htmlFile.write('<font color="red" size+=3><b>\n')
                    htmlFile.write(lines[index])
                    htmlFile.write('</b></font>')
                    htmlFile.write('</a> \n')
                    htmlFile.write('<pre>\n')
                elif index in warnLines :
                    htmlFile.write('</pre>\n')
                    htmlFile.write('<a name="line_' + str(index) + '">')
                    htmlFile.write('<font color="blue" size+=3><b>\n')
                    htmlFile.write(lines[index])
                    htmlFile.write('</b></font>')
                    htmlFile.write('</a> \n')
                    htmlFile.write('<pre>\n')
                else:
                    htmlFile.write(lines[index])
            htmlFile.write("</pre>\n</body>\n</html>")
            htmlFile.close()

        errLimit = False
	if len(errorList.items()) > 500 :
            if (self.htmlOut and self.sumLog ) :
                self.sumLog.write( '<font color="#ff0000"><b>Caution:</b> Too many errors found ("+len(errorList.items())+"), further printout suppressed !!</font>\n')
                errLimit = True

        if self.verbose > 10 and not errLimit :
            for key, value in errorList.items() :
                log.debug("++++++++++" +  key)
                for index in value:
                    if (self.htmlOut and self.sumLog ) :
                        self.sumLog.write( '<a name="' + pkgName + '"></a>\n')
                        self.sumLog.write( "<hr />\n")
                        self.sumLog.write( '<a href="'+htmlFileName+'#line_' + str(index) + '">\n' )
                    try:
                        log.debug("------------------------------------------")
                        for delta in range(-2,2) :
                            if (self.htmlOut and self.sumLog ) :
                                self.sumLog.write( str(index+delta) + " : " + lines[index+delta])
                            log.debug(" " + str(index+delta) + ":" + lines[index+delta])
                    except IndexError:
                        pass
                    if (self.htmlOut and self.sumLog ) :
                        self.sumLog.write( '</a>\n')

        msg = "In total: "

        if (nErr == 0) :
            msg += "no errors, "
        else:
            if (nMkErr > 0) :
                msg += str(nMkErr) + " make errors, "
            msg += str(nErr) + " errors, "
            self.errFiles.append(htmlFileName)

        if ( nWarn == 0):
            msg += "no warnings"
        else:
            msg += str(nWarn) + " warnings"

        msg += " found in " + str(len(lines)) + " lines."

        if self.verbose > 0 :
            log.debug(msg)
        if (self.htmlOut and self.sumLog ) :
            self.sumLog.write( msg + "\n")
            self.sumLog.write( '</p>\n' )

        if prjAfsMatch :
            self.handleQmtestFile(file)

        return nMkErr, nErr, nWarn

    # --------------------------------------------------------------------------------

    def handleQmtestFile(self, file):
        log.debug("ignoring qmtest file:" + file)
        return 0,0

    # --------------------------------------------------------------------------------

    def checkFiles(self, fileList=[]) :

        import socket
        hostName = socket.gethostname().lower()

        import time
        date = time.ctime()
        if self.htmlOut and not self.sumLog :
            summaryFileName =  self.files.split("/")[9]+"-log.summary"
            self.sumLog = open(summaryFileName,'w')
            self.sumLog.write("<html>\n<head><title>Summary of logfiles</title></head>\n<body>\n<pre>\n")
            self.sumLog.write('<h2>Check of logfiles</h2>\n')
            self.sumLog.write( "<p>\n")
            self.sumLog.write( "Checking done on " + hostName + " at " + date )
            self.sumLog.write( "</p>\n")
            self.sumLog.write( "<p>\n")
            self.sumLog.write('<a href="#summary">Summary of checks</a>\n')
            self.sumLog.write( "</p>\n")
        totErr = 0
        totMkErr = 0
        totWarn = 0

        errFiles = []

        nFiles = 0
        nFilErr  = 0
        nFilWarn = 0
        if self.files :

            try:
                nMkErr, nErr, nWarn = self.checkLog(self.files)
            except IOError:
                sys.exit(-1)
            nFiles += 1
            totMkErr += nMkErr
            totErr += nErr
            totWarn += nWarn

            if nErr > 0 : nFilErr += 1
            if nWarn > 0 : nFilWarn += 1

        if self.verbose > 0 :
            print "\n================================================================================\n"

            if nFiles > 0 :
                print "Checked a total of ", nFiles, "log files."
                print "A total of ", totMkErr," make errors in ", nFilErr, 'files.'
                print "A total of ", totErr  , "errors in ", nFilErr, 'files.'
                print "A total of ", totWarn , "warnings in ", nFilWarn, 'files.'
                print "Files with errors: "
                for f in self.errFiles:
                    print "\t", f
                print
            else:
                print "No files found to check"
                print ""

        if self.htmlOut and self.sumLog :
            self.sumLog.write('<a name="summary"></a><hr />\n')
            self.sumLog.write("Checked a total of " + str(nFiles) + " log files.\n")
            self.sumLog.write("A total of " + str(totErr) +  " errors in " + str(nFilErr) + ' files.\n')
            self.sumLog.write("A total of " + str(totWarn) + " warnings in " + str(nFilWarn) + ' files.\n')
            self.sumLog.write("Files with errors: \n")

            self.sumLog.write("<table>\n")
            for f in self.errFiles:
                self.sumLog.write('<tr><td><a href="#' + f + '">' + f + '</a> </td></tr>\n')
            self.sumLog.write("</table>\n")

            self.sumLog.write("\n")
            self.sumLog.write("</pre>\n</body>\n</html>")
            self.sumLog.close()

        return

# --------------------------------------------------------------------------------

def usage():

    print sys.argv[0],"[--hmtl] <logFile> [<logFile> ...]"

    return

# ================================================================================

if __name__ == "__main__" :

    import getopt
    options = sys.argv[1:]
    try:
        opts, args = getopt.getopt(options, 'h',
                                   ['help','html','verbose=','topDir='])
    except getopt.GetoptError:
        usage()
        sys.exit(-2)

    html = None
    verb = 0
    slot = None
    top  = None

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit()

        if o in ('--html',):
            html = True
        if o in ('--verbose',):
            verb = a
        #if o in ('--slot',):
           # slot = a
        if o in ('--topDir',):
            top = a

    checker = LogChecker()

    if html : checker.setHtml(html)
    if top  : checker.topDir = top
    #checker.setSlot(slot)

    checker.verbose = verb
    checker.checkFiles(args)
