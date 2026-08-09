import os
import json
import urllib.request

token = os.environ.get("GH_PAT")
username = "mrityunjay-jha117"
url = "https://api.github.com/graphql"
headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}

query = """
query($login: String!) {
  user(login: $login) {
    followers { totalCount }
    repositories(first: 100, ownerAffiliations: [OWNER]) {
      totalCount
    }
  }
}
"""
data = json.dumps({"query": query, "variables": {"login": username}}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers=headers)
try:
    with urllib.request.urlopen(req) as response:
        result = json.loads(response.read().decode())
        print(json.dumps(result))
except Exception as e:
    print(e)
