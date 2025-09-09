# LangGraph research paper generation

A sophisticated research paper generation system built with LangGraph that demonstrates parallel processing capabilities for creating comprehensive academic documents. This agent uses a multi-node workflow to generate, write, and synthesize research paper sections in parallel, showcasing the power of LangGraph's parallelization features.

## 🚀 Features

- **Parallel Section Writing**: Multiple sections are written simultaneously using LangGraph's `Send` functionality
- **Structured Output**: Uses Pydantic models for type-safe data handling
- **Template-Driven**: Configurable document templates for consistent structure
- **AI-Powered Content Generation**: Leverages GPT-4 for high-quality academic writing
- **Modular Architecture**: Clean separation of concerns with dedicated nodes for each task

## 🏗️ Architecture

The system follows a three-stage pipeline:

```
Topic Input → Section Generation → Parallel Section Writing → Synthesis → Final Report
```

### Workflow Components

1. **Section Generator** (`generate_sections.py`)

   - Analyzes the input topic and template
   - Generates structured section outlines with titles and descriptions
   - Uses structured LLM output for consistent formatting

2. **Section Writers** (`section_writer.py`)

   - **Parallel execution**: Multiple section writers run simultaneously
   - Each writer focuses on a single section
   - Produces well-formatted Markdown content
   - Maintains academic writing standards

3. **Synthesizer** (`synthesizer.py`)
   - Combines all completed sections
   - Creates the final comprehensive report
   - Ensures proper document structure

## 📋 Prerequisites

- Python 3.13+
- OpenAI API key
- UV package manager (recommended)

## 🛠️ Installation

1. **Clone the repository**

   ```bash
   git clone https://github.com/jameskanyiri/LangGraph-research-paper-generation.git
   cd langgraph_parallelization_eval_agent
   ```

2. **Install dependencies**

   ```bash
   uv sync
   ```

3. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

## 🚀 Usage

### Basic Usage

```python
from src.agent import graph
from src.configuration import Configuration

# Configure the agent
config = {
    "configurable": {
        "template": "Your custom template here..."
    }
}

# Run the agent
result = await graph.ainvoke(
    {"topic": "Your research topic here"},
    config=config
)

print(result["final_report"])
```

## ⚙️ Configuration

### Custom Templates

The system uses a configurable template system. You can customize the document structure by modifying the `template` field in the configuration:

```python
custom_template = """
# Your Custom Research Paper Template

## 1. Executive Summary
- High-level overview and key findings

## 2. Problem Statement
- Clear definition of the research problem

## 3. Solution Approach
- Detailed methodology and approach

## 4. Results and Analysis
- Findings and their interpretation

## 5. Conclusion
- Summary and future directions
"""
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🙏 Acknowledgments

- Built with [LangGraph](https://github.com/langchain-ai/langgraph) for workflow orchestration
- Powered by [LangChain](https://github.com/langchain-ai/langchain) for LLM integration
- Uses [OpenAI's GPT-4](https://openai.com/gpt-4) for content generation

## 📞 Support

For questions, issues, or contributions, please:

1. Check the [Issues](https://github.com/your-repo/issues) page
2. Create a new issue with detailed information
3. Contact the maintainers

---

**Note**: This project is designed for research and evaluation purposes. Ensure you have appropriate API keys and follow usage guidelines for all integrated services.
