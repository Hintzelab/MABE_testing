# MABE_testing
automated executable-level functional and consistency testing
`mtest.py`

## WIP
This is very much a work-in-progress at the moment as we decide the best way to include all relevant modes of testing.

### To Do
- [x] Create convenience utility to run baseline or testline mabe with arguments
- [x] Capture stdout to a standard filename ex: stdout.txt
- [x] Capture stderr to a standard filename ex: stderr.txt
- [x] Modify ABDiff to accept a path (and path-sep-agnostic)
- [x] Add ability to specify only specific tests ex: pass 'defaults' for test_defaults.py to be run

### Description
During MABE development we want to ensure that
we do not inadvertently change (or break) the
functioning of other parts of MABE. To do this
we can compare MABE output from your development
version to an older version. This tool can be
told to compare against any branch or commit
hash.

Simple testing relies on the pytest module.
Group tests into files of the format `test_*.py`
with tests as functions named `test_*()` which
perform an assert.

Test functions will be run in the order they are
specified, allowing setup and teardown functions,
if needed. A helper function `ABdiff(filename)` is
included that will compare the same file in your
version of MABE with the older version of MABE.

### Requirements
- make
- gcc compiler >= 6.2
- python3 >= 3.5
- git

### Usage
```
$ python mtest.py -h
usage: mtest.py [-h] [-f] [-s SUBSET] [branch] [commit]

positional arguments:
  branch
  commit

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           force new download and compile
  -s SUBSET, --subset SUBSET
                        test filter expression: "defaults and not settings"
```

### Example
Download MABE_testing into your MABE repo

```
git clone https://github.com/hintzelab/mabe mymabe
cd mymabe
git clone https://github.com/hintzelab/mabe_testing
cd mabe_testing
```

Test your `mymabe` build against development
```
python mtest.py development
```

More advanced testing
```
python contest.py -s "reload brains Markov" ../ development development "cp ~/projects/mabetest/buildOptions.txt . && python pythonTools/mbuild.py -g make && make -j24" ./mabe
```
