# MABE_testing
automated executable-level functional testing
`mtest.py`

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

### Usage
```
$ python mtest.py -h
usage: mtest.py [-h] [-f] [branch] [commit]

positional arguments:
  branch
  commit

optional arguments:
  -h, --help   show this help message and exit
  -f, --force  force new download and compile
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
python mtest.py -c development
```
