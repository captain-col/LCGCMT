import string,os,sys

def splitPath(path):
  l2     = []
 
  l1 = string.split(path,'/')
  for x in l1 : l2 += string.split(x,'\\')

  if not l2[-1] : l2 = l2[:-1]

  return l2


def mkRelDir(cur, dest):
# """
# Create a relative path from the current directory (cur) to the
# destination directory (dest). The path will be split by both
# the linux and windows directory separators and returned with
# joined by the current platform specific separator.
# """
  curl = splitPath(cur)
  desl = splitPath(dest)
  lcurl = len(curl)
  ldesl = len(desl)
  lcomm = 0

  for x in range(min(lcurl,ldesl)) :
    if curl[x] == desl[x] : lcomm += 1
    else  : break

  return string.join([os.pardir]*(lcurl-lcomm)+desl[lcomm:],os.sep)


if __name__ == '__main__' :

  print mkRelDir(sys.argv[1], sys.argv[2])
  
