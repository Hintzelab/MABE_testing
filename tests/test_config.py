import os, subprocess, pytest
from utils.helpers import this_repo_path, exe_name, EXE, slash, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, diff, repoDiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents
from utils.helpers import copyfileAndPermissions, movefile, movefileSwap
from utils.helpers import thisTestName, repoDiffForDifference, repoDiffForSimilarity, diffForDifference, diffForSimilarity

##
## all tests run IN ORDER OF DEFINITION and are run if they begin with 'test_'
## a test_fn() will fail on first failure and stop testing that test_fn, continuing on to the next test_fn.
## use `assert condition, "error message"` in a test_fn() to print a useful message on failure
##

generate_default_cfg_files_RAN = False
def generate_default_cfg_files():
    global generate_default_cfg_files_RAN
    if not generate_default_cfg_files_RAN:
        for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
            cd(this_repo_path)
            cd(eachdir)
            runStr = EXE+" -s"
            runCmdAndSaveOutput( runStr, filename='screen-settings' ) ## save settings to file
            for eachfile in ["settings.cfg", "settings_organism.cfg", "settings_world.cfg"]: ## make a backup of the settings files
                copyfileAndPermissions(eachfile, eachfile+".bak")
            runStr = EXE+" -f settings*.cfg -s"
            runCmdAndSaveOutput( runStr, filename='screen-settings-reload' ) ## load and save settings to file
            for eachfile in ["settings.cfg", "settings_organism.cfg", "settings_world.cfg"]: ## make a backup of the settings files
                copyfileAndPermissions(eachfile, eachfile+".bak")
            cd('..')
        generate_default_cfg_files_RAN = True

## testing consistency of screen output
def test_screen_settings():
    generate_default_cfg_files()
    repoDiffForSimilarity('screen-settings')
def test_screen_settings_reload():
    generate_default_cfg_files()
    repoDiffForSimilarity('screen-settings-reload')

## cfg from -s
def test_settings_cfg():
    generate_default_cfg_files()
    repoDiffForSimilarity('settings.cfg')
def test_settings_organism_cfg():
    generate_default_cfg_files()
    repoDiffForSimilarity('settings_organism.cfg')
def test_settings_world_cfg():
    generate_default_cfg_files()
    repoDiffForSimilarity('settings_world.cfg')

## cfg from -f *fg -s
def test_settings_reload_cfg():
    generate_default_cfg_files()
    diffForSimilarity(dirname_baseline+'settings.cfg.bak',
         dirname_baseline+'settings.cfg',
         outfilename='diffForSimilarity-baseline-settings.cfg')
    diffForSimilarity(dirname_testline+'settings.cfg.bak',
         dirname_testline+'settings.cfg',
         outfilename='diffForSimilarity-testline-settings.cfg')
def test_settings_reload_organism_cfg():
    generate_default_cfg_files()
    diffForSimilarity(dirname_baseline+'settings_organism.cfg.bak',
         dirname_baseline+'settings_organism.cfg',
         outfilename='diffForSimilarity-baseline-settings_organism.cfg')
    diffForSimilarity(dirname_testline+'settings_organism.cfg.bak',
         dirname_testline+'settings_organism.cfg',
         outfilename='diffForSimilarity-testline-settings_organism.cfg')
def test_settings_reload_world_cfg():
    generate_default_cfg_files()
    diffForSimilarity(dirname_baseline+'settings_world.cfg.bak',
         dirname_baseline+'settings_world.cfg',
         outfilename='diffForSimilarity-baseline-settings_world.cfg')
    diffForSimilarity(dirname_testline+'settings_world.cfg.bak',
         dirname_testline+'settings_world.cfg',
         outfilename='diffForSimilarity-testline-settings_world.cfg')
