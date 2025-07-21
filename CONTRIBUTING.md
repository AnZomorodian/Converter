# Contributing to Fily Pro

We love your input! We want to make contributing to Fily Pro as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, to track issues and feature requests, as well as accept pull requests.

### Pull Requests

Pull requests are the best way to propose changes to the codebase. We actively welcome your pull requests:

1. Fork the repo and create your branch from `main`.
2. If you've added code that should be tested, add tests.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes.
5. Make sure your code lints.
6. Issue that pull request!

### Development Setup

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/fily-pro.git
   cd fily-pro
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # Development dependencies
   ```

4. **Install LibreOffice**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install libreoffice
   
   # macOS
   brew install --cask libreoffice
   ```

5. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

6. **Run tests**
   ```bash
   python -m pytest
   ```

7. **Start the development server**
   ```bash
   python main.py
   ```

### Code Style

We use several tools to maintain code quality:

- **Black** for code formatting
- **isort** for import sorting
- **flake8** for linting
- **mypy** for type checking

Run all checks:
```bash
make lint
```

Format code:
```bash
make format
```

### Testing

We use pytest for testing. Please ensure all tests pass before submitting:

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=.

# Run specific test file
python -m pytest tests/test_converter.py

# Run with verbose output
python -m pytest -v
```

### Writing Tests

- Write tests for all new functionality
- Follow the existing test structure
- Use descriptive test names
- Include both positive and negative test cases
- Mock external dependencies (LibreOffice, file system operations)

Example test structure:
```python
def test_convert_word_to_pdf_success():
    """Test successful Word to PDF conversion."""
    # Arrange
    input_file = "test.docx"
    output_file = "test.pdf"
    
    # Act
    result = convert_to_pdf(input_file, output_file)
    
    # Assert
    assert result is True
    assert os.path.exists(output_file)
```

### Commit Messages

We follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

Types:
- `feat`: A new feature
- `fix`: A bug fix
- `docs`: Documentation only changes
- `style`: Changes that do not affect the meaning of the code
- `refactor`: A code change that neither fixes a bug nor adds a feature
- `perf`: A code change that improves performance
- `test`: Adding missing tests or correcting existing tests
- `chore`: Changes to the build process or auxiliary tools

Examples:
```
feat: add batch file upload functionality
fix: resolve file extension validation bug
docs: update API documentation
test: add unit tests for converter module
```

## Issue Reporting

We use GitHub issues to track public bugs. Report a bug by [opening a new issue](https://github.com/yourusername/fily-pro/issues/new).

### Bug Reports

Great bug reports tend to have:

- A quick summary and/or background
- Steps to reproduce
  - Be specific!
  - Give sample code if you can
- What you expected would happen
- What actually happens
- Notes (possibly including why you think this might be happening, or stuff you tried that didn't work)

### Feature Requests

We love feature requests! Please provide:

- Clear description of the feature
- Use case or problem it solves
- Possible implementation approach
- Any related issues or discussions

## Project Structure

```
fily-pro/
├── app.py              # Flask application setup
├── main.py             # Application entry point
├── routes.py           # URL routing and handlers
├── converter.py        # File conversion logic
├── models.py           # Database models
├── utils/              # Utility functions
│   ├── __init__.py
│   ├── security.py     # Security utilities
│   ├── validation.py   # Input validation
│   └── helpers.py      # General helpers
├── tests/              # Test files
│   ├── __init__.py
│   ├── test_app.py
│   ├── test_routes.py
│   ├── test_converter.py
│   └── fixtures/       # Test files and data
├── static/             # Static assets
│   ├── css/
│   ├── js/
│   └── images/
├── templates/          # Jinja2 templates
├── uploads/            # Temporary uploads
├── converted/          # Converted files
├── docs/               # Documentation
├── requirements.txt    # Production dependencies
├── requirements-dev.txt # Development dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
├── Makefile           # Development commands
└── .github/           # GitHub workflows
    └── workflows/
        ├── ci.yml
        └── deploy.yml
```

## Security

### Reporting Security Issues

Please do not report security vulnerabilities through public GitHub issues. Instead, send an email to security@filyteam.com.

### Security Guidelines

- Never commit sensitive data (API keys, passwords, etc.)
- Validate all user inputs
- Use secure file handling practices
- Implement proper authentication for sensitive operations
- Follow OWASP guidelines for web application security

## Performance Guidelines

- Optimize file processing for large files
- Implement proper caching strategies
- Use asynchronous processing for heavy operations
- Monitor memory usage during conversions
- Implement rate limiting for API endpoints

## Documentation

- Update README.md for user-facing changes
- Update API documentation for endpoint changes
- Add docstrings to all functions and classes
- Update CHANGELOG.md for notable changes
- Write clear commit messages

## Community

- Be respectful and inclusive
- Help others in discussions
- Share knowledge and best practices
- Provide constructive feedback
- Follow our Code of Conduct

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Getting Help

- Check existing issues and discussions
- Read the documentation
- Ask questions in GitHub Discussions
- Join our community Discord (coming soon)

Thank you for contributing to Fily Pro! 🚀