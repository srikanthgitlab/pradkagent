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
import time
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
        g = Github(github_token)
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

def create_file_with_ai_content(file_path: str, requirements: str, file_contents: str, repository: str = "", reference_directory: str = "") -> str:
    """
    Create a file in GitHub repository with provided content.
    Creates a new branch, adds the file, and creates a PR for review.
    
    Args:
        file_path: Path where the file should be created (e.g., 'src/utils/helper.py')
        requirements: Description of what the code should do (for PR documentation)
        file_contents: The actual content to write to the file
        repository: Repository in format 'owner/repo'. If empty, uses default from env.
        reference_directory: Directory to analyze for code patterns (optional)
    
    Returns:
        String containing the result of file creation and PR details.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token:
        return "Error: GitHub token not configured"
    
    if not file_path:
        return "Error: File path is required"
    
    if not file_contents:
        return "Error: File contents are required"
    
    github_repository = repository if repository else os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    try:
        g = Github(github_token)
        repo = g.get_repo(github_repository)
        
        # Generate unique timestamp for the file and branch
        timestamp = int(time.time())
        
        # Create unique branch name
        new_branch_name = f"feature/ai-generated-{timestamp}"
        base_branch = repo.default_branch
        
        # Analyze existing code patterns if reference directory is provided
        reference_analysis = ""
        if reference_directory:
            try:
                ref_contents = repo.get_contents(reference_directory)
                reference_analysis = f"\n\n## Reference Code Analysis\nAnalyzing patterns from {reference_directory}:\n"
                
                for content in ref_contents:
                    if content.type == "file" and content.name.endswith(('.py', '.js', '.ts', '.java', '.cpp', '.c')):
                        try:
                            file_content = repo.get_contents(content.path)
                            decoded_content = file_content.decoded_content.decode('utf-8')
                            # Extract key patterns (imports, class definitions, function signatures)
                            lines = decoded_content.split('\n')
                            patterns = []
                            for line in lines[:20]:  # First 20 lines for patterns
                                line = line.strip()
                                if line.startswith(('import ', 'from ', 'class ', 'def ', '@')):
                                    patterns.append(line)
                            if patterns:
                                reference_analysis += f"\n### {content.name}:\n" + "\n".join(patterns[:5])
                        except:
                            continue
            except Exception as e:
                reference_analysis = f"\n\n## Reference Analysis Error: {str(e)}"
        
        # Use the provided file contents
        file_content = file_contents
        
        # Create unique file path with timestamp if it would conflict in main branch
        original_path = file_path
        try:
            existing_file = repo.get_contents(file_path, ref=base_branch)
            if existing_file:
                # Add timestamp to make it unique
                path_parts = file_path.rsplit('.', 1)
                if len(path_parts) == 2:
                    file_path = f"{path_parts[0]}_{timestamp}.{path_parts[1]}"
                else:
                    file_path = f"{file_path}_{timestamp}"
        except:
            # File doesn't exist, use original path
            pass
        
        # Step 1: Create new branch
        base_ref = repo.get_git_ref(f"heads/{base_branch}")
        base_sha = base_ref.object.sha
        
        new_ref = repo.create_git_ref(
            ref=f"refs/heads/{new_branch_name}",
            sha=base_sha
        )
        
        # Step 2: Create file in the new branch
        commit_message = f"Add {file_path} - AI generated based on requirements"
        result = repo.create_file(
            path=file_path,
            message=commit_message,
            content=file_content,
            branch=new_branch_name
        )
        
        # Step 3: Create Pull Request
        pr_title = f"Add AI-generated file: {file_path}"
        pr_body = f"""## Description
This PR adds a new file `{file_path}` generated automatically based on specified requirements.

## Requirements
{requirements}

## Generated Content
- **File**: `{file_path}`
- **Generated**: {timestamp}
- **Branch**: `{new_branch_name}`

## AI Analysis
The file was generated using AI based on the provided requirements{' and reference code patterns from ' + reference_directory if reference_directory else ''}.

## Code Preview
```
{file_content[:300]}...
```

## Review Notes
- ✅ File generated based on requirements
- ✅ Unique timestamp to avoid conflicts: {timestamp}
- ✅ Ready for review and integration
{reference_analysis if reference_analysis else ''}

**Please review the generated code and merge if it meets your requirements.**
"""
        
        # Create Pull Request
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=new_branch_name,
            base=base_branch
        )
        
        g.close()
        
        return f"""Successfully created AI-generated file with PR workflow:

📁 **File Created**: {file_path}
🌿 **Branch**: {new_branch_name}
📝 **Requirements**: {requirements}
⏰ **Timestamp**: {timestamp}

📋 **Pull Request Details**:
- PR Number: #{pr.number}
- PR URL: {pr.html_url}
- Status: {pr.state}
- Title: {pr.title}

🔗 **Links**:
- File URL: {result['content'].html_url}
- Commit SHA: {result['commit'].sha}

📄 **Generated Content Preview**:
{file_content[:200]}...

✅ **Next Steps**: 
The file has been created in a new branch and a pull request has been opened for review. 
Please review the PR and merge it if the generated code meets your requirements.
"""
        
    except Exception as e:
        return f"Error creating file with AI content and PR: {str(e)}"

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
            create_file_with_ai_content,
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

When creating files with AI content using create_file_with_ai_content:
1. Generate the actual file content based on the user's requirements
2. Provide the complete, functional code/content in the file_contents parameter
3. The requirements parameter should describe what the code should do (for PR documentation)
4. Create actual working code, not templates or placeholders

For example, if user asks "Create a simple HTML page that displays Hello, World!" in file "helloworld/index.html":
- Generate complete HTML with proper structure, styling, and "Hello, World!" text
- Pass this complete HTML as the file_contents parameter
- Use requirements like "Create a simple HTML page that displays Hello, World!" for documentation

You have access to these GitHub capabilities (when configured):
- List repository contents: Use list_repository_contents() to see files and directories
- Get file content: Use get_file_content() to read specific files
- Test GitHub connection: Use test_github_connection() to verify connectivity
- Get repository info: Use get_repository_info() to get repository details
- Create AI-generated files: Use create_file_with_ai_content() to create files with your generated content

When working with repositories:
- If no repository is specified, the default repository from environment variables will be used
- Repository format should be 'owner/repo' (e.g., 'microsoft/vscode')
- For file paths, use forward slashes even on Windows

Always generate complete, functional code that fulfills the user's requirements. 
Be concise and helpful. If you don't know something, just say so.
""",
    tools=available_tools,
)
