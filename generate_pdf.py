#!/usr/bin/env python3
"""
Generate Roman_Ekimov_CV.pdf directly from Jekyll _data/*.yml files.
"""
import os
import re
import base64
import subprocess
import yaml

workspace_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(workspace_dir, "_data")
photo_path = os.path.join(workspace_dir, "photo.png")
pdf_path = os.path.join(workspace_dir, "Roman_Ekimov_CV.pdf")
html_path = os.path.join(workspace_dir, "cv.html")

# Load YAML Data
with open(os.path.join(data_dir, "profile.yml"), "r", encoding="utf-8") as f:
    profile = yaml.safe_load(f)

with open(os.path.join(data_dir, "specialties.yml"), "r", encoding="utf-8") as f:
    specialties = yaml.safe_load(f)

with open(os.path.join(data_dir, "experience.yml"), "r", encoding="utf-8") as f:
    experience = yaml.safe_load(f)

with open(os.path.join(data_dir, "education.yml"), "r", encoding="utf-8") as f:
    education = yaml.safe_load(f)

# Load Photo
with open(photo_path, "rb") as f:
    photo_b64 = base64.b64encode(f.read()).decode("utf-8")

def md_to_html(text):
    # Convert **bold** to <strong>bold</strong>
    text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', text)
    # Convert [link](url) to <a href="url">link</a>
    text = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', text)
    return text

# Build Specialties HTML
specialties_html = ""
for group in specialties:
    skills_joined = ", ".join(group["skills"])
    specialties_html += f"""
      <div class="skill-group">
        <span class="skill-name">{group['category']}:</span>
        <span class="skill-val">{skills_joined}</span>
      </div>"""

# Build Experience HTML
experience_html = ""
for job in experience:
    company_link = f"""<a href="{job['company_url']}">{job['company']}</a>""" if job.get('company_url') else job['company']
    tagline = f"""<div class="exp-tagline">{job['tagline']}</div>""" if job.get('tagline') else ""
    
    bullets_html = ""
    for bullet in job['bullets']:
        bullets_html += f"<li>{md_to_html(bullet)}</li>\n"

    experience_html += f"""
    <div class="exp-item">
      <div class="exp-header">
        <div>
          <span class="exp-role">{job['role']}</span> &mdash; <span class="exp-company">{company_link}</span>
        </div>
        <div class="exp-date">{job['dates']}</div>
      </div>
      {tagline}
      <ul class="exp-bullets">
        {bullets_html}
      </ul>
    </div>"""

# Build Education HTML
education_html = ""
for edu in education:
    faculty_str = f" ({edu['faculty']})" if edu.get('faculty') else ""
    education_html += f"""
    <div class="edu-item">
      <div>
        <div class="edu-title">{edu['school']}</div>
        <div class="edu-sub">{edu['degree']}{faculty_str}</div>
      </div>
      <div class="edu-date">{edu['years']}</div>
    </div>"""

html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>{profile['name']} - CV</title>
<style>
  @page {{
    size: A4;
    margin: 12mm 14mm 12mm 14mm;
  }}

  * {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    color: #1e293b;
    background-color: #ffffff;
    line-height: 1.45;
    font-size: 9.5pt;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  a {{
    color: #0284c7;
    text-decoration: none;
  }}

  .header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 16px;
    padding-bottom: 12px;
    border-bottom: 2.5px solid #0284c7;
    margin-bottom: 14px;
  }}

  .header-info {{
    flex: 1;
  }}

  .name {{
    font-size: 22pt;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.5px;
    line-height: 1.1;
    margin-bottom: 4px;
  }}

  .headline {{
    font-size: 11.5pt;
    font-weight: 600;
    color: #0284c7;
    margin-bottom: 8px;
  }}

  .contacts {{
    display: flex;
    flex-wrap: wrap;
    gap: 5px 14px;
    font-size: 8.5pt;
    color: #475569;
  }}

  .contact-item {{
    display: inline-flex;
    align-items: center;
    gap: 4px;
  }}

  .contact-item svg {{
    width: 13px;
    height: 13px;
    fill: #0284c7;
    flex-shrink: 0;
  }}

  .avatar {{
    width: 82px;
    height: 82px;
    border-radius: 50%;
    object-fit: cover;
    border: 2.5px solid #0284c7;
    box-shadow: 0 2px 6px rgba(0, 0, 0, 0.12);
    flex-shrink: 0;
  }}

  .section {{
    margin-bottom: 11px;
  }}

  .section-title {{
    font-size: 10.5pt;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.8px;
    color: #0f172a;
    border-bottom: 1.5px solid #e2e8f0;
    padding-bottom: 3px;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .section-title svg {{
    width: 14px;
    height: 14px;
    fill: #0284c7;
  }}

  .skills-grid {{
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 6px 14px;
  }}

  .skill-group {{
    font-size: 8.5pt;
    line-height: 1.35;
  }}

  .skill-name {{
    font-weight: 700;
    color: #0f172a;
  }}

  .skill-val {{
    color: #334155;
  }}

  .exp-item {{
    margin-bottom: 10px;
    break-inside: avoid;
    page-break-inside: avoid;
  }}

  .exp-header {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 2px;
  }}

  .exp-role {{
    font-size: 10pt;
    font-weight: 700;
    color: #0f172a;
  }}

  .exp-company {{
    font-weight: 600;
    color: #0284c7;
  }}

  .exp-date {{
    font-size: 8.5pt;
    font-weight: 600;
    color: #64748b;
    white-space: nowrap;
  }}

  .exp-tagline {{
    font-size: 8.5pt;
    color: #64748b;
    font-style: italic;
    margin-bottom: 4px;
  }}

  .exp-bullets {{
    list-style-type: disc;
    padding-left: 16px;
    margin: 0;
  }}

  .exp-bullets li {{
    font-size: 8.5pt;
    color: #334155;
    margin-bottom: 2.5px;
    line-height: 1.34;
  }}

  .exp-bullets li strong {{
    color: #0f172a;
  }}

  .edu-item {{
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    break-inside: avoid;
    page-break-inside: avoid;
    margin-top: 4px;
  }}

  .edu-title {{
    font-size: 9.5pt;
    font-weight: 700;
    color: #0f172a;
  }}

  .edu-sub {{
    font-size: 8.8pt;
    color: #475569;
    margin-top: 2px;
  }}

  .edu-date {{
    font-size: 8.5pt;
    font-weight: 600;
    color: #64748b;
  }}
</style>
</head>
<body>

  <!-- Header -->
  <div class="header">
    <div class="header-info">
      <div class="name">{profile['name']}</div>
      <div class="headline">{profile['headline']}</div>
      <div class="contacts">
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M20 4H4c-1.1 0-1.99.9-1.99 2L2 18c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>
          <a href="mailto:{profile['email']}">{profile['email']}</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
          {profile['location']}
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M9.78 18.65l.28-4.23 7.68-6.92c.34-.31-.07-.46-.52-.19L7.74 13.3 3.64 12c-.88-.25-.89-.86.2-1.3l15.97-6.16c.73-.33 1.43.18 1.15 1.3l-2.72 12.81c-.19.91-.74 1.13-1.5 0.71L12.6 15.9l-1.99 1.93c-.23.23-.42.42-.83.42z"/></svg>
          <a href="{profile['telegram_url']}">@{profile['telegram']}</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M19 3a2 2 0 0 1 2 2v14a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h14m-.5 15.5v-5.3a3.26 3.26 0 0 0-3.26-3.26c-.85 0-1.84.52-2.28 1.3v-1.11h-2.79v8.37h2.79v-4.93c0-.77.62-1.4 1.39-1.4a1.4 1.4 0 0 1 1.4 1.4v4.93h2.75M6.46 10.9v8.37H9.2V10.9H6.46M7.83 6.45a1.6 1.6 0 1 0 0 3.2 1.6 1.6 0 0 0 0-3.2z"/></svg>
          <a href="{profile['linkedin_url']}">linkedin.com/in/{profile['linkedin']}</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M12 2A10 10 0 0 0 2 12c0 4.42 2.87 8.17 6.84 9.5.5.08.66-.23.66-.5v-1.69c-2.77.6-3.36-1.34-3.36-1.34-.46-1.16-1.11-1.47-1.11-1.47-.91-.62.07-.6.07-.6 1 .07 1.53 1.03 1.53 1.03.87 1.52 2.34 1.07 2.91.83.1-.65.35-1.09.63-1.34-2.22-.25-4.55-1.11-4.55-4.92 0-1.11.38-2 1.03-2.71-.1-.25-.45-1.29.1-2.64 0 0 .84-.27 2.75 1.02.79-.22 1.65-.33 2.5-.33.85 0 1.71.11 2.5.33 1.91-1.29 2.75-1.02 2.75-1.02.55 1.35.2 2.39.1 2.64.65.71 1.03 1.6 1.03 2.71 0 3.82-2.34 4.66-4.57 4.91.36.31.69.92.69 1.85V21c0 .27.16.59.67.5C19.14 20.16 22 16.42 22 12A10 10 0 0 0 12 2z"/></svg>
          <a href="{profile['github_url']}">github.com/{profile['github']}</a>
        </div>
        <div class="contact-item">
          <svg viewBox="0 0 24 24"><path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 17.93c-3.95-.49-7-3.85-7-7.93 0-.62.08-1.21.21-1.79L9 15v1c0 1.1.9 2 2 2v1.93zm6.9-2.54c-.26-.81-1-1.39-1.9-1.39h-1v-3c0-.55-.45-1-1-1H8v-2h2c.55 0 1-.45 1-1V7h2c1.1 0 2-.9 2-2v-.41c2.93 1.19 5 4.06 5 7.41 0 2.08-.8 3.97-2.1 5.39z"/></svg>
          <a href="https://toywar.github.io">toywar.github.io</a>
        </div>
      </div>
    </div>
    <img src="data:image/png;base64,{photo_b64}" class="avatar" alt="{profile['name']}">
  </div>

  <!-- Specialties -->
  <div class="section">
    <div class="section-title">
      <svg viewBox="0 0 24 24"><path d="M22.7 19l-9.1-9.1c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/></svg>
      Technical Specialties
    </div>
    <div class="skills-grid">
      {specialties_html}
    </div>
  </div>

  <!-- Experience -->
  <div class="section">
    <div class="section-title">
      <svg viewBox="0 0 24 24"><path d="M20 6h-4V4c0-1.11-.89-2-2-2h-4c-1.11 0-2 .89-2 2v2H4c-1.11 0-1.99.89-1.99 2L2 19c0 1.11.89 2 2 2h16c1.11 0 2-.89 2-2V8c0-1.11-.89-2-2-2zm-6 0h-4V4h4v2z"/></svg>
      Professional Experience
    </div>
    {experience_html}
  </div>

  <!-- Education -->
  <div class="section" style="break-inside: avoid; page-break-inside: avoid;">
    <div class="section-title">
      <svg viewBox="0 0 24 24"><path d="M5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82zM12 3L1 9l11 6 9-4.91V17h2V9L12 3z"/></svg>
      Education
    </div>
    {education_html}
  </div>

</body>
</html>
"""

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"Rendered HTML to {html_path}")

def find_chrome():
    """Locate a Chrome/Chromium binary (env override, PATH, then common install paths)."""
    import glob
    import shutil

    env_bin = os.environ.get("CHROME_BIN")
    if env_bin and os.path.exists(env_bin):
        return env_bin

    for name in ("google-chrome", "google-chrome-stable", "chromium", "chromium-browser"):
        found = shutil.which(name)
        if found:
            return found

    patterns = [
        "/opt/pw-browsers/chromium-*/chrome-linux/chrome",
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    ]
    for pattern in patterns:
        matches = sorted(glob.glob(pattern))
        if matches:
            return matches[-1]

    raise SystemExit("No Chrome/Chromium binary found. Set CHROME_BIN to one.")

cmd = [
    find_chrome(),
    "--headless=new",
    "--disable-gpu",
    "--no-sandbox",
    "--no-pdf-header-footer",
    f"--print-to-pdf={pdf_path}",
    html_path
]

res = subprocess.run(cmd, capture_output=True, text=True)
if os.path.exists(pdf_path):
    print(f"Successfully generated PDF: {pdf_path} ({os.path.getsize(pdf_path)} bytes)")
else:
    print("Error generating PDF:", res.stderr)
