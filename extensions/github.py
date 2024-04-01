import subprocess
from github import Github
from git import Repo
import os
def search_github_repos(query, max_results=10):
    # Replace 'YOUR_ACCESS_TOKEN' with your actual GitHub access token
    g = Github("YOUR_ACCESS_TOKEN")

    # Search for repositories based on the query
    repos = g.search_repositories(query, sort="stars", order="desc")

    # List to store results
    results = []

    # Iterate through search results and collect repository information
    for repo in repos[:max_results]:
        results.append({
            "name": repo.full_name,
            "description": repo.description,
            "url": repo.html_url,
            "stars": repo.stargazers_count
        })

    return results

def clone_repository(repo_url, destination_folder):
    try:
        # Clone the repository
        Repo.clone_from(repo_url, destination_folder)
        print(f"Repository cloned successfully to {destination_folder}")
    except Exception as e:
        return(f"An error occurred: {str(e)}")


def upload_to_github(project_dir, repo_name, commit_message):
    try:
        # Navigate to the project directory
        os.chdir(project_dir)

        # Initialize a Git repository object
        repo = Repo.init(project_dir)

        # Add all files to the repository
        repo.index.add("*")

        # Commit changes with the provided commit message
        repo.index.commit(commit_message)

        # Push changes to the remote repository
        origin = repo.create_remote('origin', f'git@github.com:USERNAME/{repo_name}.git')
        origin.push()

        print("Files uploaded to GitHub successfully")
    except Exception as e:
        return(f"An error occurred: {str(e)}")

def create_repo(repo_name, description=""):
    try:
        # Initialize PyGithub with access token
        g = Github("YOUR_ACCESS_TOKEN")

        # Create a new repository
        user = g.get_user()
        repo = user.create_repo(repo_name, description=description)

        print(f"Repository '{repo_name}' created successfully")
        print(f"URL: {repo.html_url}")
    except Exception as e:
        return(f"An error occurred: {str(e)}")

def get_commits(repo_name):
    try:
        # Initialize PyGithub with access token
        g = Github("YOUR_ACCESS_TOKEN")

        # Get the repository
        repo = g.get_repo(repo_name)

        # Get the list of commits
        commits = repo.get_commits()

        # Print information about each commit
        print("Commits:")
        for commit in commits:
            print(f"SHA: {commit.sha}, Author: {commit.author.login}, Date: {commit.commit.author.date}, Message: {commit.commit.message}")
    except Exception as e:
        return(f"An error occurred: {str(e)}")

def get_issues(repo_name):
    try:
        # Initialize PyGithub with access token
        g = Github("YOUR_ACCESS_TOKEN")

        # Get the repository
        repo = g.get_repo(repo_name)

        # Get the list of issues
        issues = repo.get_issues(state="open")

        # Print information about each issue
        print("Issues:")
        for issue in issues:
            print(f"Title: {issue.title}, Author: {issue.user.login}, State: {issue.state}")
    except Exception as e:
        return(f"An error occurred: {str(e)}")

def get_repos_owned_by_owner():
    try:
        # Initialize PyGithub with access token
        g = Github("YOUR_ACCESS_TOKEN")

        # Get the user or organization
        user_or_org = g.get_user("Likhithsai2580")

        # Get the list of repositories owned by the user or organization
        repos = user_or_org.get_repos()

        # Print information about each repository
        print(f"Repositories owned by Likhithsai2580:")
        for repo in repos:
            print(repo.full_name)
        return repos
    except Exception as e:
        return(f"An error occurred: {str(e)}")


def github_function(action, *args):
    try:
        # Replace 'YOUR_ACCESS_TOKEN' with your actual GitHub access token
        g = Github("access_token")

        if action == 'search_repos':
            query, max_results = args
            return search_github_repos(g, query, max_results)

        elif action == 'clone_repo':
            repo_url, destination_folder = args
            return clone_repository(repo_url, destination_folder)

        elif action == 'upload_to_github':
            project_dir, repo_name, commit_message = args
            return upload_to_github(project_dir, repo_name, commit_message)

        elif action == 'create_repo':
            repo_name, description = args
            return create_repo(g, repo_name, description)

        elif action == 'get_commits':
            repo_name = args[0]
            return get_commits(g, repo_name)

        elif action == 'get_issues':
            repo_name = args[0]
            return get_issues(g, repo_name)

        elif action == 'get_repos_owned_by_owner':
            return get_repos_owned_by_owner(g)

        else:
            return "Invalid action specified."

    except Exception as e:
        return f"An error occurred: {str(e)}"
