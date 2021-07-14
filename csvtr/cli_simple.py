# The Cli class defined in this file, <cli_simple>, provides a basic example of
# how to do "manual" parsing of command-line arguments; Because supporting
# complex command lines is not a trivial task, normally it is recommended to
# use one of the command-parsing libraries available, such as argparse. Please
# see the <cli_argparse> file for an example of that.

from .cli_common import CliCommon

class Cli:

    def __init__(self, args):
        self.src_file_path = ""
        self.dest_file_path = ""
        self.column_spec =  []
        self.parse_args(args)

    def usage(self):
        print("Usage:\n")
        print("csvtr - simple transforms for csv files")

    def parse_args(self, args):
        if len(args) < 2:
            print("Error: not enough arguments provided, see usage below\n")
            self.usage()

    def run(self):
        CliCommon.run(self.src_file_path,
                      self.dest_file_path,
                      self.column_spec)
