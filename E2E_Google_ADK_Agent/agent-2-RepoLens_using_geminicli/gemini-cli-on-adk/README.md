# Gemini CLI ADK Agent

An advanced AI agent built with Google's Agent Development Kit (ADK) that integrates the Gemini CLI as a powerful tool for software development lifecycle tasks. The agent can analyze code, generate tests, perform security audits, and provide refactoring recommendations by leveraging the Gemini CLI in non-interactive mode.

## 🚀 Features

- **Code Analysis**: Analyze entire codebases from GitHub repositories
- **Test Generation**: Automatically generate comprehensive unit tests
- **Security Audits**: Identify potential vulnerabilities and security issues
- **Code Review**: Get intelligent code quality suggestions
- **Refactoring**: Receive refactoring recommendations following best practices
- **Documentation**: Generate API documentation and README files
- **Architecture Analysis**: Understand system architecture and component relationships
- **Performance Optimization**: Identify bottlenecks and suggest improvements

## 🏗️ Architecture

The system consists of four main layers:

1. **Presentation Layer**: ADK Web Interface for user interaction
2. **Agent Layer**: ADK Agent with reasoning and tool orchestration
3. **Tool Layer**: Gemini CLI Tool wrapper function
4. **Execution Layer**: Gemini CLI process and git operations

```
User → ADK Web UI → ADK Agent → Gemini CLI Tool → GitHub Repo → Gemini CLI → Results
```

## 📋 Prerequisites

- **Python**: 3.10-3.14
- **Node.js**: 20.x or higher
- **Git**: Latest version
- **Gemini API Key**: Get from [Google AI Studio](https://aistudio.google.com/app/apikey)

## 🛠️ Installation & Setup

### 1. Clone the Repository

```bash
cd gemini-cli-on-adk
```

### 2. Create Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate venv (Windows)
.\venv\Scripts\Activate.ps1

# Activate venv (Unix/Mac)
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -e .
```

### 4. Install Gemini CLI

```bash
npm install -g @google/gemini-cli
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
GEMINI_API_KEY=your-api-key-here
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_CLOUD_LOCATION=us-central1
```

**Get your API Key**: Visit [Google AI Studio](https://aistudio.google.com/app/apikey)

### 6. Run the Agent

```bash
adk web --host 0.0.0.0 --port 8080 .
```

Access the web interface at: **http://localhost:8080**

## 💡 Usage Examples

### Basic Queries

#### 1. Code Analysis
```
Analyze the architecture of https://github.com/username/repo and explain the main components
```

#### 2. Generate Unit Tests
```
Generate comprehensive unit tests for https://github.com/username/repo
```

#### 3. Code Review
```
Review the code quality in https://github.com/username/repo and suggest improvements
```

### Advanced Queries

#### 4. Security Audit
```
Perform a security audit on https://github.com/username/repo and identify potential vulnerabilities
```

#### 5. Performance Analysis
```
Analyze https://github.com/username/repo for performance bottlenecks and suggest optimizations
```

#### 6. API Documentation
```
Generate complete API documentation for https://github.com/username/repo
```

#### 7. Refactoring Recommendations
```
Analyze https://github.com/username/repo and suggest refactoring opportunities following SOLID principles
```

#### 8. Design Patterns
```
Recommend design patterns that could improve https://github.com/username/repo
```

## 🔧 How It Works

1. **User submits a request** through the ADK web interface with a task and GitHub URL
2. **Agent receives the request** and determines it needs to use the Gemini CLI tool
3. **Tool clones the repository** to system temp directory with shallow clone (memory optimized)
4. **Gemini CLI executes** in non-interactive mode with the task prompt
5. **Results are returned** to the agent and presented to the user

### Key Optimizations

- **Shallow Clone**: Uses `--depth 1 --single-branch` to minimize memory usage
- **Git Memory Limits**: Configures git to use max 10-20MB during clone
- **Node.js Memory**: Increases heap size to 4GB for large repositories
- **Repository Caching**: Reuses cloned repositories for subsequent requests
- **Windows Compatibility**: Full path resolution for Gemini CLI on Windows

## 📁 Project Structure

```
gemini-cli-on-adk/
├── app/
│   ├── __init__.py
│   ├── agent.py              # Main agent definition and gemini_cli tool
│   └── agent_engine_app.py   # Agent Engine application
├── deployment/               # Cloud deployment configurations
├── .env                      # Environment variables (create this)
├── Dockerfile                # Container definition
├── pyproject.toml            # Python dependencies
├── uv.lock                   # Locked dependencies
└── README.md                 # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GEMINI_API_KEY` | Gemini API key for authentication | - | Yes |
| `GOOGLE_CLOUD_PROJECT` | GCP project ID (optional) | - | No |
| `GOOGLE_CLOUD_LOCATION` | Region for Vertex AI | us-central1 | No |
| `NODE_OPTIONS` | Node.js memory limit | --max-old-space-size=4096 | No |

### Timeouts

- **Git Clone**: 300 seconds (5 minutes)
- **Gemini CLI Execution**: 600 seconds (10 minutes)

## 🐛 Troubleshooting

### Common Issues

#### 1. "Error cloning repository"
**Cause**: Out of memory during git clone

**Solution**:
- The agent uses shallow clone with memory limits
- Try a smaller repository first
- Increase system virtual memory

#### 2. "Gemini CLI not found"
**Cause**: Gemini CLI not in PATH

**Solution**:
```bash
# Verify installation
npm list -g @google/gemini-cli

# Reinstall if needed
npm install -g @google/gemini-cli
```

#### 3. "Authentication error"
**Cause**: Missing or invalid API key

**Solution**:
- Verify `GEMINI_API_KEY` in `.env` file
- Get a new key from [Google AI Studio](https://aistudio.google.com/app/apikey)
- Restart the server after updating `.env`

#### 4. "Out of memory" error
**Cause**: Large repository or insufficient system memory

**Solution**:
- The agent automatically sets `NODE_OPTIONS=--max-old-space-size=4096`
- Close other applications to free up memory
- Try with a smaller repository

### Debug Mode

Enable detailed logging:
```bash
# Set debug environment variable
$env:DEBUG='*'  # Windows
export DEBUG='*'  # Unix/Mac

# Run the agent
adk web --host 0.0.0.0 --port 8080 .
```

## 🚀 Deployment

### Docker

```bash
# Build image
docker build -t gemini-cli-adk:latest .

# Run container
docker run -p 8080:8080 \
  -e GEMINI_API_KEY=your-api-key \
  gemini-cli-adk:latest
```

### Cloud Run

See `deployment/` folder for Cloud Run deployment configurations.

## 🔐 Security Considerations

- **Public Repositories Only**: Currently supports only public GitHub repositories
- **Repository Isolation**: Each repository is cloned to a unique temp directory
- **Automatic Cleanup**: Failed clones are automatically cleaned up
- **API Key Security**: Store API keys in environment variables, never in code
- **Timeouts**: Strict timeouts prevent resource exhaustion

## 🚧 Limitations

- Only supports public GitHub repositories (private repo support planned)
- Repositories are cached in temp directory (ephemeral storage)
- Maximum repository size limited by available memory
- Gemini CLI tool execution is non-interactive

## 🔮 Future Enhancements

- [ ] Support for private repositories via GitHub tokens
- [ ] Persistent repository caching with Cloud Storage
- [ ] Real-time streaming of Gemini CLI output
- [ ] Support for GitLab, Bitbucket, and other SCM platforms
- [ ] Multi-repository analysis
- [ ] Custom tool configurations
- [ ] Rate limiting and quota management
- [ ] Cost tracking and monitoring

## 📚 Resources

- [Google ADK Documentation](https://cloud.google.com/vertex-ai/docs/agent-builder)
- [Gemini CLI Documentation](https://github.com/google/gemini-cli)
- [Google AI Studio](https://aistudio.google.com/)
- [Cloud Run Documentation](https://cloud.google.com/run/docs)

## 📄 License

Copyright 2025 Google LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📧 Support

For issues and questions:
- Open an issue on GitHub
- Check the troubleshooting section above
- Review the ADK and Gemini CLI documentation

---

**Built with ❤️ using Google's Agent Development Kit (ADK) and Gemini CLI**
