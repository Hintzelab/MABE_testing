import os, subprocess, pytest
from utils.helpers import this_repo_path, exe_name, EXE, slash, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, diff, repoDiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents
from utils.helpers import thisTestName, repoDiffForDifference, repoDiffForSimilarity, diffForDifference, diffForSimilarity
from utils.helpers import copyfileAndPermissions

##
## all tests run IN ORDER OF DEFINITION and are run if they begin with 'test_'
## a test_fn() will fail on first failure and stop testing that test_fn, continuing on to the next test_fn.
## use `assert condition, "error message"` in a test_fn() to print a useful message on failure
##
generate_default_run_files_RAN = False
def generate_default_run_files():
    global generate_default_run_files_RAN
    if not generate_default_run_files_RAN:
        for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
            cd(this_repo_path)
            cd(eachdir)
            runCmdAndSaveOutput( "{exe}".format(exe=EXE), filename='screen-simulation')
            cd('..')
        generate_default_run_files_RAN = True

## testing consistency of screen output
def test_screen_help():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndSaveOutput( "{exe} -h".format(exe=EXE), filename='screen-help' )
        cd('..')
    repoDiffForSimilarity('screen-help')
def test_screen_run():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndSaveOutput( "{exe} -s".format(exe=EXE), filename='screen-settings' )
        cd('..')
    repoDiffForSimilarity('screen-settings')
def test_screen_simulation():
    generate_default_run_files()
    repoDiffForSimilarity('screen-simulation')
def test_screen_plf_generation():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndSaveOutput( "{exe} -l".format(exe=EXE), filename='screen-poploader' )
        cd('..')
    repoDiffForSimilarity('screen-poploader')

## cfg
def test_settings_cfg():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndHideOutput( "{exe} -s".format(exe=EXE))
        cd('..')
    repoDiffForSimilarity('settings.cfg')
def test_settings_organism_cfg():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndHideOutput( "{exe} -s".format(exe=EXE))
        cd('..')
    repoDiffForSimilarity('settings_organism.cfg')
def test_settings_world_cfg():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndHideOutput( "{exe} -s".format(exe=EXE))
        cd('..')
    repoDiffForSimilarity('settings_world.cfg')

## csv
def test_max_csv():
    generate_default_run_files()
    repoDiffForSimilarity('max.csv')
def test_pop_csv():
    generate_default_run_files()
    repoDiffForSimilarity('pop.csv')
def test_lod_data_csv():
    generate_default_run_files()
    repoDiffForSimilarity('LOD_data.csv')
def test_lod_organisms_csv():
    generate_default_run_files()
    repoDiffForSimilarity('LOD_organisms.csv')

## poploader
def test_plf():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndHideOutput( "{exe} -l".format(exe=EXE))
        cd('..')
    repoDiffForSimilarity('population_loader.plf')

## version output
def test_version_baseline():
    for eachdir in [dirname_baseline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndSaveOutput( "{exe} -v".format(exe=EXE), filename='screen-version' )
        cd('..')
    result = getFileContents(dirname_baseline+'screen-version')
    line1=result[0]
    assert len(line1) != 1, thisTestName()+": version information not found but should have been included in the build"

def test_version_testline():
    for eachdir in [dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndSaveOutput( "{exe} -v".format(exe=EXE), filename='screen-version' )
        cd('..')
    result = getFileContents(dirname_testline+'screen-version')
    line1=result[0]
    assert len(line1) != 1, thisTestName()+": version information not found but should have been included in the build"

def test_version_length():
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndSaveOutput( "{exe} -v".format(exe=EXE), filename='screen-version' )
        cd('..')
    baselineStr = ''.join(getFileContents(dirname_baseline+'screen-version'))
    testlineStr = ''.join(getFileContents(dirname_testline+'screen-version'))
    assert len(baselineStr) == len(testlineStr), thisTestName()+": version line length or commit hash length differs"
