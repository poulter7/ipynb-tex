import export_cells
import collections
from optparse import OptionParser
import logging
import os
import json

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", )
    (options, args) = parser.parse_args()
    export_cells.extract_cells(options.filename or args[0])


if __name__ == '__main__':
    main()
