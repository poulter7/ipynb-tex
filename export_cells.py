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

            logging.warn("Processing src tag {0}".format(tag))
            source[tag].extend(cell['source'])
            cell_outputs = cell.get('outputs')
            if cell_outputs:
                logging.warn("Processing output tag {0}".format(tag))
                for cell_output in cell_outputs:
                    output_type = cell_output.get('output_type')
                    if output_type == 'stream':
                        output[tag].extend(cell_output['text'])
                    elif output_type == 'execute_result':
                        for datatype, value in cell_output['data'].items():
                            if datatype == 'text/plain':
                                output[tag].extend(value)
                            else:
                                logging.warn("Unable to process datatype {0}".format(datatype))
                    else:

                        logging.warn("Unable to process output_type {0}".format(output_type))
    return source, output


def save_ipynb_cells(cell_sources, cell_outputs, output_dir):
    for category, contents in zip(['source', 'output'], [cell_sources, cell_outputs]):
        for tag, value in cell_sources.items():
            path = os.path.join(output_dir, '{0}.{1}'.format(tag, category))
            logging.warn("Exporting to {0}".format(path))
            with open(path, 'w') as f:
                f.write("".join(value))


def load_ipynb(path):
    return json.loads(open(path, "r").read())

if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename", )
    (options, args) = parser.parse_args()
    ipynb_path = os.path.abspath(options.filename or args[0])
    ipynb_dirname = os.path.dirname(ipynb_path)
    ipynb_filename = os.path.basename(ipynb_path)

    output_dir = os.path.join(ipynb_dirname, '.cells', ipynb_filename.replace('.ipynb', ''))
    try:
        os.makedirs(output_dir)
    except Exception, e:
        logging.fatal(e)

    sources, outputs = parse_ipynb(load_ipynb(ipynb_path))
    save_ipynb_cells(sources, outputs, output_dir)
