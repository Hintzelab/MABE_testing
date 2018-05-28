
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

from utils.helpers import copyfileAndPermissions, this_repo_path, mabe, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, runCmdAndShowOutput, runCmdAndReturnOutput, runCmdAndSaveOutput, rmAllDiffFiles
from utils.helpers import rmfile

## TODO: add ability to pass arguments to mbuild

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('branch', nargs='?', default='master')
    parser.add_argument('commit', nargs='?', default='HEAD')
    parser.add_argument('-f','--force', action='store_true', required = False, default = False, help='force new download and compile')
    parser.add_argument('-s','--subset', type=str, default='', help='test filter expression: "defaults and not settings"')
    args = parser.parse_args()
    cd(this_repo_path)
    compile_default_projects(args)
    subsetTests = '' if not len(args.subset) else '-k "'+args.subset+'"'
    rmAllDiffFiles()
    pytest.main(shlex.split("-s --color=yes -v --tb=line {subset}".format(subset=subsetTests))) ## invoke pytest (pass a filename here to run test on specific file)

def writeDefaultBuildOptions():
    content = """% World
  * Test
% Genome
  * Circular
% Brain
  * CGP
% Optimizer
  * Simple
% Archivist
  * LODwAP"""
    with open("buildOptions.txt",'w') as bo:
        bo.write(content)

def compile_default_projects(args):
    if not os.path.isfile(path_baseline_exe) or args.force:
        print("clone new",args.branch,"at",args.commit,"as baseline", flush=True)
        shutil.rmtree(dirname_baseline,ignore_errors=True)
        repo = git.Repo.clone_from("https://github.com/hintzelab/mabe", dirname_baseline, branch=args.branch)
        revision = repo.create_head('revision',args.commit)
        repo.heads.revision.checkout()
        cd(dirname_baseline)
        print("building baseline", flush=True)
        rmfile("buildOptions.txt") ## remove buildOptions so we can regenerate it
        writeDefaultBuildOptions()
        subprocess.run("python pythonTools/mbuild.py -i", shell=True, check=True) ## regenerate buildOptions with ALL available modules
        subprocess.run("python pythonTools/mbuild.py -p{cores}".format(cores=str(psutil.cpu_count(logical=False))), shell=True, check=True)
        cd("..")
    if not os.path.isfile(os.path.join('..',mabe)):
        cd("..")
        print("building testline", flush=True)
        rmfile("buildOptions.txt") ## remove buildOptions so we can regenerate it
        writeDefaultBuildOptions()
        subprocess.run("python pythonTools/mbuild.py -i", shell=True, check=True) ## regenerate buildOptions with ALL available modules
        subprocess.run("python pythonTools/mbuild.py -p{cores}".format(cores=str(psutil.cpu_count(logical=False))), shell=True, check=True)
        cd(this_repo_path)
    os.makedirs(dirname_testline, exist_ok=True)
    copyfileAndPermissions(os.path.join('..',mabe), path_testline_exe)

if __name__ == '__main__':
    main()
