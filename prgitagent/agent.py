import os
from typing import List, Optional
from google.adk.agents import Agent
from dotenv import load_dotenv

# Load environment variables from the same directory as this file
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

def create_github_tools() -> List:
    """
    Create GitHub tools for the agent.
    Returns empty list if GitHub token is not configured.
    """
    github_token = os.getenv("GITHUB_TOKEN")
    if not github_token or github_token == "your_github_token_here":
        print("Warning: GitHub token not configured. GitHub tools will not be available.")
        print("To enable GitHub integration:")
        print("1. Create a GitHub Personal Access Token at https://github.com/settings/tokens")
        print("2. Add it to your .env file: GITHUB_TOKEN=your_token_here")
        return []
    
    try:
        from langchain_community.tools.github.tool import GitHubAction
        from langchain_community.utilities.github import GitHubAPIWrapper
        
        # Initialize GitHub wrapper
        # Note: Some operations may require setting GITHUB_REPOSITORY env var or passing repo in tool calls
        github_repository = os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")        
        print(f"Using GitHub repository: {github_repository}")
        
        github = GitHubAPIWrapper(
            github_token=github_token,
            github_repository=github_repository,
            github_app_id="",  # Explicitly pass empty string
            github_app_private_key=""  # Explicitly pass empty string
        )
        
        # Create comprehensive GitHub tools
        github_tools = [
            # Issues Management
            GitHubAction(
                name="get_issues",
                description="Get issues from a GitHub repository. Use format: owner/repo",
                mode="get_issues",
                api_wrapper=github,
            ),
            GitHubAction(
                name="get_issue",
                description="Get a specific issue from a GitHub repository. Use format: owner/repo and issue_number",
                mode="get_issue", 
                api_wrapper=github,
            ),
            GitHubAction(
                name="comment_on_issue",
                description="Comment on a GitHub issue. Requires repo, issue_number, and comment text",
                mode="comment_on_issue",
                api_wrapper=github,
            ),
            
            # Pull Requests Management
            GitHubAction(
                name="list_open_pull_requests",
                description="List open pull requests in a GitHub repository",
                mode="list_open_pull_requests",
                api_wrapper=github,
            ),
            GitHubAction(
                name="get_pull_request",
                description="Get a specific pull request from a GitHub repository",
                mode="get_pull_request",
                api_wrapper=github,
            ),
            GitHubAction(
                name="create_pull_request",
                description="Create a pull request in a GitHub repository",
                mode="create_pull_request",
                api_wrapper=github,
            ),
            GitHubAction(
                name="list_pull_request_files",
                description="List files included in a pull request",
                mode="list_pull_request_files",
                api_wrapper=github,
            ),
            GitHubAction(
                name="create_review_request",
                description="Create a review request for a pull request",
                mode="create_review_request",
                api_wrapper=github,
            ),
            
            # File Operations
            GitHubAction(
                name="create_file",
                description="Create a file in a GitHub repository",
                mode="create_file",
                api_wrapper=github,
            ),
            GitHubAction(
                name="read_file",
                description="Read a file from a GitHub repository. Use format: owner/repo and file_path",
                mode="read_file",
                api_wrapper=github,
            ),
            GitHubAction(
                name="update_file",
                description="Update an existing file in a GitHub repository",
                mode="update_file",
                api_wrapper=github,
            ),
            GitHubAction(
                name="delete_file",
                description="Delete a file from a GitHub repository",
                mode="delete_file",
                api_wrapper=github,
            ),
            GitHubAction(
                name="get_files_from_directory",
                description="Get files from a specific directory in a GitHub repository",
                mode="get_files_from_directory",
                api_wrapper=github,
            ),
            
            # Branch Management
            GitHubAction(
                name="list_branches_in_repo",
                description="List all branches in a GitHub repository",
                mode="list_branches_in_repo",
                api_wrapper=github,
            ),
            GitHubAction(
                name="set_active_branch",
                description="Set the active branch for GitHub operations",
                mode="set_active_branch",
                api_wrapper=github,
            ),
            GitHubAction(
                name="create_branch",
                description="Create a new branch in a GitHub repository",
                mode="create_branch",
                api_wrapper=github,
            ),
            GitHubAction(
                name="list_files_in_main_branch",
                description="Overview of existing files in the main branch",
                mode="list_files_in_main_branch",
                api_wrapper=github,
            ),
            GitHubAction(
                name="list_files_in_bot_branch",
                description="Overview of files in current working branch",
                mode="list_files_in_bot_branch",
                api_wrapper=github,
            ),
            
            # Search Operations
            GitHubAction(
                name="search_issues_and_prs",
                description="Search issues and pull requests in a GitHub repository",
                mode="search_issues_and_prs",
                api_wrapper=github,
            ),
            GitHubAction(
                name="search_code",
                description="Search code in a GitHub repository",
                mode="search_code",
                api_wrapper=github,
            ),
        ]
        
        print(f"GitHub integration enabled with {len(github_tools)} tools available.")
        return github_tools
        
    except ImportError as e:
        print(f"Warning: Could not import GitHub tools: {e}")
        print("Please install requirements: pip install -r requirements.txt")
        return []
    except Exception as e:
        print(f"Error initializing GitHub tools: {e}")
        return []

# Create GitHub tools
github_tools = create_github_tools()

root_agent = Agent(
    model='gemini-2.0-flash-001',
    name='root_agent',
    description='A helpful assistant for user questions with GitHub integration capabilities.',
    instruction="""You are a helpful assistant with GitHub integration capabilities. 
    
    You can help users with:
    1. General questions and assistance
    2. GitHub repository management (if configured)
    3. Reading and analyzing code from GitHub repositories
    4. Managing GitHub issues and pull requests
    
    GitHub capabilities (when available):
    - Get and search repository issues
    - Read files from repositories
    - Create and comment on issues
    - Create pull requests
    - Manage repository files
    - List branches and files in repositories
    - Search code and issues in repositories
    - Create and manage branches
    - Create and manage pull requests
    - Search code in repositories
    - Manage files in repositories

    You can also:
    - Answer general questions about GitHub usage
    - Provide guidance on using GitHub features
    - Assist with code-related queries
    - Help with repository management tasks
    - Provide information on GitHub best practices
    - Assist with troubleshooting GitHub issues

    
    
    Be concise and helpful. If you don't know something, just say so.
    If GitHub tools are not available, inform the user and guide them to configure their GitHub token.
    """,
    tools=github_tools,  # Add GitHub tools to the agent
)
