
import argparse
import os
import sys
import shutil # rmtree
import subprocess # invoking command line module installation
import psutil
from utils import pyreq
pyreq.require("pygit:git,pytest")
import git
import pytest

from utils.helpers import test_repo_name, product, dir_base, dir_test, path_base, path_test

## TODO: add ability to pass arguments to mbuild

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c','--compare', default = 'master', help='branch or commit hash to compare.')
    parser.add_argument('-f','--force', action='store_true', required = False, default = False, help='force new download and compile')
    args = parser.parse_args()
    compile_default_projects(args)
    pytest.main(["-s","--color=yes"]) ## invoke pytest (pass a filename here to run test on specific file)

def compile_default_projects(args):
    if not os.path.isfile(os.path.join(dir_base,product)) or args.force:
        print("clone new",args.compare,"as baseline", flush=True)
        shutil.rmtree(dir_base)
        repo = git.Repo.clone_from("https://github.com/hintzelab/mabe", dir_base, branch=args.compare)
        os.chdir(dir_base)
        print("building", flush=True)
        subprocess.run("python pythonTools/mbuild.py -p"+str(psutil.cpu_count(logical=False)), shell=True, check=True)
        os.chdir("..")
    if not os.path.isfile(os.path.join('..',product)):
        os.chdir("..")
        print("building", flush=True)
        subprocess.run("python pythonTools/mbuild.py -p"+str(psutil.cpu_count(logical=False)), shell=True, check=True)
        os.chdir(test_repo_name)
    os.makedirs(dir_test, exist_ok=True)
    shutil.copyfile(os.path.join('..',product), path_test)

if __name__ == '__main__':
    main()
