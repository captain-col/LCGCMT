import os, cmt, checkPackageXml


class checkAllPackageXml:

  def __init__(self):

    self.cmt = cmt.CMT()
    self.builderPackages = []

  def getBuilderPackageList(self):
    for pkg in self.cmt.uses:
      pl = pkg.split()
      if 'LCG_Builders' in pl:
        if pl[1][:4] != 'LCG_':
          self.builderPackages.append(pl[-1][1:-1]+pl[3]+os.sep+pl[1])
    

  def checkAll(self):
    self.getBuilderPackageList()
    for x in self.builderPackages:
      os.chdir(x+os.sep+'cmt')
      cpx = checkPackageXml.checkPackageXml()
      cpx.check()

if __name__ == '__main__':

  capx = checkAllPackageXml()
  capx.checkAll()
