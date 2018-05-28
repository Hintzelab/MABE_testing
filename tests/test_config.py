import os, subprocess, pytest
from utils.helpers import this_repo_path, mabe, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, diff, ABdiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents
from utils.helpers import copyfileAndPermissions, movefile, movefileSwap

##
## all tests run IN ORDER OF DEFINITION and are run if they begin with 'test_'
## a test_fn() will fail on first failure and stop testing that test_fn, continuing on to the next test_fn.
## use `assert condition, "error message"` in a test_fn() to print a useful message on failure
##

@pytest.fixture ## indicates this is the constructor fn for all the test fns in this module
def ctx(): ## create a context for all the tests - you could potentially use this to pass an obj to all test fns
    if not ctx.ran:
        ## generate cfg (have to 'cd' there, because mabe '-s' ignores 'GLOBAL-outputDirectory' setting)
        ## and run mabe with defaults
        dirs = [dirname_baseline, dirname_testline]
        for eachdir in dirs: ## loop through each of baseline and testline and generate the files for later diffing
            cd(eachdir)
            runCmdAndSaveOutput( "./{exe} -s".format(exe=mabe), filename='screen-settings' ) ## save settings to file
            for eachfile in ["settings.cfg", "settings_organism.cfg", "settings_world.cfg"]: ## make a backup of the settings files
                copyfileAndPermissions(eachfile, eachfile+".bak")
            runCmdAndSaveOutput( "./{exe} -f settings*.cfg -s".format(exe=mabe), filename='screen-settings-reload' ) ## load and save settings to file
            for eachfile in ["settings.cfg", "settings_organism.cfg", "settings_world.cfg"]: ## make a backup of the settings files
                copyfileAndPermissions(eachfile, eachfile+".bak")
            ##
            ## MORE GENERATION OF FILES OR BEHAVIOR HERE
            ##
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

## testing consistency of screen output
def test_screen_settings(ctx):
    ABdiff('screen-settings')
def test_screen_settings_reload(ctx):
    ABdiff('screen-settings-reload')

## cfg from -s
def test_settings_cfg(ctx):
    ABdiff('settings.cfg')
def test_settings_organism_cfg(ctx):
    ABdiff('settings_organism.cfg')
def test_settings_world_cfg(ctx):
    ABdiff('settings_world.cfg')

## cfg from -f *fg -s
def test_settings_reload_cfg(ctx):
    diff(dirname_baseline+'settings.cfg.bak',dirname_baseline+'settings.cfg',outfilename='diff-baseline-settings.cfg')
    diff(dirname_testline+'settings.cfg.bak',dirname_testline+'settings.cfg',outfilename='diff-testline-settings.cfg')
def test_settings_reload_organism_cfg(ctx):
    diff(dirname_baseline+'settings_organism.cfg.bak',dirname_baseline+'settings_organism.cfg',outfilename='diff-baseline-settings_organism.cfg')
    diff(dirname_testline+'settings_organism.cfg.bak',dirname_testline+'settings_organism.cfg',outfilename='diff-testline-settings_organism.cfg')
def test_settings_reload_world_cfg(ctx):
    diff(dirname_baseline+'settings_world.cfg.bak',dirname_baseline+'settings_world.cfg',outfilename='diff-baseline-settings_world.cfg')
    diff(dirname_testline+'settings_world.cfg.bak',dirname_testline+'settings_world.cfg',outfilename='diff-testline-settings_world.cfg')
