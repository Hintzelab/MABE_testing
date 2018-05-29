import os, subprocess, pytest
from utils.helpers import this_repo_path, mabe, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, diff, ABdiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents
from utils.helpers import thisTestName

##
## all tests run IN ORDER OF DEFINITION and are run if they begin with 'test_'
## a test_fn() will fail on first failure and stop testing that test_fn, continuing on to the next test_fn.
## use `assert condition, "error message"` in a test_fn() to print a useful message on failure
##

@pytest.fixture ## indicates this is the constructor fn for all the test fns in this module
def ctx(): ## create a context for all the tests - you could potentially use this to pass an obj to all test fns
    if not ctx.ran: ## prevents reinit before each and every test fn in this module
        ## generate cfg (have to 'cd' there, because mabe '-s' ignores 'GLOBAL-outputDirectory' setting)
        ## and run mabe with defaults
        runStr = "./"+mabe+" -p GLOBAL-randomSeed {seed} GLOBAL-updates 1 ARCHIVIST_LODWAP-terminateAfter 0"
        dirs = [dirname_baseline, dirname_testline]
        for eachdir in dirs: ## loop through each of baseline and testline and generate the files for later diffing
            cd(this_repo_path)
            cd(eachdir)
            ## Create 2 files both with random seed
            runCmdAndSaveOutput(runStr.format(seed='-1'), filename='screen-settings-randseed-random-A' )
            runCmdAndSaveOutput(runStr.format(seed='-1'), filename='screen-settings-randseed-random-B' )
            ## Create 2 files both with identical seed
            runCmdAndSaveOutput(runStr.format(seed='101'), filename='screen-settings-randseed-nonrandom-A' )
            runCmdAndSaveOutput(runStr.format(seed='101'), filename='screen-settings-randseed-nonrandom-B' )
            cd('..') ## could also have done cd(this_repo_path)
        ## FYI, could have done it the following way if we were up one dir in mabe_testing
        #runCmdAndSaveOutput( "{exe} -p GLOBAL-outputDirectory {path}".format(exe=path_baseline_exe, path=dirname_baseline), filename=dirname_baseline+'screen-simulation' )
        ctx.ran = True

    yield None ## could have actually passed a context object here to all the test fns
    ##
    ## teardown happens after the last test in the module finishes
    ##
    return
ctx.ran = False

## Test randomSeed -1 produces expected different output from 2 consecutive runs
@pytest.mark.parametrize('testDir',[dirname_baseline, dirname_testline], ids=['baseline','testline'])
def test_screen_randseed_random(ctx,testDir):
    diff(testDir+'screen-settings-randseed-random-A',
         testDir+'screen-settings-randseed-random-B',
         outfilename="diff-"+testDir+"-screen-settings-randseed-random-A",
         expectDifferent=True)

## Test randomSeed -1 between baseline and testline
def test_screen_randseed_random_inconsistency(ctx):
    ABdiff('screen-settings-randseed-random-A', expectDifferent=True)

## Test randomSeed -1 produces expected different output from 2 consecutive runs
@pytest.mark.parametrize('testDir',[dirname_baseline, dirname_testline], ids=['baseline','testline'])
def test_screen_randseed_nonrandom(ctx,testDir):
    diff(testDir+'screen-settings-randseed-nonrandom-A',
         testDir+'screen-settings-randseed-nonrandom-B',
         outfilename="diff-"+testDir+"-screen-settings-randseed-nonrandom-A")

## Test randomSeed -1 between baseline and testline
def test_screen_randseed_nonrandom_consistency(ctx):
    ABdiff('screen-settings-randseed-nonrandom-A')
