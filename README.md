# Transform your $20 Cursor into a Devin-like AI Assistant

This repository gives you everything needed to supercharge your Cursor or Windsurf IDE with **advanced** agentic AI capabilities—similar to the $500/month Devin—but at a fraction of the cost. In under a minute, you’ll gain:

* Automated planning and self-evolution, so your AI “thinks before it acts” and learns from mistakes
* Extended tool usage, including web browsing, search engine queries, and LLM-driven text/image analysis
* [Experimental] Multi-agent collaboration, with o1 doing the planning, and regular Claude/GPT-4o doing the execution.

## Why This Matters

Devin impressed many by acting like an intern who writes its own plan, updates that plan as it progresses, and even evolves based on your feedback. But you don’t need Devin’s $500/month subscription to get most of that functionality. By customizing the .cursorrules file, plus a few Python scripts, you’ll unlock the same advanced features inside Cursor.

## Key Highlights

1.	Easy Setup
   
   Copy the provided config files into your project folder. Cursor users only need the .cursorrules file. It takes about a minute, and you’ll see the difference immediately.

2.	Planner-Executor Multi-Agent (Experimental)

   Our new [multi-agent branch](https://github.com/grapeot/devin.cursorrules/tree/multi-agent) introduces a high-level Planner (powered by o1) that coordinates complex tasks, and an Executor (powered by Claude/GPT) that implements step-by-step actions. This two-agent approach drastically improves solution quality, cross-checking, and iteration speed.

3.	Extended Toolset

   Includes:
   
   * Web scraping (Playwright)
   * Search engine integration (DuckDuckGo)
   * LLM-powered analysis

   The AI automatically decides how and when to use them (just like Devin).

4.	Self-Evolution

   Whenever you correct the AI, it can update its “lessons learned” in .cursorrules. Over time, it accumulates project-specific knowledge and gets smarter with each iteration. It makes AI a coachable and coach-worthy partner.
	
## Usage

1. Copy all files from this repository to your project folder
2. For Cursor users: The `.cursorrules` file will be automatically loaded
3. For Windsurf users: Use both `.windsurfrules` and `scratchpad.md` for similar functionality

## Setup

1. Create Python virtual environment:
```bash
# Create a virtual environment in ./venv
python3 -m venv venv

# Activate the virtual environment
# On Unix/macOS:
source venv/bin/activate
# On Windows:
.\venv\Scripts\activate
```

2. Configure environment variables:
```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your API keys and configurations
```

3. Install dependencies:
```bash
# Install required packages
pip install -r requirements.txt

# Install Playwright's Chromium browser (required for web scraping)
python -m playwright install chromium
```

## Tools Included

### LLM Integration
- Multi-provider support (OpenAI, Anthropic, Deepseek, Google, Azure)
- Local LLM deployment options
- Flexible API configuration
- Comprehensive error handling

### Web Tools
- Advanced web scraping with JavaScript support (using Playwright)
- Concurrent webpage processing
- Search engine integration with dual providers:
  - Serper API (Google search results)
  - DuckDuckGo (fallback)
- Intelligent content extraction and formatting

### Data Management
- SQLite database operations
  - Query execution with parameterization
  - SQL script execution
  - CSV import/export capabilities
  - Transaction support
- Automatic schema generation
- Data validation and error handling

### Content Analysis
- YouTube video processing
  - Transcript extraction
  - Content summarization
  - Multiple URL format support
  - Multilingual capabilities

### System Integration
- Calendar management (macOS)
  - Event creation and scheduling
  - Multiple calendar support
  - Flexible time format handling
- File system operations
- Process handling

## Testing

The project includes comprehensive unit tests for all tools. To run the tests:

```bash
# Make sure you're in the virtual environment
source venv/bin/activate  # On Windows: .\venv\Scripts\activate

# Run all tests
PYTHONPATH=. python -m unittest discover tests/
```

The test suite includes:
- Search engine tests (DuckDuckGo and Serper API integration)
- Web scraper tests (Playwright-based scraping)
- LLM API tests (Multiple provider integration)
- SQLite operations tests
- YouTube content analysis tests
- Calendar integration tests

## Background

For detailed information about the motivation and technical details behind this project, check out the blog post: [Turning $20 into $500 - Transforming Cursor into Devin in One Hour](https://yage.ai/cursor-to-devin-en.html)

## License

MIT License
