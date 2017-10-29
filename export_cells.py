#!/usr/local/bin/python
from __future__ import print_function
import logging
import os
import json
import base64
from collections import namedtuple
import itertools

Datatype = namedtuple('Datatype', 'extension encoding parse')


def parse_image(raw):
    return base64.b64decode(raw)


def parse_text(text_lines):
    return os.linesep.join([r.rstrip() for r in text_lines]) + os.linesep


class OutputType(object):
    TeX = Datatype('tex', 'w', parse_text)
    PNG = Datatype('png', 'wb', parse_image)
    OUTPUT = Datatype('output', 'w', parse_text)
    SOURCE = Datatype('source', 'w', parse_text)
    MARKDOWN = Datatype('md', 'w', parse_text)


def parse_ipynb(ipynb_json):
    for cell in ipynb_json['cells']:
        for tag in cell['metadata'].get('tags', []):

            logging.info("Processing src tag {0}".format(tag))
            yield OutputType.SOURCE, tag, cell['source']
            cell_outputs = cell.get('outputs')
            if cell_outputs:
                logging.info("Processing output tag {0}".format(tag))
                for cell_output in cell_outputs:
                    output_type = cell_output.get('output_type')
                    if output_type == 'stream':
                        yield OutputType.OUTPUT, tag, cell_output['text']
                    elif output_type == 'display_data':
                        for datatype, value in list(cell_output['data'].items()):
                            if datatype == 'text/plain':
                                yield OutputType.OUTPUT, tag, value
                            elif datatype == 'text/latex':
                                yield OutputType.TeX, tag, value
                            elif datatype == 'image/png':
                                yield OutputType.PNG, tag, value
                            else:
                                logging.warning("Unable to process datatype {0}".format(datatype))
                    elif output_type == 'execute_result':
                        for datatype, value in list(cell_output['data'].items()):
                            if datatype == 'text/plain':
                                yield OutputType.OUTPUT, tag, value
                            elif datatype == 'text/latex':
                                yield OutputType.TeX, tag, value
                            elif datatype == 'image/png':
                                yield OutputType.PNG, tag, value
                            else:
                                logging.warning("Unable to process datatype {0}".format(datatype))
                    else:
                        logging.warning("Unable to process output_type {0}".format(output_type))


def save_outputs(outputs, output_dir):
    try:
        os.makedirs(os.path.join(output_dir))
    except (os.error, Exception) as e:
        pass
    type_tag = lambda _: (_[0], _[1])
    grouped_outputs = itertools.groupby(sorted(outputs, key=type_tag), key=type_tag)
    for (output_type, tag), values in grouped_outputs:
        path = os.path.join(output_dir, '{0}.{1}'.format(tag, output_type.extension))
        with open(path, output_type.encoding) as f:
            output = [v for _, _, v in values]
            logging.info("{path} <- {output}".format(path=path, output=output))
            f.writelines(output)


def extract_cells(ipynb_path, base_dir=None):
    ipynb_path = os.path.abspath(ipynb_path)
    ipynb_json = load_ipynb(ipynb_path)
    raw_outputs = parse_ipynb(ipynb_json)
    clean_outputs = ((o, t, o.parse(v)) for (o, t, v) in raw_outputs)
    ipynb_dirname = os.path.dirname(ipynb_path)
    ipynb_filename = os.path.basename(ipynb_path)

    if not base_dir:
        output_dir = ipynb_dirname
    else:
        output_dir = os.path.normcase(os.path.join(base_dir, os.path.relpath(ipynb_path.replace('.ipynb', ''))))

    cells_output_dir = os.path.join(output_dir, '.cells', ipynb_filename.replace('.ipynb', ''))
    save_outputs(clean_outputs, cells_output_dir)


def load_ipynb(ipynb_path):
    file = open(ipynb_path, 'r', encoding='utf-8')
    raw_json = file.read()
    return json.loads(raw_json)
