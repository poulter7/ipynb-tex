# Contributing to ipynb-tex

Thank you for your interest in contributing to ipynb-tex! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:

- A clear, descriptive title
- Steps to reproduce the problem
- Expected behavior
- Actual behavior
- Your environment (OS, TeX distribution, versions)
- Minimal example notebook and .tex file demonstrating the issue

### Suggesting Enhancements

Enhancement suggestions are welcome! Please open an issue with:

- A clear description of the enhancement
- Motivation for the feature
- Example use cases
- Any potential implementation approaches you've considered

### Pull Requests

1. **Fork the repository** and create your branch from `main`
2. **Make your changes** following the code style of the project
3. **Test your changes** with the example document
4. **Update documentation** if you've changed functionality
5. **Submit a pull request** with a clear description of your changes

#### Code Style

- Follow existing Lua code style in `ipynb-tex.sty`
- Use descriptive variable and function names
- Add comments for complex logic
- Keep functions focused and single-purpose

#### Testing Your Changes

Before submitting a PR, please test that:

1. The example document compiles successfully:
   ```bash
   lualatex --shell-escape document.tex
   ```

2. Your changes work with different notebook structures
3. Existing functionality is not broken

### Development Setup

1. Clone the repository
2. Make changes to `ipynb-tex.sty`
3. Test with the example document and notebook
4. Verify the generated PDF looks correct

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Assume good intentions

## Questions?

Feel free to open an issue for questions or discussions about the project.

## License

By contributing, you agree that your contributions will be licensed under the MIT License.
