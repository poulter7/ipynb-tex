import export_cells
import logging
import tempfile
import os


def test_load_ipynb_correctly():
    """Check the parsing works"""
    nb = export_cells.load_ipynb('notebook.ipynb')
    parsed_source, parsed_output = export_cells.parse_ipynb(nb)

    assert parsed_source['tag1'][0] == u'for i in range(3):'
    assert parsed_source['tag1'][1] == u'    print i'
    assert parsed_source['tag1'][2] == u'for i in range(3, 6):'
    assert parsed_source['tag1'][3] == u'    print i'
    assert parsed_source['tag2'][0] == u"print 'a'"
    logging.fatal(parsed_source['tag3'])


def test_files_exported():
    tempdir = tempfile.mkdtemp()

    assert not os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag1.source'))
    assert not os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag1.output'))
    assert not os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag2.source'))
    assert not os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag2.output'))
    assert not os.path.exists(os.path.join(tempdir, 'src', 'notebook', '.cells', 'notebook', 'tag1.source'))

    export_cells.extract_cells('notebook.ipynb', tempdir)
    export_cells.extract_cells('src/notebook.ipynb', tempdir)

    assert os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag1.source'))
    assert os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag1.output'))
    assert os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag2.source'))
    assert os.path.exists(os.path.join(tempdir, 'notebook', '.cells', 'notebook', 'tag2.output'))
    assert os.path.exists(os.path.join(tempdir, 'src', 'notebook', '.cells', 'notebook', 'tag1.source'))

