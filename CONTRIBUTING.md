# Contributing to Flask Container vs VM Performance Analysis

Thank you for your interest in contributing to this project! This document provides guidelines and information for contributors.

## 🤝 How to Contribute

### Reporting Issues

Before creating an issue, please check if it already exists. When creating a new issue, please include:

- **Clear description** of the problem or feature request
- **Steps to reproduce** (for bugs)
- **Expected vs actual behavior**
- **Environment details** (OS, Python version, Docker version)
- **Screenshots** (if applicable)

### Suggesting Enhancements

We welcome suggestions for improvements! Please include:

- **Clear description** of the enhancement
- **Use case** and benefits
- **Implementation ideas** (if you have any)
- **Alternative solutions** considered

## 🚀 Development Setup

### Prerequisites

- Python 3.9+
- Docker 20.10+
- Git
- Virtual environment (recommended)

### Local Development

1. **Fork and clone the repository**
   ```bash
   git clone https://github.com/yourusername/flask-container-vm.git
   cd flask-container-vm
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-dev.txt  # If available
   ```

4. **Run tests**
   ```bash
   pytest test_app.py -v
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 📝 Code Style Guidelines

### Python Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide
- Use type hints where appropriate
- Write docstrings for all functions and classes
- Keep line length under 88 characters (Black formatter standard)

### Docker Best Practices

- Use multi-stage builds for optimization
- Minimize image layers
- Use specific version tags
- Run as non-root user
- Include health checks

### Documentation

- Update README.md for significant changes
- Add docstrings to new functions
- Update API documentation if endpoints change
- Include examples in docstrings

## 🧪 Testing Guidelines

### Writing Tests

- Write tests for all new features
- Include both positive and negative test cases
- Aim for high test coverage
- Use descriptive test names
- Mock external dependencies

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest test_app.py

# Run with verbose output
pytest -v
```

### Test Structure

```python
def test_function_name_should_do_something():
    # Arrange
    input_data = "test"
    
    # Act
    result = function_under_test(input_data)
    
    # Assert
    assert result == expected_output
```

## 🔄 Pull Request Process

### Before Submitting

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write code following style guidelines
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   ```bash
   # Run tests
   pytest
   
   # Run linting
   flake8 .
   
   # Run type checking
   mypy .
   ```

4. **Commit your changes**
   ```bash
   git add .
   git commit -m "Add: descriptive commit message"
   ```

### Submitting a Pull Request

1. **Push your branch**
   ```bash
   git push origin feature/your-feature-name
   ```

2. **Create a Pull Request**
   - Use a clear, descriptive title
   - Reference any related issues
   - Provide a detailed description
   - Include screenshots if applicable

3. **Pull Request Template**
   ```markdown
   ## Description
   Brief description of changes
   
   ## Type of Change
   - [ ] Bug fix
   - [ ] New feature
   - [ ] Breaking change
   - [ ] Documentation update
   
   ## Testing
   - [ ] Tests pass locally
   - [ ] New tests added
   - [ ] Manual testing completed
   
   ## Checklist
   - [ ] Code follows style guidelines
   - [ ] Self-review completed
   - [ ] Documentation updated
   - [ ] No breaking changes
   ```

## 📋 Review Process

### For Contributors

- Respond to feedback promptly
- Make requested changes
- Keep PRs focused and small
- Update documentation as needed

### For Maintainers

- Review code for quality and style
- Test functionality thoroughly
- Provide constructive feedback
- Merge when ready

## 🏷️ Commit Message Convention

Use conventional commits format:

```
type(scope): description

[optional body]

[optional footer]
```

### Types

- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes
- `refactor`: Code refactoring
- `test`: Test changes
- `chore`: Maintenance tasks

### Examples

```
feat(api): add new health check endpoint
fix(docker): resolve container startup issue
docs(readme): update installation instructions
```

## 🐛 Bug Reports

When reporting bugs, please include:

1. **Environment Information**
   - OS and version
   - Python version
   - Docker version
   - Package versions

2. **Steps to Reproduce**
   - Clear, numbered steps
   - Expected vs actual behavior
   - Error messages or logs

3. **Additional Context**
   - Screenshots
   - Related issues
   - Workarounds found

## 💡 Feature Requests

For feature requests, please include:

1. **Problem Description**
   - What problem does this solve?
   - Who would benefit from this?

2. **Proposed Solution**
   - How should it work?
   - Any implementation ideas?

3. **Alternatives Considered**
   - Other solutions explored
   - Why this approach is preferred

## 📞 Getting Help

- **GitHub Issues**: For bugs and feature requests
- **Discussions**: For questions and general discussion
- **Email**: For security issues (use private channels)

## 🎉 Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project documentation

Thank you for contributing! 🚀
