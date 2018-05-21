import platform
import os
from utils import pyreq
pyreq.require('difflib')
import difflib

test_repo_name = os.path.basename(os.path.dirname(os.path.realpath(__file__)))

if platform.system() == 'Windows':
    product = 'mabe.exe'
else:
    product = 'mabe'

## TODO: add ability to pass arguments to mbuild

basename_base = 'baseline' ## dirname for old baseline build (used to compare new code)
basename_test = 'testline' ## dirname for new build to compare with old baseline

path_base_exe = os.path.join(basename_base,product)
path_test_exe = os.path.join(basename_test,product)

def ABdiff(filename): ## helper fn diffing 2 files with the same name: "diff base/filename test/filename
    with open(os.path.join(basename_base,filename)) as a, open(os.path.join(basename_test,filename)) as b:
        difflines = list(difflib.context_diff(a.readlines(),b.readlines()))
        numDiffLines = len(difflines)
        print(''.join(difflines))
        assert numDiffLines == 0, filename+" differs"

def cmd(str): ## return list split on space - useful to pass a command to subprocess.run()
    return str.split()
