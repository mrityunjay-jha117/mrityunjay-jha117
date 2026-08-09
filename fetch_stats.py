import os
import sys
import json
import urllib.request
import urllib.error

def fetch_github_stats(token, username):
    url = "https://api.github.com/graphql"
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    # We need to fetch all repositories to calculate LOC. 
    # For a real implementation, pagination is required.
    query = """
    query($login: String!) {
      user(login: $login) {
        followers { totalCount }
        repositories(first: 100, ownerAffiliations: OWNER, orderBy: {field: PUSHED_AT, direction: DESC}) {
          totalCount
          nodes {
            name
            stargazers { totalCount }
            defaultBranchRef {
              target {
                ... on Commit {
                  history(author: {id: ""}) {
                    totalCount
                  }
                }
              }
            }
            languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
              edges {
                size
                node { name }
              }
            }
          }
        }
        contributionsCollection {
          totalCommitContributions
          restrictedContributionsCount
        }
      }
    }
    """
    
    data = json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers)
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
    except urllib.error.URLError as e:
        print(f"Error fetching data: {e}")
        return None

    user_data = result.get('data', {}).get('user', {})
    if not user_data:
        print("Could not fetch user data.")
        return None

    followers = user_data.get('followers', {}).get('totalCount', 0)
    repos_count = user_data.get('repositories', {}).get('totalCount', 0)
    
    total_stars = 0
    total_commits = user_data.get('contributionsCollection', {}).get('totalCommitContributions', 0)
    
    import time
    
    total_additions = 0
    total_removals = 0
    
    rest_headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github.v3+json"
    }

    repos_nodes = user_data.get('repositories', {}).get('nodes', [])
    for repo in repos_nodes:
        total_stars += repo.get('stargazers', {}).get('totalCount', 0)
        repo_name = repo.get('name')
        
        # Hit the contributors stats API
        stats_url = f"https://api.github.com/repos/{username}/{repo_name}/stats/contributors"
        req = urllib.request.Request(stats_url, headers=rest_headers)
        
        max_retries = 3
        for attempt in range(max_retries):
            try:
                with urllib.request.urlopen(req) as response:
                    status_code = response.getcode()
                    if status_code == 202:
                        time.sleep(2)
                        continue
                    elif status_code == 200:
                        stats_data = json.loads(response.read().decode())
                        if isinstance(stats_data, list):
                            for contributor in stats_data:
                                author = contributor.get('author')
                                if author and author.get('login', '').lower() == username.lower():
                                    for week in contributor.get('weeks', []):
                                        total_additions += week.get('a', 0)
                                        total_removals += week.get('d', 0)
                        break
                    else:
                        break
            except urllib.error.URLError as e:
                print(f"Error fetching stats for {repo_name}: {e}")
                break

    total_loc = total_additions - total_removals
    if total_loc < 0:
        total_loc = 0

    return {
        "followers": followers,
        "stars": total_stars,
        "repos": repos_count,
        "commits": total_commits,
        "loc": total_loc,
        "additions": total_additions,
        "removals": total_removals
    }

def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("GH_TOKEN environment variable not set! Leaving current stats in details.json untouched.")
        return
    else:
        with open("details.json", "r") as f:
            data = json.load(f)
        username = data["resume_details"]["github_stats"]["username"]
        stats = fetch_github_stats(token, username)
        if not stats:
            sys.exit(1)

    # Update details.json
    with open("details.json", "r") as f:
        data = json.load(f)
    
    gh_stats = data["resume_details"]["github_stats"]
    gh_stats["followers"] = stats["followers"]
    gh_stats["stars"] = stats["stars"]
    gh_stats["repos"] = stats["repos"]
    gh_stats["commits"] = stats["commits"]
    gh_stats["loc"] = f"{stats['loc']:,}"
    gh_stats["additions"] = f"{stats['additions']:,}"
    gh_stats["removals"] = f"{stats['removals']:,}"

    with open("details.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Successfully updated details.json with fetched stats!")

if __name__ == "__main__":
    main()
