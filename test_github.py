import os
from dotenv import load_dotenv
from github import Github

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), 'prgitagent', '.env'))

def test_github_connection():
    github_token = os.getenv("GITHUB_TOKEN")
    github_repository = os.getenv("GITHUB_REPOSITORY", "srikanthgitlab/pradkagent")
    
    print(f"Testing GitHub connection for repository: {github_repository}")
    
    try:
        # Initialize PyGithub with personal access token
        g = Github(github_token)
        
        # Get the repository
        repo = g.get_repo(github_repository)
        
        # List files in the root directory
        contents = repo.get_contents("")
        print("\nFiles in repository root:")
        for content in contents:
            print(f"- {content.path}")
            
    except Exception as e:
        print(f"Error: {e}")
    finally:
        try:
            g.close()
        except:
            pass

if __name__ == "__main__":
    test_github_connection()
