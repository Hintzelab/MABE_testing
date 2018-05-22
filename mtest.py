
import argparse
import os
import sys
import shutil # rmtree, copyFile
import stat # file permissions (because shutil.copyFile does not retain permissions)
import subprocess # invoking command line module installation
import psutil # cpu hw core count (not hyperthreading!)
import shlex
from utils import pyreq
pyreq.require("gitpython:git,pytest")
import git
import pytest

from utils.helpers import copyfileAndPermissions, this_repo_name, product, basename_base, basename_test, path_base_exe, path_test_exe

## TODO: add ability to pass arguments to mbuild

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('branch', nargs='?', default='master')
    parser.add_argument('commit', nargs='?', default='HEAD')
    parser.add_argument('-f','--force', action='store_true', required = False, default = False, help='force new download and compile')
    parser.add_argument('-s','--subset', type=str, default='', help='test filter expression: "defaults and not settings"')
    args = parser.parse_args()
    compile_default_projects(args)
    subsetTests = '' if not len(args.subset) else '-k "'+args.subset+'"'
    pytest.main(shlex.split("-s --color=yes -v --tb=line {subset}".format(subset=subsetTests))) ## invoke pytest (pass a filename here to run test on specific file)

def compile_default_projects(args):
    if not os.path.isfile(path_base_exe) or args.force:
        print("clone new",args.branch,"at",args.commit,"as baseline", flush=True)
        shutil.rmtree(basename_base,ignore_errors=True)
        repo = git.Repo.clone_from("https://github.com/hintzelab/mabe", basename_base, branch=args.branch)
        revision = repo.create_head('revision',args.commit)
        repo.heads.revision.checkout()
        os.chdir(basename_base)
        print("building baseline", flush=True)
        subprocess.run("python pythonTools/mbuild.py -p{cores}".format(cores=str(psutil.cpu_count(logical=False))), shell=True, check=True)
        os.chdir("..")
    if not os.path.isfile(os.path.join('..',product)):
        os.chdir("..")
        print("building testline", flush=True)
        subprocess.run("python pythonTools/mbuild.py -p{cores}".format(cores=str(psutil.cpu_count(logical=False))), shell=True, check=True)
        os.chdir(this_repo_name)
    os.makedirs(basename_test, exist_ok=True)
    copyfileAndPermissions(os.path.join('..',product), path_test_exe)

if __name__ == '__main__':
    main()
