import json
import urllib.request
import time

username = "mrityunjay-jha117"

# Fetch repos using REST API (no auth needed for public repos)
url = f"https://api.github.com/users/{username}/repos?per_page=100"
headers = {"Accept": "application/vnd.github.v3+json"}
req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
repos = json.loads(response.read().decode())

repo_stats = []

for repo in repos:
    repo_name = repo.get('name')
    stats_url = f"https://api.github.com/repos/{username}/{repo_name}/stats/contributors"
    req = urllib.request.Request(stats_url, headers=headers)
    
    total_additions = 0
    total_removals = 0
    
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req) as response:
                if response.getcode() == 202:
                    time.sleep(2)
                    continue
                elif response.getcode() == 200:
                    stats_data = json.loads(response.read().decode())
                    if isinstance(stats_data, list):
                        for contributor in stats_data:
                            author = contributor.get('author')
                            if author and author.get('login', '').lower() == username.lower():
                                for week in contributor.get('weeks', []):
                                    total_additions += week.get('a', 0)
                                    total_removals += week.get('d', 0)
                    break
        except Exception as e:
            print(f"Error fetching {repo_name}: {e}")
            break
            
    repo_stats.append({
        "name": repo_name,
        "additions": total_additions,
        "removals": total_removals,
        "loc": total_additions - total_removals
    })

repo_stats.sort(key=lambda x: x["additions"], reverse=True)
print(f"{'Repository':<30} | {'Additions':<10} | {'Removals':<10} | {'LOC':<10}")
print("-" * 68)
for stat in repo_stats:
    if stat['additions'] > 0:
        print(f"{stat['name']:<30} | {stat['additions']:<10} | {stat['removals']:<10} | {stat['loc']:<10}")
