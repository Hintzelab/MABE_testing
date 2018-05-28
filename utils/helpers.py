import platform, subprocess, os, glob
import shutil, stat # for file copy w/ permissions
from utils import pyreq
pyreq.require('difflib')
import difflib

#this_repo_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
this_repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if platform.system() == 'Windows': ## mtest can still be run on windows if you have the exes already compiled in the right places (baseline/ and testline/)
    mabe = 'mabe.exe'
else:
    mabe = 'mabe'

## TODO: add ability to pass arguments to mbuild

dirname_baseline = 'baseline/' ## dirname for old baseline build (used to compare new code)
dirname_testline = 'testline/' ## dirname for new build to compare with old baseline

path_baseline_exe = os.path.join(dirname_baseline,mabe)
path_testline_exe = os.path.join(dirname_testline,mabe)

def cd(path): ## alias for os.chdir, but also platforms the path
    os.chdir( os.path.abspath(path) )

def copyfileAndPermissions(source,destination): ## uses shutil, stat, and os to copy preserving permissions
    shutil.copyfile(source, destination)
    st = os.stat(source)
    os.chown(destination, st[stat.ST_UID], st[stat.ST_GID])
    os.chmod(destination, st[stat.ST_MODE])

def movefile(source,destination): ## alias for shutil.move
    shutil.move(source,destination)
def movefileSwap(file1,file2): ## swaps two files
    file1 = os.path.abspath(file1)
    file2 = os.path.abspath(file2)
    shutil.move(file1,'.tempforfilemove')
    shutil.move(file2,file1)
    shutil.move('.tempforfilemove',file2)

def rmAllDiffFiles(): ## removes all diff files
    files = glob.glob(os.path.join(this_repo_path,'diff-*'))
    for eachfile in files:
        os.remove(eachfile)

def getFileContents(filename): ## helper fn to load a file and return contents as list
    contents=[]
    with open(os.path.abspath(filename)) as infile:
        contents=infile.readlines()
    return contents

def diff(file1, file2, outfilename): ## helper fn diffing 2 arbitrary files
    with open(os.path.abspath(file1)) as a, open(os.path.abspath(file1)) as b:
        contentsA = a.readlines()
        contentsB = b.readlines()
        difflines = list(difflib.ndiff(contentsA, contentsB)) ## perform diff and return human-readable format
        difflines_machinereadable = list(difflib.context_diff(contentsA, contentsB)) ## perform diff and return machine-readable format
        numDiffLines = len(difflines_machinereadable)
        numDiffs = [line[0] in ['+','-'] for line in difflines].count(True) ## counts lines that begin with + or -
        if numDiffLines != 0:
            outfilename
            with open(os.path.abspath(outfilename), 'w') as outfile:
                outfile.write(''.join(difflines))
        assert numDiffLines == 0, "{a} and {b} differ with {ndiffs} differences. see diff-{name}".format(a=file1, b=file2, ndiffs=str(numDiffs), name=filename )

def ABdiff(filename): ## helper fn diffing 2 files with the same name: "diff baseline/filename testline/filename"
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
        assert numDiffLines == 0, filename+" differs with {ndiffs} differences. see diff-{name}".format( ndiffs=str(numDiffs), name=filename )

def runCmdAndHideOutput(str): ## calls subprocess.run(str,stdout=subprocess.DEVNULL, shell=True)
    subprocess.run(str, stdout=subprocess.DEVNULL, shell=True)
def runCmdAndReturnOutput(str): ## calls subprocess.run(str, shell=True, check=True) and returns result
    resultObj = subprocess.run(str, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return resultObj.stdout.decode()+'\n'+resultObj.stderr.decode()
def runCmdAndShowOutput(str): ## calls subprocess.run(str, shell=True, check=True)
    print( runCmdAndReturnOutput(str), flush=True)
def runCmdAndSaveOutput(str, filename): ## calls subprocess.run(str, shell=True, check=True) and saves result to filename
    output = runCmdAndReturnOutput(str)
    platformedPath = os.path.abspath(filename) ## converts possible "adir/afile.txt" to "C:\the\whole\path\adir\afile.txt" if needed
    with open(platformedPath, 'w') as outfile:
        outfile.write(output)
