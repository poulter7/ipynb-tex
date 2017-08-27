import extract_cells

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", )
    (options, args) = parser.parse_args()
    extract_cells.extract_cells(options.filename or args[0])


if __name__ == '__main__':
    main()
