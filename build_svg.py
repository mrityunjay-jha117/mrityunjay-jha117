import json
import os

def create_svg(theme):
    # Read details
    with open('details.json', 'r') as f:
        data = json.load(f)
    details = data['resume_details']

    # Read ascii art from txt folder
    txt_path = f'txt/{theme}.txt'
    if not os.path.exists(txt_path):
        txt_path = 'image.txt'
    with open(txt_path, 'r') as f:
        ascii_art = f.read()

    # Colors based on theme
    if theme == 'dark':
        bg_color = "#0d1117"
        text_color = "#c9d1d9"
        accent_color = "#58a6ff"
        title_color = "#f0f6fc"
        card_bg = "#161b22"
        card_border = "#30363d"
        success_color = "#3fb950"  # For additions
        danger_color = "#f85149"   # For removals
    else:
        bg_color = "#ffffff"
        text_color = "#57606a"
        accent_color = "#0969da"
        title_color = "#24292f"
        card_bg = "#f6f8fa"
        card_border = "#d0d7de"
        success_color = "#1a7f37"
        danger_color = "#cf222e"

    width = 1150
    height = 620

    # Start SVG
    svg = f'''<svg width="{width}" height="{height}" viewBox="0 0 {width} {height}" fill="none" xmlns="http://www.w3.org/2000/svg">
    <style>
        .ascii {{
            font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, Courier, monospace;
            font-size: 14px;
            letter-spacing: 0px;
            fill: {text_color};
            white-space: pre;
        }}
        .title {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 34px;
            font-weight: 800;
            fill: {accent_color};
        }}
        .subtitle {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 18px;
            font-weight: 700;
            fill: {title_color};
        }}
        .text {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
            font-size: 14px;
            fill: {text_color};
        }}
        .stat-val {{
            font-weight: 700;
            fill: {title_color};
        }}
        .label {{
            font-weight: 600;
            fill: {title_color};
        }}
        .bg {{
            fill: {bg_color};
        }}
        .border {{
            stroke: {card_border};
            stroke-width: 1;
            fill: none;
            rx: 12;
        }}
        .card {{
            fill: {card_bg};
            stroke: {card_border};
            stroke-width: 1;
            rx: 8;
        }}
        .additions {{ fill: {success_color}; font-weight: bold; }}
        .removals {{ fill: {danger_color}; font-weight: bold; }}
    </style>
    
    <!-- Background -->
    <rect width="{width}" height="{height}" class="bg" rx="12"/>
    <rect x="0.5" y="0.5" width="{width-1}" height="{height-1}" class="border"/>

    <!-- ASCII Art (Left Side) - Centered vertically & Made larger -->
    <g transform="translate(35, 60)">
        <text class="ascii" xml:space="preserve">
'''
    
    lines = [line for line in ascii_art.split('\n') if line.strip() or line]
    line_height = 15.5
    for i, line in enumerate(lines):
        y_pos = i * line_height
        safe_line = line.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        svg += f'            <tspan x="0" y="{y_pos}">{safe_line}</tspan>\n'
    
    svg += '''        </text>
    </g>

    <!-- Details (Right Side) -->
    <g transform="translate(480, 50)">
'''
    
    y_cursor = 10
    
    # 1. Header
    svg += f'        <text x="0" y="{y_cursor + 20}" class="title">{details["name"]}</text>\n'
    svg += f'        <text x="0" y="{y_cursor + 45}" class="text" font-weight="500">{details["education"][0]["degree"]} @ {details["education"][0]["institution"]}</text>\n'
    
    card_y = y_cursor + 70
    card_spacing = 16
    
    # 2. Contact & Profiles (Full Width, 2 Columns to avoid clutter)
    svg += f'        <rect x="0" y="{card_y}" width="620" height="90" class="card" />\n'
    svg += f'        <text x="15" y="{card_y + 25}" class="subtitle">Profiles &amp; Contact</text>\n'
    
    # Left Col (Email, LinkedIn)
    svg += f'        <text x="15" y="{card_y + 52}" class="text"><tspan class="label">Email:</tspan> {details["contact"]["email"]}</text>\n'
    svg += f'        <text x="15" y="{card_y + 74}" class="text"><tspan class="label">LinkedIn:</tspan> {details["contact"]["linkedin"]}</text>\n'
    
    # Clean up the cluttered text for competitive programming
    lc_user = details["contact"]["LeetCode"].strip('/')
    cf_user = details["contact"]["Codeforces"].strip('/')
    lc_rank = details["Competetive programming"][0].replace("on LeetCode", "").strip()
    cf_rank = details["Competetive programming"][1].replace("on Codeforces", "").strip()
    
    # Right Col (LeetCode, Codeforces)
    svg += f'        <text x="310" y="{card_y + 52}" class="text"><tspan class="label">LeetCode:</tspan> {lc_user} ({lc_rank})</text>\n'
    svg += f'        <text x="310" y="{card_y + 74}" class="text"><tspan class="label">Codeforces:</tspan> {cf_user} ({cf_rank})</text>\n'
    
    # 3. GitHub Stats (Full Width, 3 Columns)
    card2_y = card_y + 90 + card_spacing
    svg += f'        <rect x="0" y="{card2_y}" width="620" height="110" class="card" />\n'
    svg += f'        <text x="15" y="{card2_y + 25}" class="subtitle">GitHub Statistics</text>\n'
    
    g_y = card2_y + 52
    
    # Row 1 of Stats
    svg += f'        <text x="15" y="{g_y}" class="text"><tspan class="label">Repositories:</tspan> <tspan class="stat-val">{details["github_stats"]["repos"]}</tspan></text>\n'
    svg += f'        <text x="220" y="{g_y}" class="text"><tspan class="label">Stars:</tspan> <tspan class="stat-val">{details["github_stats"].get("stars", 0)}</tspan></text>\n'
    svg += f'        <text x="420" y="{g_y}" class="text"><tspan class="label">Followers:</tspan> <tspan class="stat-val">{details["github_stats"].get("followers", 0)}</tspan></text>\n'
    
    g_y += 28
    
    # Row 2 of Stats
    svg += f'        <text x="15" y="{g_y}" class="text"><tspan class="label">Commits:</tspan> <tspan class="stat-val">{details["github_stats"]["commits"]}</tspan></text>\n'
    svg += f'        <text x="220" y="{g_y}" class="text"><tspan class="label">Lines of Code:</tspan> <tspan class="stat-val">{details["github_stats"].get("loc", 0)}</tspan></text>\n'
    svg += f'        <text x="420" y="{g_y}" class="text"><tspan class="additions">++{details["github_stats"].get("additions", 0)}</tspan> <tspan class="removals">--{details["github_stats"].get("removals", 0)}</tspan></text>\n'

    # 4. Technical Skills
    card3_y = card2_y + 110 + card_spacing
    svg += f'        <rect x="0" y="{card3_y}" width="620" height="135" class="card" />\n'
    svg += f'        <text x="15" y="{card3_y + 25}" class="subtitle">Technical Skills</text>\n'
    
    s_y = card3_y + 50
    svg += f'        <text x="15" y="{s_y}" class="text"><tspan class="label">Languages:</tspan> {", ".join(details["technical_skills"]["languages"])}</text>\n'
    s_y += 22
    svg += f'        <text x="15" y="{s_y}" class="text"><tspan class="label">Web Dev:</tspan> {", ".join(details["technical_skills"]["Web Development"])}</text>\n'
    s_y += 22
    svg += f'        <text x="15" y="{s_y}" class="text"><tspan class="label">Databases:</tspan> {", ".join(details["technical_skills"]["databases_and_orm"])}</text>\n'
    s_y += 22
    svg += f'        <text x="15" y="{s_y}" class="text"><tspan class="label">DevOps:</tspan> {", ".join(details["technical_skills"]["devops"])}</text>\n'
    
    # 5. Experience
    card4_y = card3_y + 135 + card_spacing
    svg += f'        <rect x="0" y="{card4_y}" width="620" height="80" class="card" />\n'
    svg += f'        <text x="15" y="{card4_y + 25}" class="subtitle">Experience</text>\n'
    
    svg += f'        <text x="15" y="{card4_y + 55}" class="text"><tspan class="label">{details["experience"][0]["company"]}</tspan> - {details["experience"][0]["role"]}</text>\n'
    svg += f'        <text x="15" y="{card4_y + 55}" class="text" text-anchor="end" dx="585">{details["experience"][0]["duration"]}</text>\n'

    svg += '''    </g>
</svg>'''

    with open(f'{theme}_mode.svg', 'w', encoding='utf-8') as f:
        f.write(svg)

create_svg('light')
create_svg('dark')
print("SVGs created successfully with updated layout and new GitHub Stats!")
