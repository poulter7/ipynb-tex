# ipynb-tex.sty

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![GitHub stars](https://img.shields.io/github/stars/poulter7/ipynb-tex.svg)](https://github.com/poulter7/ipynb-tex/stargazers)

ipynb-tex is a simple LaTeX style package which allows you to extract tagged cells from Jupyter notebooks and include them directly in LaTeX documents.

Rather than save output or copies of source code to insert into TeX documents, ipynb-tex always inserts the latest cells from your notebooks directly into TeX files, ensuring your documentation stays synchronized with your code.

### Installation
In your main document directory, just make a symlink to the ipynb-tex.sty file.

    ln -s /path/to/ipynb-tex/ipynb-tex.sty

### Include cells in your .tex document

The following commands are available to extract content from tagged notebook cells:

| Command | Description |
|---------|-------------|
| `\IpynbSource{notebook.ipynb}{tag}` | Include the source code from cells with the specified tag |
| `\IpynbSourceLatex{notebook.ipynb}{tag}` | Include the source as LaTeX (without sanitization) |
| `\IpynbOutText{notebook.ipynb}{tag}` | Include the text output from cells with the specified tag |
| `\IpynbOutLatex{notebook.ipynb}{tag}` | Include LaTeX-formatted output |
| `\IpynbOutImage{notebook.ipynb}{tag}` | Include an image output (returns base64-encoded image) |

### Compile LaTeX

ipynb-tex uses LuaLaTeX to execute the cell extraction code. You'll need to compile your document with LuaLaTeX and enable shell escape:

```bash
lualatex --shell-escape document.tex
```

For documents with references or complex dependencies, you may need multiple passes:

```bash
lualatex --shell-escape document.tex
lualatex --shell-escape document.tex
```


### Tagging cells in a notebook

In Jupyter Notebook or JupyterLab, you can add tags to cells:

1. **In Jupyter Notebook**: View → Cell Toolbar → Tags
2. **In JupyterLab**: Show the property inspector in the right sidebar

Once the tag interface is visible, you can add custom tags to any cell. These tags are used by ipynb-tex to identify which cells to extract.

### Dependencies

To use ipynb-tex, you need:

- **LuaLaTeX**: The LaTeX engine that executes Lua code
- **luaimageembed package**: For embedding base64-encoded images (when using `\IpynbOutImage`)
- **minted package**: For syntax highlighting (optional, for displaying code)

The package includes its own JSON parser (json.lua by rxi) embedded in the style file.

### Features

- **Direct integration**: Extract cells from Jupyter notebooks without intermediate files
- **Tag-based selection**: Use tags to select specific cells to include
- **Multiple output formats**: Support for source code, text output, LaTeX output, and images
- **Caching**: Notebooks are loaded once and cached for efficient processing
- **No external dependencies**: Pure Lua implementation with embedded JSON parser

### Limitations & Future Improvements

- Currently extracts only the first cell matching a tag
- Images are returned as base64-encoded strings requiring additional processing
- No support for extracting multiple cells with the same tag

See the example in `document.tex` for complete usage examples.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

The embedded json.lua library is Copyright (c) 2020 rxi and is also MIT licensed.

## Acknowledgments

- Uses [json.lua](https://github.com/rxi/json.lua) by rxi for JSON parsing
- Uses [luaimageembed](https://ctan.org/pkg/luaimageembed) by Christian Sachs for base64 image embedding

