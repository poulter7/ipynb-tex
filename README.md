# ipynb-tex.sty

ipynb-tex is a simple style sheet which allows you to extract tagged cells out of an ipython notebook and include them in a .tex document

Writing very very large documents in Jupyter's notebook is not practical for a range of reasons. But copying code in and out of notebooks into .py or directly into .tex files isn't a great either. It would be much better to directly grab up-to-date source (and output!) from your notebook and include it directly into your .tex files.


## Build process
1.  pdflatex --shell-escape document.tex #scan the document, figure out what Python needs to be executed
2.  pythontex document #executes the Python we found in the document
3.  pdflatex --shell-escape document.tex #include any output from our Python execution, this is pure TeX
4. pdflatex --shell-escape document.tex #ensure any references are correctly handled.

## Rebuild
This repo comes with a ready to go version of ipynb-tex.sty, but if you want to make changes and rebuild itjust run ./build, which merges ipynb-tex-template.sty and extract_cells.py to create ipynb-tex.sty.

## Requirements
pip install pygments

## Compile LaTeX
ipynb-tex uses pythontex to execute some cell extraction code and to format the resulting source. So, just as with pythontex, you'll need to execute.



