# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- LICENSE file (MIT License)
- CONTRIBUTING.md with contribution guidelines
- CHANGELOG.md for tracking changes
- requirements.txt for example dependencies
- .editorconfig for consistent coding style
- GitHub issue templates (bug report and feature request)
- Comprehensive .gitignore patterns
- Repository badges in README

### Changed
- Updated README.md with better formatting and accurate command documentation
- Fixed command table in README to match actual LaTeX commands
- Clarified that ipynb-tex uses LuaLaTeX (not PythonTeX)
- Improved documentation for tagging cells in Jupyter

### Removed
- References to non-existent doc/ directory images in README

## [0.1] - 2017-08-21

### Added
- Initial release of ipynb-tex
- Lua-based implementation with embedded JSON parser
- Support for extracting source code, text output, LaTeX output, and images
- Caching system for loaded notebooks
- Commands: `\IpynbSource`, `\IpynbSourceLatex`, `\IpynbOutText`, `\IpynbOutLatex`, `\IpynbOutImage`

[Unreleased]: https://github.com/poulter7/ipynb-tex/compare/v0.1...HEAD
[0.1]: https://github.com/poulter7/ipynb-tex/releases/tag/v0.1
