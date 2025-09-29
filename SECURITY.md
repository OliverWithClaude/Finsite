# Security Policy

## Supported Versions

Currently supporting the following versions with security updates:

| Version | Supported          |
| ------- | ------------------ |
| 1.1.x   | :white_check_mark: |
| 1.0.x   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability within Finsite, please send an email to security@finsite.example. All security vulnerabilities will be promptly addressed.

Please do not report security vulnerabilities through public GitHub issues.

## Security Measures

This application implements several security measures:

1. **Input Validation**: All user inputs are validated and sanitized
2. **SQL Injection Prevention**: Using SQLAlchemy ORM with parameterized queries
3. **CORS Configuration**: Properly configured for local development
4. **Rate Limiting**: Consider implementing rate limiting for production deployments
5. **Authentication**: Currently designed for local use; add authentication for public deployment

## Best Practices for Deployment

If deploying this application publicly:

1. **Use HTTPS**: Always serve the application over HTTPS
2. **Add Authentication**: Implement user authentication and authorization
3. **Environment Variables**: Store sensitive configuration in environment variables
4. **Rate Limiting**: Implement rate limiting on API endpoints
5. **Input Validation**: Review and strengthen input validation
6. **Database Security**: Use proper database credentials and encryption
7. **API Keys**: If using external APIs, secure your API keys properly
