# Deep Research Report Agent

A sophisticated AI-powered research report generator that creates comprehensive, well-structured documents on any topic. The system leverages advanced web search, intelligent caching, smart token management, and prompt versioning to deliver high-quality research reports.

## 🚀 Key Features

- **Multiple Report Templates**: Business, Academic, Technical, Quick, and Standard formats
- **Advanced Search Integration**: Powered by Tavily API for comprehensive research
- **Smart Caching System**: Reduces API calls by 70-90% with intelligent query similarity detection
- **Token Management**: Optimized for Claude 3.5 Sonnet with automatic context window management
- **Prompt Versioning**: A/B test and track performance of different prompt versions
- **Rate Limiting**: Built-in protections against API service interruptions
- **Robust JSON Parsing**: Handles varied AI response formats gracefully

## 🆕 New: Prompt Versioning System

The system now includes a comprehensive prompt versioning and analytics platform:

- **Version Management**: Create, manage, and switch between different prompt versions
- **Performance Analytics**: Track success rates, quality scores, and usage patterns
- **A/B Testing**: Test different prompt approaches and automatically identify best performers
- **Migration Tools**: Seamlessly migrate from static prompts to versioned system
- **CLI Management**: Command-line interface for prompt version operations

### Prompt Versioning Quick Start

```bash
# Initialize the versioning system
python initialize_prompt_versioning.py

# List all prompt versions
python prompt_cli.py list

# View analytics for a specific prompt
python prompt_cli.py analytics -p SECTION_WRITER_PROMPT

# Add a new prompt version
python prompt_cli.py add SECTION_WRITER_PROMPT v2.0 "Your improved prompt..." -d "Better formatting"

# Set active version
python prompt_cli.py set-active SECTION_WRITER_PROMPT v2.0

# Test a prompt version
python prompt_cli.py test SECTION_WRITER_PROMPT v2.0 "AI in healthcare"
```

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/spalit2025/Deep_research_structured_report.git
cd Deep_research_structured_report
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
# Create .env file with your API keys
ANTHROPIC_API_KEY=your_anthropic_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

4. Initialize prompt versioning (optional):
```bash
python initialize_prompt_versioning.py
```

## 📊 Usage Examples

### Basic Report Generation

```bash
# Generate a business report
python main.py --topic "AI in healthcare" --template business

# Generate an academic report
python main.py --topic "quantum computing" --template academic

# Quick report with verbose output
python main.py --topic "renewable energy" --template quick --verbose
```

### Advanced Features

```bash
# Generate with custom configuration
python main.py --topic "blockchain technology" --template business --config custom_config.json

# Use specific prompt version
python main.py --topic "AI ethics" --template academic --prompt-version v2.0_enhanced
```

## 🏗️ System Architecture

### Core Components

1. **Report Generator** (`report_generator.py`): Main orchestrator for report generation
2. **Prompt System** (`utils/prompt_loader.py`): Manages prompt templates and versioning
3. **Search Engine** (`utils/search_cache.py`): Handles web search with intelligent caching
4. **Token Manager** (`utils/token_manager.py`): Optimizes content for AI model limits
5. **JSON Parser** (`utils/json_parser.py`): Robust parsing of AI responses

### New: Prompt Versioning System

- **Version Manager** (`utils/prompt_versioning.py`): Core versioning and analytics engine
- **CLI Tool** (`prompt_cli.py`): Command-line interface for management
- **Migration Tool** (`initialize_prompt_versioning.py`): Setup and migration utilities

## 📈 Performance Metrics

### Search Caching
- **Cache Hit Rate**: 70-90% on subsequent runs
- **API Call Reduction**: Significant cost savings
- **Response Time**: Near-instant for cached queries

### Token Management
- **Context Optimization**: Automatic content fitting for Claude 3.5 Sonnet
- **Template-Specific Limits**: Optimized for each report type
- **Real-time Monitoring**: Track token usage throughout generation

### Prompt Versioning
- **A/B Testing**: Compare prompt performance scientifically
- **Analytics Tracking**: Success rates, quality scores, execution times
- **Version Control**: Full history and rollback capabilities

## 🔧 Configuration

### Main Configuration (`config.py`)

```python
{
    "template": "business",           # Report template type
    "prompt_version": "v1.0_static",  # Active prompt version
    "max_content_length": 200000,     # Token management limit
    "enable_search_caching": True,    # Enable intelligent caching
    "enable_prompt_versioning": True, # Enable prompt versioning
    "enable_prompt_analytics": True,  # Track prompt performance
    "cache_ttl_hours": 24.0,         # Cache expiration time
    "similarity_threshold": 0.75      # Cache similarity matching
}
```

### Prompt Versioning Configuration

```python
{
    "prompt_versions_dir": "prompt_versions",  # Version storage directory
    "prompt_usage_log": "prompt_usage.json",  # Analytics log file
    "enable_prompt_analytics": True,          # Performance tracking
    "auto_suggest_best_prompts": False        # Auto-switch to best performers
}
```

## 📚 Report Templates

### Business Template
- Executive Summary
- Market Analysis
- Competitive Landscape
- Strategic Recommendations
- Financial Projections

### Academic Template
- Abstract
- Literature Review
- Methodology
- Results & Analysis
- Conclusions

### Technical Template
- Technical Overview
- Architecture Analysis
- Implementation Details
- Performance Metrics
- Best Practices

### Quick Template
- Condensed format
- Key findings focus
- Rapid generation
- Essential insights only

## 🔍 Search & Research

### Tavily Integration
- Advanced web search capabilities
- Academic and business source prioritization
- Real-time information gathering
- Source citation and verification

### Caching Strategy
- Query similarity detection
- Persistent and in-memory caching
- Configurable TTL and cache size
- Performance monitoring and reporting

## 🎯 Prompt Engineering

### Version Management
- Create and test multiple prompt versions
- Track performance metrics automatically
- A/B test different approaches
- Rollback to previous versions

### Analytics Dashboard
- Success rate tracking
- Quality score monitoring
- Usage pattern analysis
- Performance comparisons

### Best Practices
- Use semantic versioning (v1.0, v1.1, v2.0)
- Document changes in version descriptions
- Test thoroughly before setting as active
- Monitor performance metrics regularly

## 🔧 Development & Code Quality

This project uses modern Python development practices with automated code quality tools.

### Quick Development Setup

```bash
# Run the setup script for automated configuration
./setup_dev.sh

# Or manually install development dependencies
pip install -r requirements-dev.txt
pre-commit install
```

### Code Quality Tools

- **Black**: Automatic code formatting
- **Ruff**: Fast linting, import sorting, and code analysis
- **MyPy**: Static type checking (advisory)
- **Bandit**: Security vulnerability scanning
- **Pre-commit**: Automated quality checks on git commits

### Development Workflow

1. **Make Changes**: Edit code following existing patterns
2. **Format Code**: `black .` (optional - runs automatically on commit)
3. **Check Quality**: `ruff check --fix .` (optional - runs automatically on commit)
4. **Commit**: Git hooks will automatically run quality checks
5. **Fix Issues**: Address any issues reported by the hooks
6. **Push**: Submit your changes

### Available Commands

```bash
# Code formatting and linting
black .                     # Format all Python files
ruff check --fix .          # Lint and auto-fix issues
ruff format .               # Alternative formatter

# Quality checks
pre-commit run --all-files  # Run all quality checks
mypy .                      # Type checking
bandit -r .                 # Security scanning

# Testing (when tests are added)
pytest                      # Run test suite
pytest --cov=.              # Run with coverage
```

### CI/CD Pipeline

GitHub Actions automatically runs:
- **Code Quality**: Black, Ruff, MyPy checks
- **Multi-Python Testing**: Python 3.8-3.12 compatibility
- **Integration Tests**: Core functionality verification
- **Documentation**: README and configuration validation
- **Security**: Bandit security scanning

### Configuration Files

- `pyproject.toml`: Main configuration for tools and project metadata
- `.pre-commit-config.yaml`: Pre-commit hook configuration
- `.github/workflows/ci.yml`: CI/CD pipeline configuration
- `requirements-dev.txt`: Development dependencies

## 🤝 Contributing

1. Fork the repository
2. Run `./setup_dev.sh` to set up development environment
3. Create a feature branch
4. Make changes following code quality standards
5. Test your changes thoroughly (hooks will run automatically)
6. Submit a pull request with detailed description

All contributions must pass the automated quality checks in CI/CD.

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Anthropic for Claude 3.5 Sonnet API
- Tavily for advanced web search capabilities
- Open source community for inspiration and tools

## 📞 Support

For questions, issues, or feature requests:
- Open an issue on GitHub
- Contact: [Your contact information]

---

**Note**: This system requires API keys for Anthropic (Claude) and Tavily. Ensure you have appropriate usage limits and billing set up for production use.
