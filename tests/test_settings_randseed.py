import os, subprocess, pytest
from utils.helpers import this_repo_path, exe_name, EXE, slash, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, diff, repoDiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents
from utils.helpers import thisTestName, repoDiffForDifference, repoDiffForSimilarity, diffForDifference, diffForSimilarity

##
## all tests run IN ORDER OF DEFINITION and are run if they begin with 'test_'
## a test_fn() will fail on first failure and stop testing that test_fn, continuing on to the next test_fn.
## use `assert condition, "error message"` in a test_fn() to print a useful message on failure
##

runStr = EXE+" -p GLOBAL-randomSeed {seed} GLOBAL-updates 1 ARCHIVIST_LODWAP-terminateAfter 0"

## Test randomSeed -1 produces expected different output from 2 consecutive runs
@pytest.mark.parametrize('testDir',[dirname_baseline, dirname_testline], ids=['baseline','testline'])
def test_screen_randseed_random(testDir):
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        ## Create 2 files both with random seed
        runCmdAndSaveOutput(runStr.format(seed='-1'), filename='screen-settings-randseed-random-A' )
        runCmdAndSaveOutput(runStr.format(seed='-1'), filename='screen-settings-randseed-random-B' )
        cd('..')
    diffForDifference(testDir+'screen-settings-randseed-random-A',
                      testDir+'screen-settings-randseed-random-B',
                      outfilename="diff-"+testDir+"-screen-settings-randseed-random-A")

## Test randomSeed -1 between baseline and testline
def test_screen_randseed_random_inconsistency():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        ## Create 2 files both with random seed
        runCmdAndSaveOutput(runStr.format(seed='-1'), filename='screen-settings-randseed-random-A' )
        runCmdAndSaveOutput(runStr.format(seed='-1'), filename='screen-settings-randseed-random-B' )
        cd('..')
    repoDiffForDifference('screen-settings-randseed-random-A')

## Test randomSeed 32 produces expected different output from 2 consecutive runs
@pytest.mark.parametrize('testDir',[dirname_baseline, dirname_testline], ids=['baseline','testline'])
def test_screen_randseed_nonrandom_consecutive_runs(testDir):
    #for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
    cd(this_repo_path)
    cd(testDir)
    ## Create 2 files both with random seed
    runCmdAndSaveOutput(runStr.format(seed='32'), filename='screen-settings-randseed-nonrandom-consecutive-runs-A' )
    runCmdAndSaveOutput(runStr.format(seed='32'), filename='screen-settings-randseed-nonrandom-consecutive-runs-B' )
    cd('..')
    diffForSimilarity(os.path.join(testDir,'screen-settings-randseed-nonrandom-consecutive-runs-A'),
                      os.path.join(testDir,'screen-settings-randseed-nonrandom-consecutive-runs-B'),
                      outfilename="diff-"+testDir+"-screen-settings-randseed-nonrandom-consecutive-runs-A")

## Test randomSeed 32 between baseline and testline
def test_screen_randseed_nonrandom_consistency():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        ## Create 2 files both with random seed
        runCmdAndSaveOutput(runStr.format(seed='32'), filename='screen-settings-randseed-nonrandom-consistency' )
        cd('..')
    repoDiffForSimilarity('screen-settings-randseed-nonrandom-consistency')
