# Deep Research Structured Report Agent

An AI-powered research report generator that creates comprehensive, structured reports using Generative AI and web search capabilities.

## Features

- **Multiple Report Templates**: Business, Academic, Technical, Quick, and Standard formats
- **AI-Powered Research**: Automated web search and information gathering
- **Rich Output**: Professional markdown reports with citations and sources
- **Interactive Mode**: User-friendly CLI interface with rich console output
- **Batch Processing**: Generate multiple reports at once
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
   
   # Batch mode
   python main.py --batch "Topic 1" "Topic 2" "Topic 3" --template academic
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

# Generate multiple academic reports
python main.py --batch "Machine Learning in Finance" "AI Ethics" "Quantum Computing" --template academic
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