# author: joryschossau (see github.com/joryschossau/contest)
# this is an untouched fork of `contest` from joryschossau

import argparse
import os
import sys
import shutil # rmtree, copyFile
import stat # file permissions (because shutil.copyFile does not retain permissions)
import subprocess # invoking command line module installation
#import psutil # cpu hw core count (not hyperthreading!)
import shlex
from utils import pyreq
pyreq.require("gitpython:git,pytest")
import git
import pytest

#from utils.helpers import copyfileAndPermissions, this_repo_path, mabe, dotSlashMabe, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import copyfileAndPermissions, this_repo_path, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndReturnOutput, runCmdAndSaveOutput, rmAllDiffFiles
from utils.helpers import rmfile, isGCCAvail
#from utils.helpers import exe_name, slash
from utils.helpers import is_repo_at_commit, get_branch_and_commit, is_local_repo
import utils.helpers

## TODO: add ability to pass arguments to mbuild

import platform
if platform.system() == 'Windows':
    import win32api
    import win32security
    import ntsecuritycon as con

def enableWriteFlagForGitRepoFiles(git_repo):
    if platform.system() == "Windows":
        packDir = os.path.join(git_repo,'.git','objects','pack')
        if os.path.isdir(packDir):
            for dpath, dnames, fnames in os.walk(packDir):
                if len(list(fnames)) > 0:
                    print("ERROR: The following files are locked. Please remove the repo '{}' yourself.".format(git_repo))
                    print("Running this script as admin on Windows may also fix the issue.")
                    for filename in fnames:
                        print("  ",os.path.join(dpath,filename))
                    exit(1)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('repo', type=str,        nargs='?', default=None)
    parser.add_argument('branch1', type=str,     nargs='?', default=None)
    parser.add_argument('branch2', type=str,     nargs='?', default=None)
    parser.add_argument('makeCommand', type=str, nargs='?', default=None)
    parser.add_argument('exeName', type=str,     nargs='?', default=None)
    parser.add_argument('-ls','--list', action='store_true', required = False, default = False, help='list all available tests found')
    parser.add_argument('-s','--subset', type=str, default='', help='test filter expression: "defaults and not settings"')
    args = parser.parse_args()
    noneTotal = 0
    if args.repo is None: noneTotal += 1
    if args.branch1 is None: noneTotal += 1
    if args.branch2 is None: noneTotal += 1
    if args.makeCommand is None: noneTotal += 1
    if args.exeName is None: noneTotal += 1
    if noneTotal > 0 and noneTotal < 5:
        print("Error: [repo branch1 branch2 makeCommand exeName] is an optional 5-argument group")
        parser.print_help(sys.stderr)
        exit(1)
    cd(this_repo_path)
    if args.list:
        #print("running pytest.main only performing test list")
        pytest.main(shlex.split("--color=yes -v --tb=line --collect-only"))
    else:
        print("running pytest.main")
        utils.helpers.exe_name = args.exeName
        utils.helpers.EXE = ".{}{}".format(utils.helpers.slash,utils.helpers.exe_name)
        compile_default_projects(args)
        subsetTests = '' if not len(args.subset) else '-k "'+args.subset+'"'
        pytest.main(shlex.split("--color=yes --tb=line -v {subset}".format(subset=subsetTests)))

def call_build(makeCommand):
    print("making target with '{}'".format(makeCommand))
    runCmdAndHideOutput(makeCommand)

def compile_default_projects(args):
    for eachRepo,eachBranch in zip([dirname_baseline, dirname_testline],[args.branch1,args.branch2]):
        branch,commit = get_branch_and_commit(eachBranch)
        print("{}: cloning repo '{}' and switching to {}:{}".format(eachRepo, args.repo, branch, commit))
        if is_repo_at_commit(eachRepo, branch, commit)==False: ## check if baseline repo is already set up, if not then make it
            enableWriteFlagForGitRepoFiles(eachRepo)
            shutil.rmtree(eachRepo,ignore_errors=True)
            repo = None ## initialize repo var based on local or remote invocation
            if is_local_repo(args.repo):
                oldrepo = git.Repo(args.repo)
                repo = oldrepo.clone(os.path.abspath(eachRepo), branch=branch)
            else:
                repo = git.Repo.clone_from(args.repo, eachRepo, branch=branch)
            repo.heads[0].set_commit(commit)
            repo.heads[0].checkout(force=True)
        cd(eachRepo)
        print("building {}".format(eachRepo), flush=True)
        call_build(args.makeCommand)
        cd("..")
    cd(this_repo_path)

if __name__ == '__main__':
    main()
