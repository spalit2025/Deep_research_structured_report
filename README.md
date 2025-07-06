# Deep Research Structured Report Agent

An AI-powered research report generator that creates comprehensive, structured reports using Generative AI and web search capabilities.

## Features

- **Multiple Report Templates**: Business, Academic, Technical, Quick, and Standard formats
- **AI-Powered Research**: Automated web search and information gathering
- **Smart Token Management**: Optimizes content for context windows with intelligent truncation
- **Rich Output**: Professional markdown reports with citations and sources
- **Interactive Mode**: User-friendly CLI interface with rich console output
- **Built-in Rate Limiting**: Automatic API rate limiting prevents service interruptions
- **Customizable**: Configurable templates and sections

## Quick Start

1. **Clone the repository**:
   ```bash
   git clone https://github.com/spalit2025/Deep_research_structured_report.git
   cd Deep_research_structured_report
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements_txt.txt
   ```

3. **Set up environment variables**:
   ```bash
   cp env_template.sh .env
   ```
   Edit `.env` and add your API keys:
   - `ANTHROPIC_API_KEY`: Your Anthropic API key
   - `TAVILY_API_KEY`: Your Tavily search API key

4. **Run the application**:
   ```bash
   # Interactive mode
   python main.py
   
   # Generate a single report
   python main.py "Your research topic here"
   
   # Use specific template
   python main.py "AI in healthcare" --template business
   ```

## Available Templates

- **Standard**: Balanced research report with intro, main sections, conclusion
- **Business**: Executive summary, market analysis, strategic recommendations
- **Academic**: Abstract, literature review, analysis, conclusions
- **Technical**: Technical overview, specifications, implementation details
- **Quick**: Shorter sections, faster generation, concise format

## Example Usage

```bash
# Generate a business report on AI in accounting
python main.py "application of gen ai in corporate accounting" --template business

# Generate a technical report
python main.py "Machine Learning in Finance" --template technical

# Generate a quick report
python main.py "AI Ethics Overview" --template quick
```

## Project Structure

```
├── main.py                 # Main entry point
├── report_generator.py     # Core report generation logic
├── config.py              # Configuration management
├── prompts/               # AI prompts for different templates
│   ├── planning.py        # Structure planning prompts
│   └── writing.py         # Content writing prompts
├── utils/                 # Utility functions
│   └── prompt_loader.py   # Prompt loading utilities
├── generated_reports/     # Output directory (gitignored)
└── requirements_txt.txt   # Python dependencies
```

## Configuration

The application uses a flexible configuration system that allows customization of:
- Report templates and sections
- Word counts and formatting
- AI model parameters
- Search parameters

## API Keys Required

- **Anthropic API**: For Claude AI text generation
- **Tavily API**: For web search capabilities

## Rate Limiting & Reliability

The application includes built-in rate limiting to prevent API service interruptions:

- **Automatic Delays**: 1.0s between Anthropic calls, 0.5s between Tavily calls
- **Retry Mechanisms**: Exponential backoff for failed requests (up to 3 retries)
- **Configurable**: Rate limits can be adjusted in configuration settings
- **No Batch Mode**: Removed to prevent rapid successive calls that trigger rate limits

## Smart Token Management

The application includes intelligent context window management to prevent token limit overruns:

- **Dynamic Source Optimization**: Automatically adjusts source content length based on context window
- **Intelligent Truncation**: Preserves complete sentences and paragraphs when possible
- **Template-Specific Limits**: Different token budgets for different report types
- **Usage Monitoring**: Real-time token usage reporting with warnings for high usage
- **Fallback Strategies**: Graceful degradation when content exceeds limits

### Token Management Features

| Feature | Description |
|---------|-------------|
| **Context Window Support** | Supports Claude 3.5 Sonnet (200k tokens) and other models |
| **Dynamic Source Allocation** | Distributes 60-70% of available tokens to research sources |
| **Intelligent Truncation** | Preserves sentence and paragraph boundaries when truncating |
| **Template Optimization** | Academic reports get more source content than quick reports |
| **Usage Reporting** | Shows token usage percentage and warns at 85%+ usage |

## Output

Reports are saved in the `generated_reports/` directory in markdown format with:
- Professional formatting
- Proper citations and sources
- Rich content structure
- Timestamped filenames

## License

MIT License - feel free to use and modify as needed.

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and questions, please open an issue on GitHub. 