#!/usr/bin/env python3 

''' This file is a simple example of how to build a CLI for my application using argparse. '''

import argparse


def code_to_run(args_from_outside):
    print("Hello World!")
    print(args_from_outside.first_option)
    print(args_from_outside.second_option)


if __name__ == "__main__":
    """ Python idiom that checks whether the script is being run directly as the
    main program or if it is being imported as a module into another script. When a
    Python script is executed directly, Python sets the value of __name__ to
    "__main__" for that script. However, when a script is imported as a module into
    another script, __name__ is set to the name of the module (e.g., the filename
    without the .py extension)."""
    parser = argparse.ArgumentParser("some description to declare what this parser does")
    parser.add_argument(
        "--first_option",
        type=str,
        default="some_sushi",
        help="type in favorite sushi",
    )
    parser.add_argument(
        "--second_option",
        type=str,
        default="some_desert",
        help="type desert",
    )
    args = parser.parse_args() # this will be a `Namespace` object
    code_to_run(args)

# can be run with `./argparse-CLI.py --first_option tempura --second_option cheesecake`