#!/usr/local/bin/python
from __future__ import print_function
from builtins import zip
from builtins import map
import collections
from optparse import OptionParser
import logging
import os
import json
import base64
import string


def parse_ipynb(ipynb_json):
    source = collections.defaultdict(list)
    output = collections.defaultdict(list)
    images = collections.defaultdict(list)
    latex = collections.defaultdict(list)

    for cell in ipynb_json['cells']:
        for tag in cell['metadata'].get('tags', []):

            logging.info("Processing src tag {0}".format(tag))
            source[tag].extend([v.rstrip() for v in cell['source']])
            cell_outputs = cell.get('outputs')
            if cell_outputs:
                logging.info("Processing output tag {0}".format(tag))
                for cell_output in cell_outputs:
                    output_type = cell_output.get('output_type')
                    if output_type == 'stream':
                        output[tag].extend([v.rstrip() for v in cell_output['text']])
                    elif output_type == 'display_data':
                        string_rep = cell_output['data']['image/png']
                        image = base64.b64decode(string_rep)
                        images[tag].append(image)
                    elif output_type == 'execute_result':
                        for datatype, value in list(cell_output['data'].items()):
                            if datatype == 'text/plain':
                                output[tag].extend([v.rstrip() for v in value])
                            elif datatype == 'text/latex':
                                latex[tag].extend([v.rstrip() for v in value])
                            else:
                                logging.warn("Unable to process datatype {0}".format(datatype))
                    else:

                        logging.warn("Unable to process output_type {0}".format(output_type))
    return source, output, images, latex


def save_ipynb_cells(cell_sources, cell_outputs, cell_images, cell_latex, output_dir):
    try:
        os.makedirs(os.path.join(output_dir))
    except os.error as e:
        pass
    except Exception as e:
        pass
    for category, contents in zip(['source', 'output'], [cell_sources, cell_outputs]):
        for tag, value in list(contents.items()):
            path = os.path.join(output_dir, '{0}.{1}'.format(tag, category))
            logging.info("Exporting to {0}".format(path))
            with open(path, 'w') as f:
                try:
                    f.write("\n".join(value))
                except:
                    pass
    for tag, images in list(cell_images.items()):
        for image in images:
            path = os.path.join(output_dir, '{0}.{1}'.format(tag, 'png'))
            with open(path, 'wb') as f:
                f.write(image)
    for tag, latexs in list(cell_latex.items()):
        for latex in latexs:
            path = os.path.join(output_dir, '{0}.{1}'.format(tag, 'tex'))
            with open(path, 'w') as f:
                f.write(latex)


def load_ipynb(path):
    return json.loads(open(path, "r").read())


def extract_cells(ipynb_path, base_dir=None):
    ipynb_path = os.path.abspath(ipynb_path)
    sources, outputs, images, latex = parse_ipynb(load_ipynb(ipynb_path))

    ipynb_dirname = os.path.dirname(ipynb_path)
    ipynb_filename = os.path.basename(ipynb_path)

    if not base_dir:
        output_dir = ipynb_dirname
    else:
        output_dir = os.path.normcase(os.path.join(base_dir, os.path.relpath(ipynb_path.replace('.ipynb', ''))))

    cells_output_dir = os.path.join(output_dir, '.cells', ipynb_filename.replace('.ipynb', ''))
    save_ipynb_cells(sources, outputs, images, latex, cells_output_dir)

print ('')