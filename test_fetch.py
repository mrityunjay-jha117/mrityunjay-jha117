import os
import json
import urllib.request
import subprocess
import tempfile

username = "mrityunjay-jha117"
url = f"https://api.github.com/users/{username}/repos?per_page=100"
headers = {"Accept": "application/vnd.github.v3+json"}
req = urllib.request.Request(url, headers=headers)
response = urllib.request.urlopen(req)
repos = json.loads(response.read().decode())

total_additions = 0
total_removals = 0

with tempfile.TemporaryDirectory() as tmpdir:
    for repo in repos:
        repo_name = repo.get('name')
        repo_url = repo.get('clone_url')
        repo_dir = os.path.join(tmpdir, repo_name)
        
        subprocess.run(["git", "clone", "--bare", "--filter=blob:none", repo_url, repo_dir],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        cmd_stat = ["git", "-C", repo_dir, "log", "--author=mrityunjay", "--numstat", "--pretty=format:", "--no-merges", "--all"]
        try:
            out = subprocess.check_output(cmd_stat, stderr=subprocess.DEVNULL).decode()
            for line in out.splitlines():
                parts = line.strip().split()
                if len(parts) == 3:
                    adds = parts[0]
                    dels = parts[1]
                    if adds.isdigit(): total_additions += int(adds)
                    if dels.isdigit(): total_removals += int(dels)
        except Exception as e:
            print(e)
            
print(f"Total Additions: {total_additions}, Total Removals: {total_removals}")
