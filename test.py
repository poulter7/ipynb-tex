import export_cells
import logging
import tempfile
import os


def test_load_ipynb_correctly():
    """Check the parsing works"""
    nb = export_cells.load_ipynb('sample/notebook.ipynb')
    parsed_source, parsed_output, parsed_images, parsed_latex = export_cells.parse_ipynb(nb)

    assert parsed_source['tag1'][0] == u'for i in range(3):'
    assert parsed_source['tag1'][1] == u'    print i'
    assert parsed_source['tag1'][2] == u'for i in range(3, 6):'
    assert parsed_source['tag1'][3] == u'    print i'
    assert parsed_source['tag2'][0] == u"print 'a'"
    assert len(parsed_images) == 2
    logging.fatal(parsed_source['tag3'])


def test_files_exported():
    tempdir = tempfile.mkdtemp()

    assert not os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.source'))
    assert not os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.output'))
    assert not os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.source'))
    assert not os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.output'))
    assert not os.path.exists(os.path.join(tempdir, 'sample/src', 'notebook', '.cells', 'notebook', 'tag1.source'))

    export_cells.extract_cells('sample/notebook.ipynb', tempdir)
    export_cells.extract_cells('sample/src/notebook.ipynb', tempdir)

    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.source'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.output'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.source'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.output'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'img.png'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'latex.tex'))
    assert os.path.exists(os.path.join(tempdir, 'sample/src', 'notebook', '.cells', 'notebook', 'tag1.source'))

def test_files_updated():
    tempdir = tempfile.mkdtemp()
    path = os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.source')
    img_path = os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'img.png')
    export_cells.extract_cells('sample/notebook.ipynb', tempdir)
    time_1 = os.path.getmtime(path)
    time_1_img = os.path.getmtime(img_path)
    import time
    time.sleep(1)
    export_cells.extract_cells('sample/notebook.ipynb', tempdir)
    time_2 = os.path.getmtime(path)
    time_2_img = os.path.getmtime(img_path)
    assert time_2 > time_1
    assert time_2_img > time_1_img

