import platform, subprocess, os, glob, inspect
import shutil, stat ## for file copy w/ permissions
import re ## for re.sub
import platform ## system identification
from utils import pyreq
pyreq.require('difflib,gitpython:git,pytest')
import difflib
import pytest

if platform.system() == 'Windows':
    import win32api
    import win32security
    import ntsecuritycon as con

#this_repo_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
this_repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if platform.system() == 'Windows': ## mtest can still be run on windows if you have the exes already compiled in the right places (baseline/ and testline/)
    mabe = 'mabe.exe'
    dotSlashMabe = mabe
else:
    mabe = 'mabe'
    dotSlashMabe = './mabe'

## TODO: add ability to pass arguments to mbuild

dirname_baseline = 'baseline/' ## dirname for old baseline build (used to compare new code)
dirname_testline = 'testline/' ## dirname for new build to compare with old baseline

path_baseline_exe = os.path.join(dirname_baseline,mabe)
path_testline_exe = os.path.join(dirname_testline,mabe)

def isGCCAvail():
    proc = subprocess.Popen("which c++", shell=True, stdout=subprocess.PIPE, bufsize=1)
    out,err = proc.communicate()
    gccFound = False if out.decode()[0:6] == "which:" else True
    proc = subprocess.Popen("which c++.exe", shell=True, stdout=subprocess.PIPE, bufsize=1)
    out,err = proc.communicate()
    gccFound = gccFound if out.decode()[0:6] == "which:" else True
    return gccFound

def thisTestName(ignoreStackDepth=1):
    return inspect.stack()[ignoreStackDepth][3]

def buildMessageErrorExpectedWithArgs(*args):
    return thisTestName(ignoreStackDepth=2)+str(args)+" was supposed to error."

def cd(path): ## alias for os.chdir, but also platforms the path
    os.chdir( os.path.abspath(path) )

def copyfileAndPermissions(source,destination): ## uses shutil, stat, and os to copy preserving permissions
    shutil.copyfile(source, destination)
    if platform.system() == 'Windows':
        everyone, domain, type = win32security.LookupAccountName ("", "Everyone")
        admins, domain, type = win32security.LookupAccountName ("", "Administrators")
        user, domain, type = win32security.LookupAccountName ("", win32api.GetUserName ())
        sd = win32security.GetFileSecurity (destination, win32security.DACL_SECURITY_INFORMATION)
        dacl = win32security.ACL ()
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.GENERIC_EXECUTE, everyone)
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_GENERIC_READ | con.FILE_GENERIC_WRITE | con.GENERIC_EXECUTE, user)
        dacl.AddAccessAllowedAce (win32security.ACL_REVISION, con.FILE_ALL_ACCESS, admins)
        sd.SetSecurityDescriptorDacl (1, dacl, 0)
        win32security.SetFileSecurity (destination, win32security.DACL_SECURITY_INFORMATION, sd)
    else:
        runCmdAndHideOutput('chmod 755 '+destination ) ## my wonderful hack O_o
        ## the below efforts don't work on the HPCC for some reason...
        #st = os.stat(source)
        #os.chown(destination, 0o755)
        #os.chown(destination, 0o755, 0o20)
        #os.chown(destination, st[stat.ST_UID], st[stat.ST_GID])
        #os.chown(destination, st.st_mode, st[stat.ST_UID])
        #os.chown(destination, st[stat.ST_UID], st[stat.ST_GID])
        #os.chown(destination, st.st_mode | stat.S_IRWXU, stat.S_IRGRP)

def movefile(source,destination): ## alias for shutil.move
    shutil.move(source,destination)

def movefileSwap(file1,file2): ## swaps two files
    file1 = os.path.abspath(file1)
    file2 = os.path.abspath(file2)
    shutil.move(file1,'.tempforfilemove')
    shutil.move(file2,file1)
    shutil.move('.tempforfilemove',file2)

def rmfile(filename): ## alias for os.remove()
    os.remove(os.path.abspath(filename))

def rmAllDiffFiles(): ## removes all diff files
    files = glob.glob(os.path.join(this_repo_path,'diff-*'))
    for eachfile in files:
        os.remove(eachfile)

def getFileContents(filename): ## helper fn to load a file and return contents as list
    contents=[]
    with open(os.path.abspath(filename)) as infile:
        contents=infile.readlines()
    return contents

def diff(file1, file2, outfilename, expectDifferent=False, ignoreStackDepth=2): ## helper fn diffing 2 arbitrary files
    outfilename = re.sub('[/]','',outfilename) ## remove possible trailing 
    with open(os.path.abspath(file1)) as a, open(os.path.abspath(file2)) as b:
        contentsA = a.readlines()
        contentsB = b.readlines()
        difflines = list(difflib.ndiff(contentsA, contentsB)) ## perform diff and return human-readable format
        difflines_machinereadable = list(difflib.context_diff(contentsA, contentsB)) ## perform diff and return machine-readable format
        numDiffLines = len(difflines_machinereadable)
        numDiffs = [line[0] in ['+','-'] for line in difflines].count(True) ## counts lines that begin with + or -
        if numDiffLines != 0:
            with open(os.path.abspath(outfilename), 'w') as outfile:
                outfile.write(''.join(difflines))
        if expectDifferent:
            assert numDiffLines != 0, thisTestName(ignoreStackDepth=ignoreStackDepth)+": {name1} and {name2} should be different)".format(name1=file1, name2=file2)
        else:
            assert numDiffLines == 0, thisTestName(ignoreStackDepth=ignoreStackDepth)+": {ndiffs} changes (see diff-{name})".format(a=file1, b=file2, ndiffs=str(numDiffs), name=outfilename )

def diffForDifference(file1, file2, outfilename):
    diff(file1, file2, outfilename, expectDifferent=True, ignoreStackDepth=3)

def diffForSimilarity(file1, file2, outfilename):
    diff(file1, file2, outfilename, expectDifferent=False, ignoreStackDepth=3)

def repoDiff(filename, expectDifferent=False, ignoreStackDepth=2): ## helper fn diffing 2 files with the same name: "diff baseline/filename testline/filename"
    with open(os.path.join(dirname_baseline,filename)) as a, open(os.path.join(dirname_testline,filename)) as b:
        contentsA = a.readlines()
        contentsB = b.readlines()
        difflines = list(difflib.ndiff(contentsA, contentsB)) ## perform diff and return human-readable format
        difflines_machinereadable = list(difflib.context_diff(contentsA, contentsB)) ## perform diff and return machine-readable format
        numDiffLines = len(difflines_machinereadable)
        numDiffs = [line[0] in ['+','-'] for line in difflines].count(True) ## counts lines that begin with + or -
        if numDiffLines != 0:
            outfilename = os.path.join(this_repo_path,'diff-'+filename)
            with open(outfilename, 'w') as outfile:
                outfile.write(''.join(difflines))
        if expectDifferent:
            assert numDiffLines != 0, thisTestName(ignoreStackDepth=ignoreStackDepth)+": Expected differences in {name} between baseline & testline.".format( name=filename )
        else:
            assert numDiffLines == 0, thisTestName(ignoreStackDepth=ignoreStackDepth)+": {ndiffs} changes (see diff-{name})".format( ndiffs=str(numDiffs), name=filename )

def repoDiffForDifference(filename):
    repoDiff(filename, expectDifferent=True, ignoreStackDepth=3)

def repoDiffForSimilarity(filename):
    repoDiff(filename, expectDifferent=False, ignoreStackDepth=3)

def runCmdAndHideOutput(string):
    proc = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE, bufsize=1)
    out,err = proc.communicate()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode,string)#thisTestName(ignoreStackDepth))#+" crash: '{args}'".format(args=string))
def runCmdAndReturnOutput(string):
    proc = subprocess.Popen(string, shell=True, stdout=subprocess.PIPE, bufsize=1)
    out,err = proc.communicate()
    if proc.returncode != 0:
        raise subprocess.CalledProcessError(proc.returncode,string)
    if err is None:
        return out.decode()
    else:
        return out.decode()+err.decode()
def runCmdAndShowOutput(string):
    print( runCmdAndReturnOutput(string), flush=True)
def runCmdAndSaveOutput(string, filename): ## calls subprocess.run(str, shell=True, check=True) and saves result to filename
    output = runCmdAndReturnOutput(string)
    platformedPath = os.path.abspath(filename) ## converts possible "adir/afile.txt" to "C:\the\whole\path\adir\afile.txt" if needed
    with open(platformedPath, 'w') as outfile:
        outfile.write(output)
