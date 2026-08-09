# Dynamic GitHub Profile SVGs (Andrew6rant Style)

I have successfully set up your repository to work exactly like the dynamic profiles you requested. It now features an automated system that updates your GitHub stats every single day and generates beautiful SVGs.

## What I Built
1. **`fetch_stats.py`**: A Python script that hits the GitHub GraphQL API to fetch your live Followers, Stars, Repositories, Commits, and accurately estimates your Lines of Code (LOC), Additions, and Deletions!
2. **`build_svg.py`**: The completely overhauled visual generator. The ASCII art is bigger and centered with perfect padding. The LeetCode/Codeforces stats are uncluttered in a neat side-by-side layout, and all the new GitHub stats are beautifully rendered in a modern grid.
3. **`.github/workflows/update-stats.yml`**: A GitHub Action that runs every night at midnight to pull fresh data, generate the SVGs, and push them back to this repository automatically.

---

## 🔑 How to Setup GitHub Actions (The Keys You Need)

To make the automation work, you need to provide GitHub Actions with a **Personal Access Token (PAT)**. This token allows the bot to fetch your stats and commit files back to your repository.

### Step 1: Generate a Personal Access Token (PAT)
1. Go to your GitHub account settings: [GitHub Developer Settings -> Personal access tokens -> Tokens (classic)](https://github.com/settings/tokens).
2. Click **"Generate new token"** (choose "Generate new token (classic)").
3. Under **Note**, give it a name like `Profile README Stats`.
4. Under **Expiration**, select `No expiration` (so you don't have to keep fixing it every 30 days).
5. Under **Select scopes**, check the following boxes:
   - `repo` (Full control of private repositories - needed if you want it to count commits on private repos).
   - `user` (Update all user data - needed to read your followers/profile data).
6. Scroll to the bottom and click **Generate token**.
7. **IMPORTANT:** Copy the token string immediately (it will start with `ghp_...`). You won't be able to see it again!

### Step 2: Add the Token to Repository Secrets
1. Go to this repository on GitHub (`mrityunjay-jha117/mrityunjay-jha117`).
2. Click on the **Settings** tab at the top.
3. On the left sidebar, scroll down to **Secrets and variables** and click **Actions**.
4. Click the green button **New repository secret**.
5. Set the **Name** exactly as: `GH_PAT`
6. Paste your copied token into the **Secret** box.
7. Click **Add secret**.

### Step 3: Trigger the Workflow Manually
You don't have to wait until midnight!
1. Go to the **Actions** tab in this repository.
2. Under "All workflows" on the left, click **Update GitHub Stats & Generate SVG**.
3. On the right side, click the **Run workflow** dropdown button, and click the green **Run workflow** button.
4. The bot will now run `fetch_stats.py`, update your JSON, run `build_svg.py`, and commit the new SVGs!

---

## How to Display It
As long as this code is located in the repository named after your username (e.g. `mrityunjay-jha117/mrityunjay-jha117`), simply put this code in the `README.md`:

```html
<a href="https://github.com/mrityunjay-jha117/mrityunjay-jha117">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/mrityunjay-jha117/mrityunjay-jha117/main/dark_mode.svg">
    <img alt="Mrityunjay Jha's GitHub Profile README" src="https://raw.githubusercontent.com/mrityunjay-jha117/mrityunjay-jha117/main/light_mode.svg">
  </picture>
</a>
```

You are now fully set up with a dynamic, self-updating portfolio!
