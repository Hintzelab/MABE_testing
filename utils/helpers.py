import platform, subprocess, os
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

basename_base = 'baseline' ## dirname for old baseline build (used to compare new code)
basename_test = 'testline' ## dirname for new build to compare with old baseline

path_base_exe = os.path.join(basename_base,product)
path_test_exe = os.path.join(basename_test,product)

def copyfileAndPermissions(source,destination): ## uses shutil, stat, and os to copy w/ permissions
    shutil.copyfile(source, destination)
    st = os.stat(source)
    os.chown(destination, st[stat.ST_UID], st[stat.ST_GID])
    os.chmod(destination, st[stat.ST_MODE])

def ABdiff(filename): ## helper fn diffing 2 files with the same name: "diff base/filename test/filename
    with open(os.path.join(basename_base,filename)) as a, open(os.path.join(basename_test,filename)) as b:
        difflines = list(difflib.context_diff(a.readlines(),b.readlines()))
        numDiffLines = len(difflines)
        print(''.join(difflines))
        assert numDiffLines == 0, filename+" differs"

def runCmdAndHideOutput(str): ## calls subprocess.run(str,stdout=subprocess.DEVNULL, shell=True)
    subprocess.run(str, stdout=subprocess.DEVNULL, shell=True)
def runCmdAndShowOutput(str): ## calls subprocess.run(str, shell=True, check=True)
    print( subprocess.run(str, shell=True, check=True) ,flush=True)
