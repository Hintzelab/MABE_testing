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

dir_base = 'baseline' ## dirname for old baseline build (used to compare new code)
dir_test = 'testline' ## dirname for new build to compare with old baseline

path_base = os.path.join(dir_base,product)
path_test = os.path.join(dir_test,product)

def ABdiff(filename): ## helper fn
    with open(os.path.join(dir_base,filename)) as a, open(os.path.join(dir_test,filename)) as b:
        difflines = list(difflib.context_diff(a.readlines(),b.readlines()))
        numDiffLines = len(difflines)
        print(''.join(difflines))
        assert numDiffLines == 0, filename+" differs"
