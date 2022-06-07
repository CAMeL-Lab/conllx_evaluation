""" The functions in this script generate the command line argparser, which
handles arguments passed to scripts.

Use it in your scripts in the following way:

# 1 create list of arguments
arg_list = [
    Argument('-c', '--conllx', str, 'the ConllX file'),
    Argument('-d', '--dir', str, 'the directory containing ConllX files')
    ]

# 2 pass the arguments, as well as a description of your script
args = generate_argparser_with_arguments(arg_list, script_description='this is a new parser')

# 3 now you can use args through an if statement:
if args.conllx:
    ...


LIMITATION
Not all features of argparser are implemented or available,
only the parameters found in the Argument dataclass.

"""

import argparse
from dataclasses import dataclass
from typing import List


@dataclass
class ParserComponents:
    parser: argparse.ArgumentParser
    two_files: argparse._ArgumentGroup
    two_dirs: argparse._ArgumentGroup

@dataclass
class Argument():
    char_flag: str
    string_flag: str
    arg_type: str
    arg_help: str
    required: bool = False
    metavar: str = ''


def create_arg_parser(script_description: str):
    # return argparse.ArgumentParser(description=script_description)
    parser = argparse.ArgumentParser(description=script_description)
    parser._action_groups.pop()
    two_files = parser.add_argument_group('required arguments')
    two_dirs = parser.add_argument_group('or')
    return ParserComponents(parser, two_files, two_dirs)


def add_argument_to_parser(parser_components, files_or_dirs, argument: Argument):
    if files_or_dirs == 'two_files':
        parser_component = parser_components.two_files
    else:
        parser_component = parser_components.two_dirs

    parser_component.add_argument(argument.char_flag,
        argument.string_flag,
        type=argument.arg_type,
        help=argument.arg_help,
        required=argument.required,
        metavar=argument.metavar)


def add_arguments_to_parser(parser, arguments):
    for k, v in arguments.items():
        for argument in v:
            add_argument_to_parser(parser, k, argument)


def generate_argparser_with_arguments(arguments, script_description:str):
    # create a parser
    parser_components = create_arg_parser(script_description)

    # add arguments to the parser
    add_arguments_to_parser(parser_components, arguments)

    # Execute the parse_args() method
    return parser_components.parser.parse_args()