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
    required: argparse._ArgumentGroup
    optional: argparse._ArgumentGroup

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
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')
    return ParserComponents(parser, required, optional)


def add_argument_to_parser(parser_components, argument: Argument):
    if argument.required:
        parser_component = parser_components.required
    else:
        parser_component = parser_components.optional
    parser_component.add_argument(argument.char_flag,
        argument.string_flag,
        type=argument.arg_type,
        help=argument.arg_help,
        required=argument.required,
        metavar=argument.metavar)


def add_arguments_to_parser(parser, arguments: List[Argument]):
    for argument in arguments:
        add_argument_to_parser(parser, argument)


def generate_argparser_with_arguments(arguments: List[Argument], script_description:str):
    # create a parser
    parser_components = create_arg_parser(script_description)

    # add arguments to the parser
    add_arguments_to_parser(parser_components, arguments)

    # Execute the parse_args() method
    return parser_components.parser.parse_args()