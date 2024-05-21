#!/usr/bin/env python3 
# 
# the above shebang line is needed if I want to run this script without specifying in
# interpreter within the bash, like python "./system.py file.csv". In this case I need
# to make the file executable (`chmod +x system.py`) and add the shebang line. But I can
# also run `python system.py file.csv` specifying an interpreter and then there is no
# need to add the shebang line. Also execution rights need to be granted to the file if
# trying to execute it without defining interpreter (`chmod +x [filename]`).

"""Python module os is used to interact with operating system"""
import os

# Get the value of the HOME environment variable
print(os.environ.get('HOME'))

# Print the PATH environment variable
print(os.environ['PATH'])
# os.environ serves us with a dict of all the environmental variables of the running
# process. These are provided by the shell that starts the process and can be inspected
# with the `printenv` shell command or by echoing a specific variable, like `echo
# $PATH`.

print('')
"""Python module sys is used to interact with interpreter (CPython mostly)"""

import sys
# Print the Python version
print(sys.version)

# Print the executable path of the Python interpreter
print(sys.executable)

# Print the list of command-line arguments passed to the script
print(sys.argv)
# Shell parses input into space delimited words (using some complex rules to distinguish
# commands from arguments and options). The first word needs to be either a build in
# shell command (like cd) or a path to a file that can be found within $PATH and that
# has execute (`x`) permission. The following commands are options (flagged) and their
# arguments.