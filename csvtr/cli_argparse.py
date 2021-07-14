# The Cli class defined in this file, <cli_argparse>, provides a basic example of
# how to do "manual" parsing of command-line arguments; Because supporting
# complex command lines is not a trivial task, normally it is recommended to
# use one of the command-parsing libraries available, such as argparse. Please
# see the <cli_argparse> file for an example of that.

import argparse
from .cli_common import CliCommon

class Cli:
    def __init__(self, args):
        parser = argparse.ArgumentParser(
                    prog='csvtr',
                    description='simple transforms for csv files')
        parser.add_argument('src', nargs=1,
                            help='input file name, .csv or .sjson')
        parser.add_argument('dest', nargs=1,
                            help='output file name')
        parser.add_argument('column_spec', nargs='+',
                            action=ColumnSpecArg,
                            help='define the column order for the output file')
        args = parser.parse_args()
        self.src_file_path = args.src[0]
        self.dest_file_path = args.dest[0]
        self.column_spec = args.column_spec

    def run(self):
        CliCommon.run(self.src_file_path,
                      self.dest_file_path,
                      self.column_spec)

# The ColumnSpecArg class can be passed as an action to an argparse argument
# with nargs='+' (all positional arguments following the current parsing 
# position). Its role is to split out a comma-separated list of values and
# flatten that list across multiple arguments, being resistent to the addition
# of spaces in the comma-separated list.
#
# This allows correct parsing for list arguments passed for example like this:
# 1,2,3 ,4, 5,   7
#
# with each group before a space being identified by argparse as an independent
# positional argument
class ColumnSpecArg(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        result = []
        for arg in values:
            raw_col_spec = arg.split(',')
            for item in raw_col_spec:
                if item != '':
                    result.append(int(item))
        setattr(namespace, self.dest, result)
