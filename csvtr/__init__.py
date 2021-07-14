import sys
from .cli_argparse import Cli

def main():
    cli = Cli(sys.argv)
    cli.run()
