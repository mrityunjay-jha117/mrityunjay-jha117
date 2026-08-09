import urllib.request, json
query = """
    query($login: String!) {
      user(login: $login) {
        repositories(first: 10, ownerAffiliations: OWNER) {
          totalCount
        }
      }
    }
"""
print(query)
