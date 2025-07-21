# Security

## Security Policy

This project is designed for educational purposes and learning observability practices. We take security seriously and have implemented several measures to ensure the safety of users.

## Security Measures

### Pre-commit Hooks
- **Code Formatting**: Black and isort ensure consistent code style
- **File Checks**: Trailing whitespace, end-of-file, YAML/JSON validation
- **Conflict Detection**: Merge conflict detection
- **Large File Detection**: Prevents accidental commits of large files
- **Debug Statement Detection**: Removes debug statements from production code

### Secrets Detection
- **Baseline Scanning**: Regular secrets scanning with detect-secrets
- **No Hardcoded Secrets**: All credentials are either defaults or environment variables
- **Public Repository Safe**: All sensitive data has been removed

### Dependencies
- **UV Package Manager**: Modern, secure Python package management
- **Locked Dependencies**: All dependencies are locked to specific versions
- **Regular Updates**: Dependencies can be updated with `uv lock --upgrade`

## Default Credentials

⚠️ **Important**: This project uses default credentials for demonstration purposes only:

- **Grafana**: admin/admin
- **Application**: No authentication (development only)

**Do not use these credentials in production environments!**

## Reporting Security Issues

If you discover a security vulnerability, please:

1. **Do not create a public issue**
2. **Email**: [Your email here]
3. **Include**: Detailed description and steps to reproduce

## Best Practices for Production Use

1. **Change Default Passwords**: Always change default credentials
2. **Use Environment Variables**: Store secrets in environment variables
3. **Network Security**: Restrict access to monitoring endpoints
4. **Regular Updates**: Keep dependencies updated
5. **Access Control**: Implement proper authentication and authorization
6. **TLS/SSL**: Use HTTPS in production environments

## Compliance

This project is designed for educational use and may not meet all production security requirements. Always review and adapt security measures for your specific use case.
