import export_cells
import tempfile
import os


def test_files_exported():
    tempdir = tempfile.mkdtemp()

    path = os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.source')
    assert not os.path.exists(path)
    assert not os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.output'))
    assert not os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.source'))
    assert not os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.output'))
    assert not os.path.exists(os.path.join(tempdir, 'sample/src', 'notebook', '.cells', 'notebook', 'tag1.source'))

    export_cells.extract_cells('sample/notebook.ipynb', tempdir)
    export_cells.extract_cells('sample/src/notebook.ipynb', tempdir)

    assert os.path.exists(path)
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag1.output'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.source'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'tag2.output'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'img.png'))
    assert os.path.exists(os.path.join(tempdir, 'sample/notebook', '.cells', 'notebook', 'latex.tex'))
    assert os.path.exists(os.path.join(tempdir, 'sample/src', 'notebook', '.cells', 'notebook', 'tag1.source'))


def test_save_multiple_outputs():
    """Appending to files if there are multiple outputs with the same tag"""
    tempdir = tempfile.mkdtemp()
    outputs = [
        (export_cells.OutputType.OUTPUT, 'tag1', u"a" + os.linesep),
        (export_cells.OutputType.TeX, 'tag2', u"b" + os.linesep),
        (export_cells.OutputType.OUTPUT, 'tag1', u"c" + os.linesep),
    ]
    export_cells.save_outputs(outputs, tempdir)
    output = open(os.path.join(tempdir, 'tag1.output')).readlines()
    assert output == ['a\n', 'c\n']


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
