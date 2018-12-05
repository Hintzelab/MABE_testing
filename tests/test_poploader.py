import os, subprocess, pytest
from utils.helpers import this_repo_path, exe_name, EXE, slash, dirname_baseline, dirname_testline, path_baseline_exe, path_testline_exe
from utils.helpers import cd, diff, repoDiff, runCmdAndHideOutput, runCmdAndShowOutput, runCmdAndSaveOutput, getFileContents
from utils.helpers import copyfileAndPermissions, buildMessageErrorExpectedWithArgs
from utils.helpers import thisTestName, repoDiffForDifference, repoDiffForSimilarity, diffForDifference, diffForSimilarity

##
## all tests run IN ORDER OF DEFINITION and are run if they begin with 'test_'
## a test_fn() will fail on first failure and stop testing that test_fn, continuing on to the next test_fn.
## use `assert condition, "error message"` in a test_fn() to print a useful message on failure
##

savingParams =  ' ARCHIVIST_LODWAP-dataSequence :10 ARCHIVIST_LODWAP-organismsSequence :10 ARCHIVIST_LODWAP-terminateAfter 0 ARCHIVIST_DEFAULT-writeSnapshotDataFiles 1 ARCHIVIST_DEFAULT-writeSnapshotOrganismsFiles 1 ARCHIVIST_DEFAULT-snapshotOrganismsSequence :10 ARCHIVIST_DEFAULT-snapshotDataSequence :10'

brainTestString = EXE+' -p BRAIN-brainType {brainT} GLOBAL-initPop "{initPop}" GLOBAL-updates {updates}'
brainTestStringWithSaving = brainTestString + savingParams

testString = EXE+' -p GLOBAL-initPop "{initPop}" GLOBAL-updates {updates}'
testStringWithSaving = testString + savingParams

generate_default_csv_files_RAN = False
def generate_default_csv_files():
    global generate_default_csv_files_RAN
    if not generate_default_csv_files_RAN:
        for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
            cd(this_repo_path)
            cd(eachdir)
            runCmdAndSaveOutput( "{exe} -l".format(exe=EXE), filename='screen-plf' )
            runCmdAndHideOutput( testStringWithSaving.format( initPop='default 100', updates='10' ) ) ## generate large snapshot_organisms_10.csv
            runCmdAndHideOutput( testStringWithSaving.format( initPop='default 1', updates='1' ) ) ## generate small snapshot_organisms_0.csv
            cd('..')
        generate_default_csv_files_RAN = True

## testing consistency of screen output
def test_screen_poploader():
    generate_default_csv_files()
    repoDiffForSimilarity('screen-plf')

## generated files
def test_plf():
    generate_default_csv_files()
    repoDiffForSimilarity('population_loader.plf')
def test_lod_data():
    generate_default_csv_files()
    repoDiffForSimilarity('LOD_data.csv')
def test_lod_organisms():
    generate_default_csv_files()
    repoDiffForSimilarity('LOD_organisms.csv')
def test_saving():
    generate_default_csv_files()
    repoDiffForSimilarity('snapshot_organisms_0.csv')
def test_screen_loading():
    generate_default_csv_files()
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(eachdir)
        runStr = testStringWithSaving.format(
                 initPop="'snapshot_organisms_0.csv'",
                 updates="1"
                 )
        runCmdAndSaveOutput(runStr, filename='screen-poploading') ## generate snapshot_organisms_0.csv
        cd('..') ## could also have done cd(this_repo_path)
    repoDiffForSimilarity('screen-poploading')
def test_saving_after_loading():
    repoDiffForSimilarity('snapshot_organisms_0.csv')

##
## Test success conditions for greatest/least
##
@pytest.mark.parametrize('numToLoad', [1,5,50,100], ids=['1','5','50','100'])
@pytest.mark.parametrize('mostCommand', ['greatest','least'], ids=['greatest','least'])
def test_reload_most_byid_noerror(numToLoad,mostCommand):
    generate_default_csv_files()
    outputFilename = 'screen-reload-{most}-byid-{num}'.format(
                      most=mostCommand, num=str(numToLoad)
                      )
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path) ## ensures clean state
        cd(eachdir)
        initPop = "{most} {amount} by ID from {{'snapshot_organisms_10.csv'}}".format(
                  most=mostCommand,
                  amount=str(numToLoad)
                  )
        runStr = testString.format(
                 initPop=initPop,
                 updates="1"
                 )
        runCmdAndSaveOutput(runStr, filename=outputFilename) ## normalize ID
        cd('..')
    repoDiffForSimilarity(outputFilename)

##
## Test failure conditions for greatest/least
##
## NOTE: we have to parametrize the test dir too to make separete calls, because an expected failure will end the fn immediately
@pytest.mark.parametrize('numToLoad', [-1,0,101], ids=['(-1)','(0)','(101)'])
@pytest.mark.parametrize('mostCommand', ['greatest','least'], ids=['greatest','least'])
@pytest.mark.parametrize('dirToTest', [dirname_baseline, dirname_testline], ids=['baseline','testline'])
def test_reload_most_byid_error(numToLoad,mostCommand,dirToTest):
    generate_default_csv_files()
    errorMessage = buildMessageErrorExpectedWithArgs( dirToTest,mostCommand,numToLoad ) ## returns this fn name, the args, and that error was expected
    with pytest.raises(subprocess.CalledProcessError, message=errorMessage):
        cd(this_repo_path) ## reset after possible error
        cd(dirToTest)
        initPop = "{most} {amount} by ID from {{'snapshot_organisms_10.csv'}}".format(
                  most=mostCommand,
                  amount=str(numToLoad)
                  )
        runStr = testString.format(
                 initPop=initPop,
                 updates="1"
                 )
        runCmdAndSaveOutput(runStr,'tempfile') ## must 'Show' output for error sig to be inspected

## test reloading of brains and make sure generation 0 saved out is the same as the originally loaded file
## WARNING: This test assumest 'greatest by id' works
@pytest.mark.parametrize('brainType', ['CGP','LSTM','ConstantValues','Wire','Markov'], ids=['CGP','LSTM','ConstantValues','Wire','Markov'])
def test_reload_brains(brainType):
    initPopLoading="greatest 1 by ID from {'snapshot_organisms_0.csv'}"
    for eachdir in [dirname_baseline, dirname_testline]: ## loop through each of baseline and testline and generate the files for later diffing
        cd(this_repo_path)
        cd(eachdir)
        runCmdAndHideOutput( brainTestStringWithSaving.format( brainT=brainType, initPop='default 100', updates='10' ) ) ## generate large snapshot_organisms_10.csv
        runCmdAndHideOutput( brainTestStringWithSaving.format( brainT=brainType, initPop='default 1', updates='1' ) ) ## generate small snapshot_organisms_0.csv
        runStr = brainTestStringWithSaving.format(
                 brainT=brainType,
                 initPop="default 1",
                 updates="1"
                 )
        runCmdAndHideOutput(runStr) ## generate snapshot_organisms_0.csv
        runStr = brainTestStringWithSaving.format(
                 brainT=brainType,
                 initPop=initPopLoading,
                 updates="1"
                 )
        runCmdAndHideOutput(runStr) ## normalize ID by running again
        for filetype in ['data','organisms']:
            copyfileAndPermissions('snapshot_'+filetype+'_0.csv', 'save1_'+filetype+'.csv') ## save first output
        runCmdAndHideOutput(runStr) ## generate snapshot_organisms_0.csv
        for filetype in ['data','organisms']:
            copyfileAndPermissions('snapshot_'+filetype+'_0.csv', 'save2_'+filetype+'.csv') ## save second output
        cd('..')
    diffForSimilarity(dirname_baseline+'save1_organisms.csv',
         dirname_baseline+'save2_organisms.csv',
         outfilename='diff-baseline-reloaded-{}-organisms'.format(brainType)
         )
    diffForSimilarity(dirname_testline+'save1_data.csv',
         dirname_testline+'save2_data.csv',
         outfilename='diff-testline-reloaded-{}-data'.format(brainType)
         )
