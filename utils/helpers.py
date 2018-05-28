import platform, subprocess, os, glob
import shutil, stat # for file copy w/ permissions
from utils import pyreq
pyreq.require('difflib')
import difflib

#this_repo_name = os.path.basename(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
this_repo_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

if platform.system() == 'Windows':
    product = 'mabe.exe'
else:
    product = 'mabe'

## TODO: add ability to pass arguments to mbuild

basename_base = 'baseline/' ## dirname for old baseline build (used to compare new code)
basename_test = 'testline/' ## dirname for new build to compare with old baseline

path_base_exe = os.path.join(basename_base,product)
path_test_exe = os.path.join(basename_test,product)

def copyfileAndPermissions(source,destination): ## uses shutil, stat, and os to copy preserving permissions
    shutil.copyfile(source, destination)
    st = os.stat(source)
    os.chown(destination, st[stat.ST_UID], st[stat.ST_GID])
    os.chmod(destination, st[stat.ST_MODE])

def rmAllDiffFiles(): ## removes all diff files
    files = glob.glob(os.path.join(this_repo_path,'diff-*'))
    for eachfile in files:
        os.remove(eachfile)

def ABdiff(filename): ## helper fn diffing 2 files with the same name: "diff base/filename test/filename
    with open(os.path.join(basename_base,filename)) as a, open(os.path.join(basename_test,filename)) as b:
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
