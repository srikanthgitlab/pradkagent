# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os
from typing import List, Optional
from google.adk import Agent
from dotenv import load_dotenv
from github import Github

# Load environment variables from the same directory as this file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def list_repository_contents(repository: str = "", path: str = "") -> str:
    """
    List files and directories in a GitHub repository.
    
    Args:
        repository: Repository in format 'owner/repo'. If empty, uses default from env.
        path: Directory path to list. If empty, lists root directory.
    
    Returns:
        String containing the list of files and directories.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return "Error: GitHub token not configured"
    
    github_repository = repository if repository else os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    try:
        g = Github(github_token)
        repo = g.get_repo(github_repository)
        
        # Get contents of the specified path
        contents = repo.get_contents(path)
        
        result = f"Contents of {github_repository}/{path if path else 'root'}:\n"
        
        for content in contents:
            if content.type == "dir":
                result += f"📁 {content.path}/\n"
            else:
                result += f"📄 {content.path}\n"
        
        g.close()
        return result
        
    except Exception as e:
        return f"Error listing repository contents: {str(e)}"

def get_file_content(repository: str = "", path: str = "") -> str:
    """
    Get the content of a specific file from a GitHub repository.
    
    Args:
        repository: Repository in format 'owner/repo'. If empty, uses default from env.
        path: File path to read.
    
    Returns:
        String containing the file content.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return "Error: GitHub token not configured"
    
    if not path:
        return "Error: File path is required"
    
    github_repository = repository if repository else os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    try:
        g = Github(github_token)
        repo = g.get_repo(github_repository)
        
        # Get file content
        file_content = repo.get_contents(path)
        
        if file_content.type != "file":
            return f"Error: {path} is not a file"
        
        # Decode content
        content = file_content.decoded_content.decode('utf-8')
        
        result = f"Content of {github_repository}/{path}:\n"
        result += "=" * 50 + "\n"
        result += content
        
        g.close()
        return result
        
    except Exception as e:
        return f"Error reading file content: {str(e)}"

def test_github_connection(repository: str = "") -> str:
    """
    Test GitHub connection and list files in repository root.
    Based on the test_github.py functionality.
    
    Args:
        repository: Repository in format 'owner/repo'. If empty, uses default from env.
    
    Returns:
        String containing connection test results and file listing.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return "Error: GitHub token not configured"
    
    github_repository = repository if repository else os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    try:
        # Initialize PyGithub with personal access token
        g = Github(github_token)
        
        # Get the repository
        repo = g.get_repo(github_repository)
        
        # List files in the root directory
        contents = repo.get_contents("")
        
        result = f"GitHub connection successful for repository: {github_repository}\n\n"
        result += "Files in repository root:\n"
        
        for content in contents:
            result += f"- {content.path}\n"
        
        g.close()
        return result
        
    except Exception as e:
        return f"Error testing GitHub connection: {str(e)}"

def get_repository_info(repository: str = "") -> str:
    """
    Get basic information about a GitHub repository.
    
    Args:
        repository: Repository in format 'owner/repo'. If empty, uses default from env.
    
    Returns:
        String containing repository information.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return "Error: GitHub token not configured"
    
    github_repository = repository if repository else os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    try:
        g = Github(github_token)
        repo = g.get_repo(github_repository)
        
        result = f"Repository Information for {github_repository}:\n"
        result += "=" * 50 + "\n"
        result += f"Name: {repo.name}\n"
        result += f"Description: {repo.description or 'No description'}\n"
        result += f"Language: {repo.language or 'Not specified'}\n"
        result += f"Stars: {repo.stargazers_count}\n"
        result += f"Forks: {repo.forks_count}\n"
        result += f"Open Issues: {repo.open_issues_count}\n"
        result += f"Default Branch: {repo.default_branch}\n"
        result += f"Created: {repo.created_at}\n"
        result += f"Last Updated: {repo.updated_at}\n"
        result += f"Private: {repo.private}\n"
        
        g.close()
        return result
        
    except Exception as e:
        return f"Error getting repository info: {str(e)}"

# Determine which tools to include based on GitHub token availability
def get_available_tools() -> List:
    """Get available tools based on configuration."""
    tools = []
    
    github_token = os.getenv("GITHUB_TOKEN")
    if github_token and github_token != "your_github_token_here":
        # GitHub tools are available
        tools.extend([
            list_repository_contents,
            get_file_content,
            test_github_connection,
            get_repository_info,
        ])
        print("GitHub integration enabled with GitHub tools available.")
    else:
        print("Warning: GitHub token not configured. GitHub tools will not be available.")
        print("To enable GitHub integration:")
        print("1. Create a GitHub Personal Access Token at https://github.com/settings/tokens")
        print("2. Add it to your .env file: GITHUB_TOKEN=your_token_here")
    
    return tools

# Get available tools
available_tools = get_available_tools()

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant for user questions with GitHub integration capabilities.',
    instruction="""You are a helpful assistant with GitHub integration capabilities. 
    
    You can help users with:
    1. General questions and assistance
    2. GitHub repository management (if configured)
    3. Reading and analyzing code from GitHub repositories
    4. Testing GitHub connections
    
    Available GitHub capabilities (when configured):
    - List repository contents: Use list_repository_contents() to see files and directories
    - Get file content: Use get_file_content() to read specific files
    - Test GitHub connection: Use test_github_connection() to verify connectivity
    - Get repository info: Use get_repository_info() to get repository details
    
    When working with repositories:
    - If no repository is specified, the default repository from environment variables will be used
    - Repository format should be 'owner/repo' (e.g., 'microsoft/vscode')
    - For file paths, use forward slashes even on Windows
    
    Be concise and helpful. If you don't know something, just say so.
    If GitHub tools are not available, inform the user and guide them to configure their GitHub token.
    """,
    tools=available_tools,
)
