Code can be used to run in parallel robot to execute groups of tests.

Example:
You got 2 robot files with tests.
In each you got test cases starting with two prefixes 'Some Prefix1: ' and 'Some Prefix2: ' in both. 
You got different tags defined for each files say ABC and XYZ.

What you want to do - is to run all tests with the same prefix in 1 process and with other prefix in another process (so, they are grouped together and execution can be done in parallel).

Then you run code like below:
```
python3 path/to/RobotParallel/src/utils/runner.py -i ABCORXYZ -e kw -d results
```
