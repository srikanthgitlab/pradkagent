import os
import time
from dotenv import load_dotenv
from github import Github

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'prgitagent', '.env'))

def test_create_file():
    """Test creating a file in GitHub repository using PyGithub directly."""
    github_token = os.getenv("GITHUB_TOKEN")
    github_repository = os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    if not github_token:
        print("Error: GitHub token not configured")
        return
    
    print(f"Testing file creation for repository: {github_repository}")
    
    try:
        # Initialize PyGithub with personal access token
        g = Github(github_token)
        repo = g.get_repo(github_repository)
        
        # Test file details with unique timestamp
        timestamp = int(time.time())
        file_path = f"test_files/hello_world_{timestamp}.md"
        file_content = f"# Hello World!\n\nThis is a test file created via GitHub API.\n\nCreated by: GitHub API Test Script\nTimestamp: {timestamp}\nUnique ID: {timestamp}"
        commit_message = f"Create {file_path} via API test"
        branch_name = repo.default_branch
        
        print(f"Attempting to create file: {file_path}")
        print(f"Target branch: {branch_name}")
        print(f"Unique timestamp: {timestamp}")
        
        # Create the file (it should be unique due to timestamp)
        result = repo.create_file(
            path=file_path,
            message=commit_message,
            content=file_content,
            branch=branch_name
        )
        
        print(f"Successfully created file: {file_path}")
        print(f"Commit SHA: {result['commit'].sha}")
        print(f"File URL: {result['content'].html_url}")
        
        # List the contents to verify
        print("\nVerifying file creation by listing repository contents:")
        try:
            contents = repo.get_contents("test_files")
            print("Files in test_files directory:")
            for content in contents:
                print(f"- {content.path}")
        except Exception as e:
            print(f"test_files directory issue: {e}")
            
        g.close()
        print("\nFile creation test completed successfully!")
        
    except Exception as e:
        print(f"Error during file creation test: {e}")
        import traceback
        traceback.print_exc()

def test_create_file_with_query_format():
    """Test file creation using the query format from the LangChain code."""
    github_token = os.getenv("GITHUB_TOKEN")
    github_repository = os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    if not github_token:
        print("Error: GitHub token not configured")
        return
    
    print(f"\nTesting file creation with query format for repository: {github_repository}")
    
    try:
        g = Github(github_token)
        repo = g.get_repo(github_repository)
        
        # Simulate the file_query format from LangChain with unique timestamp
        timestamp = int(time.time())
        file_query = f"""test_files/sample_code_{timestamp}.py
# Sample Python Code - Generated at {timestamp}
def hello_world():
    print("Hello, World from GitHub API! Timestamp: {timestamp}")
    return "Success"

if __name__ == "__main__":
    hello_world()
"""
        
        # Parse the file_query like in the LangChain code
        lines = file_query.split("\n")
        file_path = lines[0]
        file_contents = "\n".join(lines[1:])
        
        print(f"Parsed file path: {file_path}")
        print(f"Unique timestamp: {timestamp}")
        print(f"File contents preview: {file_contents[:50]}...")
        
        # Create new file (should be unique due to timestamp)
        result = repo.create_file(
            path=file_path,
            message=f"Create {file_path}",
            content=file_contents,
            branch=repo.default_branch
        )
        print(f"Successfully created: {file_path}")
        print(f"File URL: {result['content'].html_url}")
        
        g.close()
        print("Query format test completed successfully!")
        
    except Exception as e:
        print(f"Error during query format test: {e}")
        import traceback
        traceback.print_exc()

def test_create_branch_and_pr():
    """Test creating a new branch, adding a file, and creating a pull request."""
    github_token = os.getenv("GITHUB_TOKEN")
    github_repository = os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    if not github_token:
        print("Error: GitHub token not configured")
        return
    
    print(f"\nTesting branch creation and PR for repository: {github_repository}")
    
    try:
        g = Github(github_token)
        repo = g.get_repo(github_repository)
        
        # Define branch and file details with unique timestamp
        timestamp = int(time.time())
        new_branch_name = f"feature/api-test-{timestamp}"
        base_branch = repo.default_branch
        test_file_path = f"api_tests/branch_test_{timestamp}.md"
        test_file_content = f"""# Branch Test File

This file was created to test the GitHub API branch and PR functionality.

## Details
- Branch: {new_branch_name}
- Base Branch: {base_branch}
- Created via: GitHub API Test Script
- Timestamp: {timestamp}
- Unique ID: {timestamp}

## Purpose
Testing automated branch creation, file addition, and pull request creation.

## Verification
This file should be unique due to the timestamp: {timestamp}
"""
        
        print(f"Creating new branch: {new_branch_name}")
        print(f"Base branch: {base_branch}")
        print(f"Unique timestamp: {timestamp}")
        
        # Step 1: Get the base branch reference
        base_ref = repo.get_git_ref(f"heads/{base_branch}")
        base_sha = base_ref.object.sha
        print(f"Base SHA: {base_sha}")
        
        # Step 2: Create new branch (should be unique due to timestamp)
        new_ref = repo.create_git_ref(
            ref=f"refs/heads/{new_branch_name}",
            sha=base_sha
        )
        print(f"Successfully created branch: {new_branch_name}")
        
        # Step 3: Create file in the new branch (should be unique due to timestamp)
        print(f"Creating file: {test_file_path}")
        result = repo.create_file(
            path=test_file_path,
            message=f"Add {test_file_path} to {new_branch_name}",
            content=test_file_content,
            branch=new_branch_name
        )
        print(f"Successfully created file: {test_file_path}")
        print(f"Commit SHA: {result['commit'].sha}")
        
        # Step 4: Create Pull Request (should be unique due to timestamp in branch name)
        pr_title = f"Add API test file via {new_branch_name}"
        pr_body = f"""## Description
This PR was created automatically to test the GitHub API functionality.

## Changes
- Added `{test_file_path}` with test content
- Created via automated GitHub API test script

## Branch Details
- Source Branch: `{new_branch_name}`
- Target Branch: `{base_branch}`
- Timestamp: {timestamp}
- Unique ID: {timestamp}

## Testing
This PR demonstrates:
1. ✅ Branch creation via API
2. ✅ File creation in new branch
3. ✅ Pull request creation via API

**Note:** This is a test PR and can be safely closed after review.
"""
        
        print(f"Creating pull request...")
        print(f"Title: {pr_title}")
        
        # Create new PR (should be unique due to unique branch name)
        pr = repo.create_pull(
            title=pr_title,
            body=pr_body,
            head=new_branch_name,
            base=base_branch
        )
        
        print(f"Successfully created pull request!")
        print(f"PR Number: #{pr.number}")
        print(f"PR URL: {pr.html_url}")
        print(f"PR Title: {pr.title}")
        print(f"PR State: {pr.state}")
        
        # Step 5: Verify the created content
        print(f"\nVerifying created content:")
        try:
            # List files in the new branch
            contents = repo.get_contents("", ref=new_branch_name)
            print(f"Files in branch {new_branch_name}:")
            for content in contents:
                if content.type == "dir":
                    print(f"📁 {content.path}/")
                else:
                    print(f"📄 {content.path}")
            
            # Try to list the api_tests directory if it exists
            try:
                api_tests_contents = repo.get_contents("api_tests", ref=new_branch_name)
                print(f"\nFiles in api_tests directory:")
                for content in api_tests_contents:
                    print(f"📄 {content.path}")
            except Exception as e:
                print(f"api_tests directory not found: {e}")
                
        except Exception as e:
            print(f"Error verifying content: {e}")
        
        g.close()
        print(f"\nBranch and PR test completed successfully!")
        print(f"Summary:")
        print(f"- Branch: {new_branch_name}")
        print(f"- File: {test_file_path}")
        print(f"- PR #{pr.number} created from {new_branch_name} to {base_branch}")
        print(f"- Unique timestamp: {timestamp}")
        
    except Exception as e:
        print(f"Error during branch and PR test: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("=== GitHub File Creation Tests with Unique Identifiers ===")
    print(f"Starting tests at timestamp: {int(time.time())}")
    print()
    
    test_create_file()
    test_create_file_with_query_format()
    test_create_branch_and_pr()
    
    print("\n=== All tests completed ===")
