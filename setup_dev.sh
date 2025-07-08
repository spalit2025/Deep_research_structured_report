#!/bin/bash
# Development Environment Setup Script
# Run this script to set up code quality tools and pre-commit hooks

set -e

echo "🚀 Setting up development environment for Deep Research Report Agent..."

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not found. Please install Python 3.8 or higher."
    exit 1
fi

# Install development dependencies
echo "📦 Installing development dependencies..."
pip install -r requirements-dev.txt

# Install pre-commit hooks
echo "🔧 Installing pre-commit hooks..."
pre-commit install

# Migrate pre-commit config if needed
echo "🔄 Migrating pre-commit configuration..."
pre-commit migrate-config || true

# Run initial code formatting
echo "🎨 Applying code formatting..."
black .
ruff check --fix .

# Verify setup
echo "✅ Running initial code quality checks..."
echo "Running Black format check..."
black --check . || echo "⚠️  Some files need formatting (will be fixed automatically on commit)"

echo "Running Ruff linting..."
ruff check . || echo "⚠️  Some linting issues found (many will be fixed automatically on commit)"

echo ""
echo "🎉 Development environment setup complete!"
echo ""
echo "📋 What's been set up:"
echo "  ✓ Code formatting with Black"
echo "  ✓ Linting with Ruff"
echo "  ✓ Pre-commit hooks for automatic quality checks"
echo "  ✓ Type checking with MyPy (advisory)"
echo "  ✓ Security scanning with Bandit"
echo ""
echo "🔍 Available commands:"
echo "  black .                    # Format all code"
echo "  ruff check --fix .         # Lint and auto-fix issues"
echo "  pre-commit run --all-files # Run all quality checks"
echo "  pytest                     # Run tests (when available)"
echo ""
echo "⚡ Quick development workflow:"
echo "  1. Make your changes"
echo "  2. Git add and commit (hooks will run automatically)"
echo "  3. Fix any issues reported by the hooks"
echo "  4. Push your changes"
echo ""
echo "📚 See README.md for more information about the codebase."
