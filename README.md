# ipynb-tex.sty

ipynb-tex is a simple style sheet which allows you to extract tagged cells out of an Jupyter notebook and include them in a .tex document

Writing very very large documents in Jupyter's notebook is not practical for a range of reasons. But copying code in and out of notebooks into .py or directly into .tex files isn't a great either. It would be much better to directly grab up-to-date source (and output!) from your notebook and include it directly into your .tex files.


### Installation
In your main document directory, just make a symlink to the ipynb-tex.sty file.

    ln -s /path/to/ipynb-tex/ipynb-tex.sty

### Include cells in your .tex document

| Command                           | Description                                                                                                                 |
|--------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------------|
| `\ipynbinclude{notebook}`         | Include before `\begin{document}`. Extract the tagged cells from notebook.ipynb |
| `\ipynbsource{notebook}[tag]` | Include the source from all cells sharing the tag "example".                                                                |
| `\ipynboutput{notebook}[tag]` | Include the output from all cells sharing the tag "example".                                                                |
| `\ipynb{notebook}[tag]`       | Include the source and output from all cells sharing the tag "example".                                                     |
| `\ipynbimage{notebook}[tag]` | Include an image |
| `\ipynbtex{notebook}[tag]` | Include raw TeX output |

### Compile LaTeX
ipynb-tex uses PythonTeX to execute the cell extraction code. So, just as with PythonTeX, you'll need to execute `pythontex` as part of your document build. Also include --shell-escape to allow external functions to be called correctly.

    pdflatex --shell-escape document.tex    #scan the document, figure out what Python needs to be executed
    pythontex --rerun=always document                      #executes the Python found in the document
    pdflatex --shell-escape document.tex    #include any valid TeX printed from the Python execution
    pdflatex --shell-escape document.tex    #ensure any included references are correctly handled


### Tagging cells in a notebook

Toggle the toolbar UI

![toggle toolbar ui](doc/toggle_tag_toolbar.png)

Tag a cell

![tag a cell](doc/tag_cell.png)

### Modifying this plugin
This repo comes with a ready to go version of `ipynb-tex.sty`, but if you want to make changes and rebuild it just run `./build`, which merges `ipynb-tex-template.sty` and `extract_cells.py` to create `ipynb-tex.sty`.


### Running Tests

    pip install nose
    nosetests