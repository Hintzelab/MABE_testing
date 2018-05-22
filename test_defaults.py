import os
import subprocess
from utils.helpers import this_repo_path, product, basename_base, basename_test, path_base_exe, path_test_exe
from utils.helpers import ABdiff, runCmdAndHideOutput, runCmdAndShowOutput

## all tests run in order and are run if they begin with 'test_'
def test_startup():
    ## generate cfg (have to 'cd' there, because mabe '-s' ignores 'GLOBAL-outputDirectory' setting)
    os.chdir(basename_base)
    runCmdAndHideOutput( "./{exe} -s".format(exe=product) )
    os.chdir('..')
    os.chdir(basename_test)
    runCmdAndHideOutput( "./{exe} -s".format(exe=product) )
    os.chdir('..')
    ## run mabe with defaults
    runCmdAndHideOutput( "{exe} -p GLOBAL-outputDirectory {path}".format(exe=path_base_exe, path=basename_base) )
    runCmdAndHideOutput( "{exe} -p GLOBAL-outputDirectory {path}".format(exe=path_test_exe, path=basename_test) )

def test_max_csv():
    ABdiff('max.csv')
def test_pop_csv():
    ABdiff('pop.csv')
def test_lod_data_csv():
    ABdiff('LOD_data.csv')
def test_lod_organisms_csv():
    ABdiff('LOD_organisms.csv')
def test_settings_cfg():
    ABdiff('settings.cfg')
def test_settings_organism_cfg():
    ABdiff('settings_organism.cfg')
def test_settings_world_cfg():
    ABdiff('settings_world.cfg')

def test_shutdown():
    pass
