import os
import subprocess
from utils.helpers import test_repo_name, product, basename_base, basename_test, path_base_exe, path_test_exe, cmd
from utils.helpers import ABdiff

## all tests run in order and are run if they begin with 'test_'
def test_startup():
    ## generate cfg (have to 'cd' there, because mabe '-s' ignores 'GLOBAL-outputDirectory' setting)
    os.chdir(basename_base)
    subprocess.run(cmd("./{exe} -s".format(exe=product)), stdout=subprocess.DEVNULL)
    os.chdir('..')
    os.chdir(basename_test)
    subprocess.run(cmd("./{exe} -s".format(exe=product)), stdout=subprocess.DEVNULL)
    os.chdir('..')
    ## run mabe with defaults
    subprocess.run(cmd("{exe} -p GLOBAL-outputDirectory {path}".format(exe=path_base_exe, path=basename_base)), stdout=subprocess.DEVNULL)
    subprocess.run(cmd("{exe} -p GLOBAL-outputDirectory {path}".format(exe=path_test_exe, path=basename_test)), stdout=subprocess.DEVNULL)

def test_compare_csv_files():
    ABdiff('max.csv')
    ABdiff('pop.csv')
    ABdiff('LOD_data.csv')
    ABdiff('LOD_organisms.csv')

def test_compare_cfg_files():
    ABdiff('settings.cfg')
    ABdiff('settings_organism.cfg')
    ABdiff('settings_world.cfg')

def test_shutdown():
    pass
