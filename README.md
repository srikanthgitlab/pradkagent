# PradkAgent - GitHub-Integrated Stock Market Assistant

A helpful stock market assistant powered by Google's ADK (Agent Development Kit) with optional GitHub integration capabilities.

## Features

- **Stock Market Analysis**: Get insights and information about stocks and markets
- **GitHub Integration** (optional): Interact with GitHub repositories, manage issues, create pull requests, and work with repository files
- **Powered by Gemini 2.0 Flash**: Uses Google's latest AI model for intelligent responses

## Setup

### 1. Clone and Install Dependencies

```powershell
# Run the setup script
.\setup.ps1

# Or manually:
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure GitHub Integration (Optional)

To enable GitHub functionality:

1. Create a GitHub Personal Access Token at https://github.com/settings/tokens
2. Required scopes: `repo`, `read:user`
3. Add your token to the `.env` file:

```env
GITHUB_TOKEN=your_github_token_here
```

## Usage

### Running the Agent

```powershell
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Run the agent
adk run prgitagent
```

### Available Capabilities

#### Stock Market Features
- Market analysis and insights
- Stock information and trends
- Financial data interpretation

#### GitHub Features (when configured)
- **Repository Management**: Get repository information
- **Issue Management**: 
  - List issues: "Show me open issues in owner/repo"
  - Get specific issue: "Get issue #123 from owner/repo"
  - Comment on issues: "Comment on issue #123 in owner/repo"
- **File Operations**:
  - Read files: "Read the README.md from owner/repo"
  - Create files: "Create a new file in owner/repo"
  - Update files: "Update file.py in owner/repo"
- **Pull Requests**: Create and manage pull requests

### Example Queries

```
# Stock market queries
"What's the current trend in tech stocks?"
"Analyze the performance of Tesla stock"

# GitHub queries (when configured)
"Show me the open issues in microsoft/vscode"
"Read the package.json file from facebook/react"
"Create an issue in my-username/my-repo about bug fixes needed"
```

## Project Structure

```
├── .env                    # Environment variables (GitHub token)
├── .gitignore             # Git ignore file
├── requirements.txt       # Python dependencies
├── setup.ps1             # Setup script for Windows
├── prgitagent/
│   ├── __init__.py
│   └── agent.py          # Main agent implementation
└── README.md             # This file
```

## Dependencies

- **google-adk**: Google Agent Development Kit
- **langchain & langchain-community**: For GitHub integration
- **PyGithub**: GitHub API wrapper
- **python-dotenv**: Environment variable management
- **pandas**: Data analysis (for stock market features)

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_TOKEN` | GitHub Personal Access Token | Optional (for GitHub features) |

## Security

- **Never commit your `.env` file** to version control
- The `.env` file is already included in `.gitignore`
- Use `.env.example` as a template for required variables
- **Immediately revoke any accidentally exposed tokens** at https://github.com/settings/tokens
- Store sensitive credentials only in environment variables

## Troubleshooting

### Windows Privilege Error
If you encounter `OSError: [WinError 1314]`, run PowerShell as Administrator or enable Windows Developer Mode in Settings.

### GitHub Token Issues
- Ensure your token has the correct scopes (`repo`, `read:user`)
- Check that the token is correctly set in your `.env` file
- The agent will show a warning if GitHub integration is not available

### Import Errors
Make sure all dependencies are installed:
```powershell
pip install -r requirements.txt
```

## Development

The agent uses a modular design where GitHub tools are conditionally loaded based on environment configuration. This ensures the agent works even without GitHub integration.

### Key Components

- **Agent Configuration**: Uses Gemini 2.0 Flash model
- **Tool Integration**: GitHub tools are dynamically loaded
- **Error Handling**: Graceful fallback when GitHub is not configured
- **Best Practices**: Environment variables, proper error handling, and modular design

## License

This project follows the licensing terms of the Google ADK and its dependencies.
