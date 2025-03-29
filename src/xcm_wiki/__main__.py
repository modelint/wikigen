"""
Blueprint XCM Wiki Generator

"""
# System
import logging
import logging.config
import sys
import argparse
from pathlib import Path

# MX
from xcm_wiki.cm import ClassModelFile
from xcm_wiki import version

_logpath = Path("xcm_wiki.log")
_progname = 'Blueprint Class Model Wiki Generator'


def get_logger():
    """Initiate the logger"""
    log_conf_path = Path(__file__).parent / 'log.conf'  # Logging configuration is in this file
    logging.config.fileConfig(fname=log_conf_path, disable_existing_loggers=False)
    return logging.getLogger(__name__)  # Create a logger for this module


# Configure the expected parameters and actions for the argparse module
def parse(cl_input):
    parser = argparse.ArgumentParser(description=_progname)
    parser.add_argument('-m', '--model', action='store',
                        help='Name xcm file')
    parser.add_argument('-V', '--version', action='store_true',
                        help='Print the current version of the wiki generator app')
    return parser.parse_args(cl_input)


def main():
    # Start logging
    logger = get_logger()
    logger.info(f'{_progname} version: {version}')

    # Parse the command line args
    args = parse(sys.argv[1:])

    if args.version:
        # Just print the version and quit
        print(f'{_progname} version: {version}')
        sys.exit(0)

    # Domain specified
    if args.model:
        cm = ClassModelFile(args.model)

    logger.info("No problemo")  # We didn't die on an exception, basically
    print("\nNo problemo")


if __name__ == "__main__":
    main()
