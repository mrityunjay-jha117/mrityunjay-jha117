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
            url
          }
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
        return None

    followers = user_data.get('followers', {}).get('totalCount', 0)
    total_repos = user_data.get('repositories', {}).get('totalCount', 0)
    repos_nodes = user_data.get('repositories', {}).get('nodes', [])
    
    total_stars = 0
    total_additions = 0
    total_removals = 0
    total_commits = 0
    
    # Bypass GitHub cache by cloning repos and parsing git logs directly!
    with tempfile.TemporaryDirectory() as tmpdir:
        for repo in repos_nodes:
            repo_name = repo.get('name')
            total_stars += repo.get('stargazers', {}).get('totalCount', 0)
            repo_url = repo.get('url')
            
            # Inject token to clone without hanging/prompting for passwords
            clone_url = repo_url.replace("https://github.com", f"https://x-access-token:{token}@github.com")
            repo_dir = os.path.join(tmpdir, repo_name)
            
            try:
                # Fast bare clone
                subprocess.run(
                    ["git", "clone", "--bare", "--filter=blob:none", clone_url, repo_dir],
                    check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
                )
                
                # We count all commits globally matching user's names
                cmd_commits = ["git", "-C", repo_dir, "rev-list", "--count", "--no-merges", f"--author={username}", "HEAD"]
                try:
                    out = subprocess.check_output(cmd_commits, stderr=subprocess.DEVNULL).decode().strip()
                    if out:
                        total_commits += int(out)
                except:
                    pass
                
                # Fetch exact additions and removals
                cmd_stat = ["git", "-C", repo_dir, "log", f"--author={username}", "--numstat", "--pretty=format:", "--no-merges", "HEAD"]
                try:
                    out = subprocess.check_output(cmd_stat, stderr=subprocess.DEVNULL).decode()
                    for line in out.splitlines():
                        parts = line.strip().split()
                        if len(parts) == 3:
                            adds, dels = parts[0], parts[1]
                            if adds.isdigit(): total_additions += int(adds)
                            if dels.isdigit(): total_removals += int(dels)
                except:
                    pass
            except:
                continue

    total_loc = total_additions - total_removals

    return {
        "repos": total_repos,
        "stars": total_stars,
        "followers": followers,
        "commits": total_commits,
        "additions": total_additions,
        "removals": total_removals,
        "loc": total_loc
    }

def main():
    token = os.environ.get("GH_TOKEN")
    if not token:
        print("GH_TOKEN environment variable not set! Leaving current stats in details.json untouched.")
        return

    with open("details.json", "r") as f:
        data = json.load(f)
    username = data["resume_details"]["github_stats"]["username"]
    
    stats = fetch_github_stats(token, username)
    if not stats:
        print("Failed to fetch GitHub stats.")
        sys.exit(1)

    gh_stats = data["resume_details"]["github_stats"]
    gh_stats["repos"] = stats["repos"]
    gh_stats["commits"] = stats["commits"]
    gh_stats["additions"] = f"{stats['additions']:,}"
    gh_stats["removals"] = f"{stats['removals']:,}"
    gh_stats["loc"] = f"{stats['loc']:,}"
    gh_stats["stars"] = stats["stars"]
    gh_stats["followers"] = stats["followers"]

    with open("details.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Successfully updated details.json with fetched stats!")

if __name__ == "__main__":
    main()
