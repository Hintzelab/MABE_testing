import os
import subprocess
from utils.helpers import test_repo_name, product, dir_base, dir_test, path_base, path_test
from utils.helpers import ABdiff

## all tests run in order and are run if they begin with 'test_'

def test_startup():
    ## generate cfg (have to 'cd' there, because mabe '-s' ignores 'GLOBAL-outputDirectory' setting)
    os.chdir(dir_base)
    subprocess.run(product+" -s", stdout=subprocess.DEVNULL)
    os.chdir('..')
    os.chdir(dir_test)
    subprocess.run(product+" -s", stdout=subprocess.DEVNULL)
    os.chdir('..')
    ## run mabe with defaults
    subprocess.run(path_base+" -p GLOBAL-outputDirectory "+dir_base, stdout=subprocess.DEVNULL)
    subprocess.run(path_test+" -p GLOBAL-outputDirectory "+dir_test, stdout=subprocess.DEVNULL)

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
