#!/usr/local/bin/python
import collections
from optparse import OptionParser
import logging
import os
import json


def parse_ipynb(ipynb_json):
    source = collections.defaultdict(list)
    output = collections.defaultdict(list)

    for cell in ipynb_json['cells']:
        for tag in cell['metadata'].get('tags', []):
            # for each cell, for each tag the cell has

            logging.info("Processing src tag {0}".format(tag))
            source[tag].extend(map(unicode.rstrip, cell['source']))
            cell_outputs = cell.get('outputs')
            if cell_outputs:
                logging.info("Processing output tag {0}".format(tag))
                for cell_output in cell_outputs:
                    output_type = cell_output.get('output_type')
                    if output_type == 'stream':
                        output[tag].extend(map(unicode.rstrip, cell_output['text']))
                    elif output_type == 'execute_result':
                        for datatype, value in cell_output['data'].items():
                            if datatype == 'text/plain':
                                output[tag].extend(map(unicode.rstrip, value))
                            else:
                                logging.warn("Unable to process datatype {0}".format(datatype))
                    else:

                        logging.warn("Unable to process output_type {0}".format(output_type))
    return source, output


def save_ipynb_cells(cell_sources, cell_outputs, output_dir):
    try:
        os.makedirs(os.path.join(output_dir))
    except os.error, e:
        pass
    except Exception, e:
        logging.fatal(e)
    for category, contents in zip(['source', 'output'], [cell_sources, cell_outputs]):
        for tag, value in contents.items():
            path = os.path.join(output_dir, '{0}.{1}'.format(tag, category))
            logging.info("Exporting to {0}".format(path))
            with open(path, 'w') as f:
                f.write("\n".join(value))


def load_ipynb(path):
    return json.loads(open(path, "r").read())


def extract_cells(ipynb_path, base_dir=None):
    ipynb_path = os.path.abspath(ipynb_path)
    sources, outputs = parse_ipynb(load_ipynb(ipynb_path))

    ipynb_dirname = os.path.dirname(ipynb_path)
    ipynb_filename = os.path.basename(ipynb_path)

    if not base_dir:
        output_dir = ipynb_dirname
    else:
        output_dir = os.path.normcase(os.path.join(base_dir, os.path.relpath(ipynb_path.replace('.ipynb', ''))))

    logging.warning(ipynb_dirname)

    output_dir = os.path.join(output_dir, '.cells', ipynb_filename.replace('.ipynb', ''))
    save_ipynb_cells(sources, outputs, output_dir)


def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", )
    (options, args) = parser.parse_args()
    extract_cells(options.filename or args[0])


if __name__ == '__main__':
    main()

