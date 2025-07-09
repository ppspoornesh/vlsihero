# Contributing to VLSI Hero

Thank you for your interest in contributing to VLSI Hero! This document provides guidelines for contributing to the project.

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally
3. Create a virtual environment and install dependencies
4. Make your changes
5. Test your changes
6. Submit a pull request

## Development Setup

### Prerequisites
- Python 3.11 or higher
- Node.js 18 or higher
- PostgreSQL 12 or higher

### Installation
```bash
git clone https://github.com/yourusername/vlsi-hero.git
cd vlsi-hero
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
npm install
```

### Database Setup
```bash
# Create a PostgreSQL database
createdb vlsi_hero

# Set environment variable
export DATABASE_URL="postgresql://username:password@localhost/vlsi_hero"

# Initialize database
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

### Running the Application
```bash
python main.py
```

## Code Style

### Python
- Use Black for code formatting
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes

### JavaScript
- Use ES6+ features
- Follow consistent naming conventions
- Comment complex algorithms
- Use modern async/await syntax

### CSS
- Use Tailwind CSS utility classes
- Follow BEM methodology for custom CSS
- Maintain responsive design principles

## Testing

Before submitting a pull request, ensure:
- All existing tests pass
- New functionality includes tests
- Code is properly formatted
- Database migrations work correctly

## Pull Request Process

1. Create a descriptive branch name (`feature/add-new-quiz-type`)
2. Make atomic commits with clear messages
3. Update documentation as needed
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit pull request with detailed description

## Issues

When reporting issues:
- Use the issue templates
- Provide detailed reproduction steps
- Include browser/OS information
- Add relevant screenshots or logs

## Feature Requests

For new features:
- Check existing issues first
- Provide clear use cases
- Discuss implementation approach
- Consider backward compatibility

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help others learn and grow
- Follow the project's coding standards

## License

By contributing, you agree that your contributions will be licensed under the MIT License.