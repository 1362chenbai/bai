#!/usr/bin/env python

import requests

def search_github_projects(query):
    url = f'https://api.github.com/search/repositories?q={query}&sort=stars&order=desc'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def main():
    query = 'language:Python+stars:>1000+topic:中文'
    results = search_github_projects(query)
    print(results)

if __name__ == '__main__':
    main()