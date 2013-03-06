##########################################################
## stolen and (slighty) adapted from:
##  http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/65203
##

import os

if os.name == 'nt':

   try:
        import win32con
        import win32file
        import pywintypes
        import_failed = False
        LOCK_EX = win32con.LOCKFILE_EXCLUSIVE_LOCK
        LOCK_SH = 0 # the default
        LOCK_NB = win32con.LOCKFILE_FAIL_IMMEDIATELY
        # is there any reason not to reuse the following structure?
        __overlapped = pywintypes.OVERLAPPED()
        hexCst = -0x10000
   except:
        import_failed = True
        LOCK_EX = None
        LOCK_SH = None
        LOCK_NB = None

elif os.name == 'posix':
        import fcntl
        LOCK_EX = fcntl.LOCK_EX
        LOCK_SH = fcntl.LOCK_SH
        LOCK_NB = fcntl.LOCK_NB
else:
        raise RuntimeError("Locker only defined for nt and posix platforms")

if os.name == 'nt':
    if import_failed :
        def lock(file, flags) : pass
        def unlock(file) : pass
    else :
        def lock(file, flags):
                hfile = win32file._get_osfhandle(file.fileno())
                win32file.LockFileEx(hfile, flags, 0, hexCst, __overlapped)

        def unlock(file):
                hfile = win32file._get_osfhandle(file.fileno())
                win32file.UnlockFileEx(hfile, 0, hexCst, __overlapped)

elif os.name =='posix':
        def lock(file, flags):
                fcntl.flock(file.fileno(), flags)

        def unlock(file):
                fcntl.flock(file.fileno(), fcntl.LOCK_UN)
