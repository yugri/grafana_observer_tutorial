# Contributing to Observer

Thank you for your interest in contributing to the Observer project! This document provides guidelines for contributing effectively.

## 🚀 Quick Start

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature-name`
3. Make your changes
4. Write conventional commit messages
5. Run tests: `uv run pytest tests/ -v`
6. Run pre-commit: `uv run pre-commit run --all-files`
7. Submit a pull request

## 📝 Conventional Commits

This project uses **Conventional Commits** to automatically generate release notes. Please follow this format for all commit messages:

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

### Commit Types

| Type | Description | Example |
|------|-------------|---------|
| `feat` | A new feature | `feat: add user authentication` |
| `fix` | A bug fix | `fix: resolve memory leak in metrics collection` |
| `docs` | Documentation changes | `docs: update README with new endpoints` |
| `style` | Code style changes (formatting, etc.) | `style: format code with black` |
| `refactor` | Code refactoring | `refactor: extract metrics logic into separate module` |
| `perf` | Performance improvements | `perf: optimize database queries` |
| `test` | Adding or updating tests | `test: add integration tests for API endpoints` |
| `chore` | Maintenance tasks | `chore: update dependencies` |
| `ci` | CI/CD changes | `ci: add security scanning step` |
| `build` | Build system changes | `build: update Docker configuration` |
| `revert` | Revert previous commit | `revert: revert "feat: add user authentication"` |

### Scopes (Optional)

You can specify a scope to provide more context:

```
feat(api): add user authentication endpoint
fix(metrics): resolve memory leak in Prometheus collector
docs(readme): update installation instructions
```

### Breaking Changes

To indicate a breaking change, add `!` after the type/scope and include `BREAKING CHANGE:` in the body:

```
feat!: change API response format

BREAKING CHANGE: The /users endpoint now returns user objects instead of arrays.
```

### Examples

#### Good Commit Messages

```bash
# Feature
git commit -m "feat: add Prometheus metrics endpoint"

# Bug fix with scope
git commit -m "fix(api): handle null values in request body"

# Documentation
git commit -m "docs: add troubleshooting section to README"

# Breaking change
git commit -m "feat!: change authentication method

BREAKING CHANGE: JWT tokens are now required for all API endpoints."

# Multiple lines
git commit -m "feat(monitoring): add custom alerting rules

- Add high error rate alert
- Add response time threshold alert
- Configure alert notification channels"
```

#### Bad Commit Messages

```bash
# Too vague
git commit -m "fix stuff"

# No type
git commit -m "updated README"

# Too long without structure
git commit -m "This commit fixes a critical bug in the authentication system where users were not being properly validated and also adds some new features to the monitoring dashboard and updates the documentation to reflect these changes"
```

## 🧪 Testing

Before submitting your changes, ensure all tests pass:

```bash
# Run all tests
uv run pytest tests/ -v

# Run with coverage
uv run pytest tests/ -v --cov=.

# Run specific test file
uv run pytest tests/test_basic.py -v
```

## 🔍 Code Quality

Run pre-commit hooks to ensure code quality:

```bash
# Run all pre-commit hooks
uv run pre-commit run --all-files

# Run specific hook
uv run pre-commit run black --all-files
```

## 📋 Pull Request Guidelines

1. **Title**: Use conventional commit format (e.g., "feat: add user authentication")
2. **Description**: Clearly describe what the PR does and why
3. **Tests**: Include tests for new features or bug fixes
4. **Documentation**: Update documentation if needed
5. **Screenshots**: Include screenshots for UI changes

### PR Template

```markdown
## Description
Brief description of what this PR does.

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Code refactoring
- [ ] Performance improvement
- [ ] Other

## Testing
- [ ] Unit tests pass
- [ ] Integration tests pass
- [ ] Manual testing completed

## Checklist
- [ ] Code follows project style guidelines
- [ ] Self-review completed
- [ ] Documentation updated
- [ ] No breaking changes (or breaking changes documented)
```

## 🚀 Release Process

Releases are automatically created when code is pushed to the `main` branch. The release notes are generated from conventional commits since the last release.

### 📈 Semantic Versioning

This project uses **automatic semantic versioning** based on your commit types:

| Commit Type | Version Bump | Example |
|-------------|--------------|---------|
| `feat!` or `BREAKING CHANGE:` | **MAJOR** (1.0.0 → 2.0.0) | Breaking API changes |
| `feat:` | **MINOR** (1.0.0 → 1.1.0) | New features |
| `fix:`, `docs:`, `style:`, etc. | **PATCH** (1.0.0 → 1.0.1) | Bug fixes, docs |

**Examples**:
```bash
# Major version bump (breaking change)
git commit -m "feat!: change authentication method"

# Minor version bump (new feature)
git commit -m "feat: add user dashboard"

# Patch version bump (bug fix)
git commit -m "fix: resolve login issue"
```

### Manual Release (if needed)

```bash
# Update version in .version file
# Create and push tag
git tag -a v1.2.0 -m "Release v1.2.0"
git push origin v1.2.0
```

## 🤝 Getting Help

- **Issues**: Use GitHub issues for bug reports and feature requests
- **Discussions**: Use GitHub Discussions for questions and ideas
- **Documentation**: Check [README.md](README.md) and [TUTORIAL.md](TUTORIAL.md)

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.
