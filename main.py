#!/usr/bin/env python

import requests
import base64
import os

def search_github_projects(query):
    url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def update_projects_md(projects, existing_content):
    new_content = existing_content + '\n'
    for project in projects:
        name = project['name']
        html_url = project['html_url']
        new_content += f'- [{name}]({html_url})\n'
    return new_content


def main():
    query = 'language:Python stars:>1000 topic:中文'
    results = search_github_projects(query)
    projects = results['items']

    # Read existing content of projects.md
    url = 'https://api.github.com/repos/1362chenbai/bai/contents/projects.md?ref=main'
    try:
        response = requests.get(url)
        response.raise_for_status()
        content = response.json()['content']
        existing_content = base64.b64decode(content).decode('utf-8')
    except requests.exceptions.RequestException as e:
        print(f"Error reading projects.md: {e}")
        return

    # Update projects.md with new projects
    updated_content = update_projects_md(projects, existing_content)

    # Get the SHA of the latest commit
    url = 'https://api.github.com/repos/1362chenbai/bai/git/refs/heads/main'
    try:
        response = requests.get(url)
        response.raise_for_status()
        sha = response.json()['object']['sha']
    except requests.exceptions.RequestException as e:
        print(f"Error getting latest commit SHA: {e}")
        return

    # Update projects.md on GitHub
    url = 'https://api.github.com/repos/1362chenbai/bai/contents/projects.md'
    headers = {
        'Authorization': f'token {os.environ["GITHUB_TOKEN"]} '
    }
    data = {
        'message': 'Update projects.md with new projects',
        'content': base64.b64encode(updated_content.encode('utf-8')).decode('utf-8'),
        'sha': sha,
        'branch': 'main'
    }
    try:
        response = requests.put(url, headers=headers, json=data)
        response.raise_for_status()
        print("projects.md updated successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error updating projects.md: {e}")
        return

if __name__ == '__main__':
    main()