import os, subprocess, pytest
from utils.helpers import this_repo_path, mabe, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, diff, ABdiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents
from utils.helpers import copyfileAndPermissions

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
        dirs = [dirname_baseline, dirname_testline]
        for eachdir in dirs: ## loop through each of baseline and testline and generate the files for later diffing
            cd(eachdir)
            runCmdAndSaveOutput( "./{exe} -l".format(exe=mabe), filename='screen-plf' )
            runCmdAndHideOutput( "./{exe} -p GLOBAL-updates 10 ARCHIVIST_LODWAP-organismsSequence :10 ARCHIVIST_LODWAP-terminateAfter 0 ARCHIVIST_DEFAULT-writeSnapshotDataFiles 1 ARCHIVIST_DEFAULT-writeSnapshotOrganismsFiles 1 ARCHIVIST_DEFAULT-snapshotOrganismsSequence :10".format(exe=mabe)) ## generate snapshot_organisms_100.csv
            #runCmdAndSaveOutput( "./{exe} -p GLOBAL-initPop \"MASTER = snapshot_organisms_100.csv\"".format(exe=mabe))
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
def test_screen_poploader(ctx):
    ABdiff('screen-plf')

## generated files
def test_plf(ctx):
    ABdiff('population_loader.plf')
def test_lod_data(ctx):
    ABdiff('LOD_data.csv')
def test_lod_organisms(ctx):
    ABdiff('LOD_organisms.csv')
def test_snapshot_organisms_10_loading(ctx):
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(eachdir)
        runCmdAndSaveOutput( './{exe} -p GLOBAL-initPop "MASTER = \'snapshot_organisms_10.csv\'" GLOBAL-updates 10 ARCHIVIST_LODWAP-dataSequence :10 ARCHIVIST_LODWAP-organismsSequence :10 ARCHIVIST_LODWAP-terminateAfter 0 ARCHIVIST_DEFAULT-writeSnapshotDataFiles 1 ARCHIVIST_DEFAULT-writeSnapshotOrganismsFiles 1 ARCHIVIST_DEFAULT-snapshotOrganismsSequence :10 ARCHIVIST_DEFAULT-snapshotDataSequence :10'.format(exe=mabe), filename="screen-poploading") ## generate snapshot_organisms_100.csv
        cd('..') ## could also have done cd(this_repo_path)
    ABdiff('snapshot_organisms_10.csv')
    ABdiff('screen-poploading')

## test reloading of brains and make sure generation 0 saved out is the same as the originally loaded file
## NOTE: This isn't working right now, though I'm unsure why.
@pytest.mark.parametrize('brainType', ['CGP','LSTM','ConstantValues','Wire','Markov'], ids=['CGP','LSTM','ConstantValues','Wire','Markov'])
def test_reload_CGP(ctx, brainType):
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(eachdir)
        runCmdAndHideOutput( './{exe} -p BRAIN-brainType {brainT} GLOBAL-updates 10 ARCHIVIST_LODWAP-dataSequence :10 ARCHIVIST_LODWAP-organismsSequence :10 ARCHIVIST_LODWAP-terminateAfter 0 ARCHIVIST_DEFAULT-writeSnapshotDataFiles 1 ARCHIVIST_DEFAULT-writeSnapshotOrganismsFiles 1 ARCHIVIST_DEFAULT-snapshotOrganismsSequence :10 ARCHIVIST_DEFAULT-snapshotDataSequence :10'.format(exe=mabe,brainT=brainType)) ## generate snapshot_organisms_10.csv
        for filetype in ['data','organisms']:
            copyfileAndPermissions('snapshot_'+filetype+'_10.csv','save1_'+filetype+'.csv') ## save timepoint 10
        runCmdAndHideOutput( './{exe} -p BRAIN-brainType {brainT} GLOBAL-updates 1 ARCHIVIST_LODWAP-dataSequence :10 ARCHIVIST_LODWAP-organismsSequence :10 ARCHIVIST_LODWAP-terminateAfter 0 ARCHIVIST_DEFAULT-writeSnapshotDataFiles 1 ARCHIVIST_DEFAULT-writeSnapshotOrganismsFiles 1 ARCHIVIST_DEFAULT-snapshotOrganismsSequence :10 ARCHIVIST_DEFAULT-snapshotDataSequence :10'.format(exe=mabe,brainT=brainType)) ## generate snapshot_organisms_0.csv
        for filetype in ['data','organisms']:
            copyfileAndPermissions('snapshot_'+filetype+'_0.csv','save2_'+filetype+'.csv') ## save timepoint 0
        cd('..') ## could also have done cd(this_repo_path)
    ## compare original timepoint 10 and reloaded timepoint 0 (hopefully they are the same)
    diff(dirname_baseline+'save1_organisms.csv',dirname_baseline+'save2_organisms.csv',outfilename='diff-baseline-reloaded-{}-organisms'.format(brainType))
    diff(dirname_testline+'save1_data.csv',dirname_testline+'save2_data.csv',outfilename='diff-testline-reloaded-{}-data'.format(brainType))
