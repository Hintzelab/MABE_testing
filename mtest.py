
import argparse
import os
import sys
import shutil # rmtree
import subprocess # invoking command line module installation
import psutil
from utils import pyreq
pyreq.require("gitpython:git,pytest")
import git
import pytest

from utils.helpers import test_repo_name, product, basename_base, basename_test, path_base_exe, path_test_exe, cmd

## TODO: add ability to pass arguments to mbuild

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('branch', nargs='?', default='master')
    parser.add_argument('commit', nargs='?', default='HEAD')
    parser.add_argument('-f','--force', action='store_true', required = False, default = False, help='force new download and compile')
    args = parser.parse_args()
    compile_default_projects(args)
    pytest.main(["-s","--color=yes"]) ## invoke pytest (pass a filename here to run test on specific file)

def compile_default_projects(args):
    if not os.path.isfile(path_base_exe) or args.force:
        print("clone new",args.branch,"at",args.commit,"as baseline", flush=True)
        shutil.rmtree(basename_base,ignore_errors=True)
        repo = git.Repo.clone_from("https://github.com/hintzelab/mabe", basename_base, branch=args.branch)
        revision = repo.create_head('revision',args.commit)
        repo.heads.revision.checkout()
        os.chdir(basename_base)
        print("building", flush=True)
        subprocess.run(cmd("python pythonTools/mbuild.py -p{cores}".format(cores=str(psutil.cpu_count(logical=False)))), shell=True, check=True)
        os.chdir("..")
    if not os.path.isfile(os.path.join('..',product)):
        os.chdir("..")
        print("building", flush=True)
        subprocess.run(cmd("python pythonTools/mbuild.py -p{cores}".format(cores=str(psutil.cpu_count(logical=False)))), shell=True, check=True)
        os.chdir(test_repo_name)
    os.makedirs(basename_test, exist_ok=True)
    shutil.copyfile(os.path.join('..',product), path_test_exe)

if __name__ == '__main__':
    main()
